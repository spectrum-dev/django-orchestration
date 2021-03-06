from celery import current_app
from celery.result import allow_join_result

from orchestrator.exceptions import ScreenerBulkDataBlockDneException
from orchestrator.models import BlockRegistry
from orchestrator.services.flow.graph import DependencyGraph


class SpectrumFlow:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.input_payloads = {}
        # TODO: Can populate this from the database to perform some caching optimization
        self.outputs = {}
        self.signals = {}
        self.edge_validation = {}

        graph = DependencyGraph(vertices, edges)

        self.graph = graph.graph.adjacency_list
        self.dependency_graph = graph.dependency_graph.adjacency_list
        self.batched_tasks = graph.batched_tasks
        self.strategy_type = self.get_strategy_type()

        # Valid
        self.valid = self.validate()

    def get_block_in_flow_by_id(self, block_id):
        """
        Retrieves a block in a flow by its ID

        Inputs:
            - block_id: ID of block in flow

        Raises:
            - Exception: When block ID could not be found
        """
        try:
            return self.vertices[block_id]
        except KeyError:
            raise Exception(f"The block id '{block_id}' could not be found")

    def perform_dfs(
        self,
        visited,
        block_id_in_flow,
        allowed_block_data,
        target_block_data,
        blocks_found,
    ):
        block_data = self.get_block_in_flow_by_id(block_id_in_flow)

        if any(
            block_data["blockType"] == target_block
            for target_block in target_block_data["blockType"]
        ):
            for allowed_block in allowed_block_data:
                if block_data["blockType"] == allowed_block["blockType"] and str(
                    block_data["blockId"]
                ) == str(allowed_block["blockId"]):

                    blocks_found.add(block_id_in_flow)

                    # TODO: This is where a "more than" block flow will happen
                    if len(blocks_found) == int(target_block_data["number"]):
                        return

        if block_id_in_flow not in visited:
            visited.add(block_id_in_flow)

            for neighbor in self.dependency_graph[block_id_in_flow]:
                self.perform_dfs(
                    visited,
                    neighbor,
                    allowed_block_data,
                    target_block_data,
                    blocks_found,
                )

    def get_strategy_type(self):
        """
        Goes through the nodeList to determine the strategy type
        """
        strategy_type = "BACKTEST"
        for _, metadata in self.vertices.items():
            if metadata["blockType"] == "BULK_DATA_BLOCK":
                strategy_type = "SCREENER"
                break

        return strategy_type

    def validate(self):
        """
        Performs validation on the existing flow to ensure
        that all nodes have data filled in, all edge connections
        are valid and the sequence of steps that need to be run is valid

        Output:
            - Queue denoting order that operations need to run (indexed by block ID in flow)
                [{1}, {2, 3}, {4}, {5}] -> self.batched_tasks


            - Dictionary mapping each block ID in flow to the payload that needs to be sent,
              with a reference to data required from previous steps
                {
                    1: {
                        inputs: {},
                        outputs: {
                            ref: [ None ]
                        }
                    },
                    2: {
                        inputs: {},
                        outputs: {
                            ref: [ 1 ]
                        }
                    }
                    ...
                }
        """
        # Base case -> there are no tasks to be run
        if len(self.batched_tasks) == 0:
            return {
                "isValid": False,
                "code": "VALIDATE-001",
                "description": "There are no tasks to be run",
            }

        # Edge Validation -> Checks if each edge connection is valid and creates a dictionary representing edge - valid pairs
        for edge in self.edges:
            try:
                source_block = self.get_block_in_flow_by_id(edge["source"])
                target_block = self.get_block_in_flow_by_id(edge["target"])

                target_block_registry_data = BlockRegistry.objects.get(
                    block_type=target_block["blockType"],
                    block_id=target_block["blockId"],
                )

                # Ensures that the edge is valid
                is_valid_edge = any(
                    [
                        str(allowed_input_block["blockId"])
                        == str(source_block["blockId"])
                        and allowed_input_block["blockType"]
                        == source_block["blockType"]
                        for allowed_input_block in target_block_registry_data.validations[
                            "input"
                        ][
                            "allowed_blocks"
                        ]
                    ]
                )

                # Error description if edge is not valid
                allowed_connections = []
                if not is_valid_edge:
                    for allowed_block in target_block_registry_data.validations[
                        "input"
                    ]["allowed_blocks"]:
                        try:
                            block_registry_data = BlockRegistry.objects.get(
                                block_type=allowed_block["blockType"],
                                block_id=allowed_block["blockId"],
                            )
                            allowed_connections.append(block_registry_data.block_name)
                        except BlockRegistry.DoesNotExist:
                            pass

                self.edge_validation[edge["id"]] = {
                    "status": is_valid_edge,
                    "target_block": target_block_registry_data.block_name,
                    "allowed_connections": allowed_connections,
                }

            except BlockRegistry.DoesNotExist:
                return {
                    "isValid": False,
                    "code": "VALIDATE-008",
                    "description": f"The block with parameters block type {target_block['blockType']} and block ID {target_block['blockId']} could not be found in the database",
                }

        all_valid = all(
            [value["status"] for key, value in self.edge_validation.items()]
        )

        if not all_valid:
            return {
                "isValid": False,
                "code": "VALIDATE-002",
                "description": f"Input into target block with block type {source_block['blockType']} and block id {source_block['blockId']}",
            }

        # Block Form Input Validation -> checks if every block has all the inputs it needs
        for task in self.batched_tasks:
            for block in task:
                block_data = self.get_block_in_flow_by_id(block)

                # Creates the input payloads object
                self.input_payloads[block] = {"inputs": {}, "outputs": {"ref": set()}}
                self.input_payloads[block]["blockType"] = block_data["blockType"]
                self.input_payloads[block]["blockId"] = block_data["blockId"]
                if "data" in block_data:
                    self.input_payloads[block]["data"] = block_data["data"]

                for key, value in block_data.items():
                    if type(value) is dict and "value" in value.keys():
                        if value["value"] == "" or value["value"] == None:
                            return {
                                "isValid": False,
                                "code": "VALIDATE-003",
                                "description": f"The value for key {key} in block id {block} is invalid / empty",
                            }

                        if (
                            "inputFromConnectionValue" in value
                            and value["inputFromConnectionValue"] != ""
                        ):
                            self.input_payloads[block]["inputs"][
                                key
                            ] = f'{value["inputFromConnectionValue"]}-{value["value"]}'
                        else:
                            # Populates the inputs record with the required keys
                            self.input_payloads[block]["inputs"][key] = value["value"]

        # Block Edge Input Validation -> Checks if block "has access" to the data it needs to run correctly
        for task in self.batched_tasks:
            for block in task:
                block_data = self.get_block_in_flow_by_id(block)
                for key, value in block_data.items():
                    try:
                        block_type = block_data["blockType"]
                        block_id = block_data["blockId"]

                        block_registry_data = BlockRegistry.objects.get(
                            block_type=block_type,
                            block_id=block_id,
                        )

                        # For a block with no dependencies but has multiple required attributes
                        if (
                            len(self.dependency_graph[block]) == 0
                            and len(
                                block_registry_data.validations["input"]["required"]
                            )
                            != 0
                        ):
                            return {
                                "isValid": False,
                                "code": "VALIDATE-004",
                                "description": f"The block of type {block_type} and id {block_id}. The required number of inputs is {len(block_registry_data.validations['input']['required'])} but there were 0.",
                            }

                        # Will search for dependencies data
                        required_blocks_found = set()
                        for required_block in block_registry_data.validations["input"][
                            "required"
                        ]:
                            visited = set()
                            self.perform_dfs(
                                visited,
                                block,
                                block_registry_data.validations["input"][
                                    "allowed_blocks"
                                ],
                                required_block,
                                required_blocks_found,
                            )

                        assembled_dependency_list = {}
                        for required_block in required_blocks_found:
                            required_block_data = self.get_block_in_flow_by_id(
                                required_block
                            )

                            if (
                                required_block_data["blockType"]
                                not in assembled_dependency_list
                            ):
                                assembled_dependency_list[
                                    required_block_data["blockType"]
                                ] = []
                            assembled_dependency_list[
                                required_block_data["blockType"]
                            ].append(required_block)

                        for required_block in block_registry_data.validations["input"][
                            "required"
                        ]:
                            if not any(
                                req_block in assembled_dependency_list
                                for req_block in required_block["blockType"]
                            ):
                                return {
                                    "isValid": False,
                                    "code": "VALIDATE-005",
                                    "description": f"Required block {required_block['blockType']} is not in the assembled dependency list",
                                }

                            total_number = 0
                            for req_block in required_block["blockType"]:
                                if req_block in assembled_dependency_list:
                                    total_number += len(
                                        assembled_dependency_list[req_block]
                                    )

                            if total_number < required_block["number"]:
                                return {
                                    "isValid": False,
                                    "code": "VALIDATE-006",
                                    "description": f"The number of blocks of {required_block['blockType']} is less than the number ({required_block['number']}) required",
                                }

                            # Case where there is only meant to be one incoming value, and if there is a direct connection between two blocks, to only use that data
                            if any(
                                (
                                    req_block in assembled_dependency_list
                                    and len(assembled_dependency_list[req_block])
                                    > required_block["number"]
                                )
                                for req_block in required_block["blockType"]
                            ):
                                # Retrieves a list of adjacent blocks that could be of varying types
                                adjacent_blocks = list(self.dependency_graph[block])
                                # Subset of adjacent_blocks filtered by the block type
                                adjacent_blocks_of_matching_type = []
                                # Checks if adjacent block is in the list of required blocks
                                for adjacent_block in adjacent_blocks:
                                    if any(
                                        adjacent_block
                                        in assembled_dependency_list.get(req_block, [])
                                        for req_block in required_block["blockType"]
                                    ):
                                        adjacent_blocks_of_matching_type.append(
                                            adjacent_block
                                        )

                                # If the adjancent blocks fulfil the required amount, it sets the data pulled to those adjacent blocks
                                if (
                                    len(adjacent_blocks_of_matching_type)
                                    == required_block["number"]
                                ):
                                    for req_block in required_block["blockType"]:
                                        if req_block in assembled_dependency_list:
                                            assembled_dependency_list[
                                                req_block
                                            ] = adjacent_blocks_of_matching_type

                            # Adds the block of this block type to the input_payloads output ref
                            for req_block in required_block["blockType"]:
                                if req_block in assembled_dependency_list:
                                    for required_block in assembled_dependency_list[
                                        req_block
                                    ]:
                                        self.input_payloads[block]["outputs"][
                                            "ref"
                                        ].add(required_block)

                    except BlockRegistry.DoesNotExist:
                        return {
                            "isValid": False,
                            "code": "VALIDATE-007",
                            "description": f"The block with parameters block type {block_type} and block ID {block_id} could not be found in the database",
                        }

        # A check for screeners to ensure that the strategy is full
        if self.strategy_type == "SCREENER":
            signal_block = False
            for _, value in self.vertices.items():
                if value["blockType"] == "SIGNAL_BLOCK":
                    signal_block = True
                    break

            if not signal_block:
                return {
                    "isValid": False,
                    "code": "VALIDATE-008",
                    "description": "The screener being run is not complete",
                }

        return {"isValid": True, "code": "VALIDATE-OK", "description": ""}

    def celery_send_helper(self, block_id_in_flow, payload):
        """
        Helper function that invokes the low-level celery
        function 'send_task' and sends a request payload
        """
        output_key = f"{payload['blockType']}-{payload['blockId']}-{block_id_in_flow}"

        if "data" in payload:
            return (output_key, None, payload["data"])

        task = current_app.send_task(
            "blocks.celery.event_ingestor",
            args=(payload,),
            queue="blocks",
            routing_key="block_task",
        )

        return (output_key, task, None)

    def run(self):
        """
        Takes a queue of operations that need to be run and a
        dictionary mapping of what each request payload should
        look like and orchestrates the running of a flow

        Outputs:
            - An output cache
        """
        for tasks in self.batched_tasks:
            queued_items = []
            for block in tasks:
                payload = self.input_payloads[block]
                payload["outputs"]["ref"] = list(payload["outputs"]["ref"])

                # Implement logic to pull data from the self.outputs
                if len(payload["outputs"]["ref"]) > 0:
                    for ref in payload["outputs"]["ref"]:
                        # Searches for corresponding output key and adds that data to the payload based on the ref
                        for key in self.outputs.keys():
                            if key.split("-")[2] == ref:
                                payload["outputs"][key] = self.outputs[key]

                    del payload["outputs"]["ref"]

                response = self.celery_send_helper(
                    block_id_in_flow=block, payload=payload
                )
                queued_items.append(response)

            for queued_item in queued_items:
                output_key, pending_value, provided_data = queued_item

                with allow_join_result():
                    if pending_value:
                        response = pending_value.get()

                        # Some responses come with a "response" key, which we will extract out
                        if "response" in response:
                            self.outputs[output_key] = response["response"]
                        else:
                            self.outputs[output_key] = response
                    else:
                        self.outputs[output_key] = provided_data

        # Extracts signals
        last_tasks = self.batched_tasks[-1]
        if len(last_tasks) == 1:
            last_task_id = last_tasks.pop()
            last_block_data = self.get_block_in_flow_by_id(last_task_id)
            if last_block_data["blockType"] == "SIGNAL_BLOCK":
                for key in self.outputs.keys():
                    if key.split("-")[2] == last_task_id:
                        self.signals = self.outputs[key]

        return True

    def get_bulk_data(self):
        """
        Takes a BULK_DATA_BLOCK and splits it up into several individual backtest flows.
        Aggregates results at the end of the flow and returns a JSON List of the names of tickers that meet the situations outlined
        """

        def send_helper(block_id_in_flow, payload):
            """
            Helper function that invokes the low-level celery
            function 'send_task' and sends a request payload
            """
            output_key = (
                f"{payload['blockType']}-{payload['blockId']}-{block_id_in_flow}"
            )

            task = current_app.send_task(
                "blocks.celery.event_ingestor",
                args=(payload,),
                queue="blocks",
                routing_key="screenr_task",
            )

            return (output_key, task)

        # ASSUMPTION: BULK_DATA_BLOCK should always be the first block in the flow
        task_containing_bulk_data = self.batched_tasks[0]
        print(task_containing_bulk_data)
        bulk_data_task = task_containing_bulk_data.pop()

        # If this Block ID is not a data block, raise an exception
        payload = self.input_payloads[bulk_data_task]
        if payload["blockType"] != "BULK_DATA_BLOCK":
            raise ScreenerBulkDataBlockDneException

        # Prepares the payload and makes the request to the block monolith
        del payload["outputs"]["ref"]
        _, task = send_helper(bulk_data_task, payload)

        # Gets the response and returns to the user
        with allow_join_result():
            response = task.get()
            return bulk_data_task, response, payload
