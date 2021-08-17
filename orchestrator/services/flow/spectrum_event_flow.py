from orchestrator.models import BlockRegistry
from orchestrator.services.flow.spectrum_flow import DependencyGraph


class SpectrumEventFlow:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.input_payloads = {}
        # TODO: Can populate this from the database to perform some caching optimization
        self.outputs = {}
        self.edge_validation = {}

        graph = DependencyGraph(vertices, edges)

        self.graph = graph.graph.adjacency_list
        self.dependency_graph = graph.dependency_graph.adjacency_list
        self.batched_tasks = graph.batched_tasks

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

        if block_data["blockType"] == target_block_data["blockType"]:
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
                            ref: None
                        }
                    },
                    2: {
                        inputs: {},
                        outputs: {
                            ref: 1
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

                for key, value in block_data.items():
                    if type(value) is dict and "value" in value.keys():
                        if value["value"] == "" or value["value"] == None:
                            return {
                                "isValid": False,
                                "code": "VALIDATE-003",
                                "description": f"The value for key {key} in block id {block} is invalid / empty",
                            }

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
                                ] = 0
                            assembled_dependency_list[
                                required_block_data["blockType"]
                            ] += 1

                        for required_block in block_registry_data.validations["input"][
                            "required"
                        ]:
                            if (
                                not required_block["blockType"]
                                in assembled_dependency_list
                            ):
                                return {
                                    "isValid": False,
                                    "code": "VALIDATE-005",
                                    "description": f"Required block {required_block['blockType']} is not in the assembled dependency list",
                                }

                            if (
                                assembled_dependency_list[required_block["blockType"]]
                                < required_block["number"]
                            ):
                                return {
                                    "isValid": False,
                                    "code": "VALIDATE-006",
                                    "description": f"The number of blocks of {required_block['blockType']} is less than the number ({required_block['number']}) required",
                                }

                        for required_block in required_blocks_found:
                            self.input_payloads[block]["outputs"]["ref"].add(
                                required_block
                            )
                    except BlockRegistry.DoesNotExist:
                        return {
                            "isValid": False,
                            "code": "VALIDATE-007",
                            "description": f"The block with parameters block type {block_type} and block ID {block_id} could not be found in the database",
                        }

        return {"isValid": True, "code": "VALIDATE-OK", "description": ""}

    def run(self):
        """
        Takes a queue of operations that need to be run and a
        dictionary mapping of what each request payload should
        look like and orchestrates the running of a flow

        Outputs:
            - An output cache
        """
        pass
