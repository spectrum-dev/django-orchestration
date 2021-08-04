import json
import requests
from os import environ
from copy import deepcopy

from orchestrator.models import BlockRegistry
from orchestrator.services.results.main import main


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def __repr__(self):
        return repr(self.adjacency_list)

    def insert(self, source_vertex, dest_vertex):
        """
        Inserts one or both vertices (depending on if either exists) and
        connects one vertex to the other

        Attributes:
            source_vertex: Start / Originating Vertex
            dest_vertex: Destination Vertex
        """
        if not (source_vertex in self.adjacency_list):
            self.adjacency_list[source_vertex] = set()

        self.adjacency_list[source_vertex].add(dest_vertex)


class DependencyGraph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

        self.graph = self.generate_graph()
        self.dependency_graph = self.generate_dependency_graph()
        self.batched_tasks = self.generate_batched_tasks()

    def generate_graph(self):
        """
        Generates an adjacency list graph representation using the node and edge pairs
        """
        graph = Graph()

        # Initializes the Adjacency List of Blocks
        for block_id, vertex in self.vertices.items():
            if block_id not in graph.adjacency_list:
                graph.adjacency_list[block_id] = set()

        for edge in self.edges:
            graph.insert(edge["source"], edge["target"])

        return graph

    def generate_dependency_graph(self):
        """
        Transposes the adjacency list to create a graph of dependencies
        """
        dependency_graph = Graph()

        # Initializes the adjacency list with initial values
        for source_vertex, _ in self.graph.adjacency_list.items():
            if source_vertex not in dependency_graph.adjacency_list:
                dependency_graph.adjacency_list[source_vertex] = set()

        # Reverses the direction of the node connections
        for source_vertex, dest_vertices in self.graph.adjacency_list.items():
            if source_vertex not in dependency_graph.adjacency_list:
                dependency_graph.adjacency_list[source_vertex] = set()

            for dest_vertex in dest_vertices:
                dependency_graph.insert(dest_vertex, source_vertex)

        return dependency_graph

    def generate_batched_tasks(self):
        """
        Creates a series of batches tasks that need to be executed sequentially
        """
        batches = []

        dependency_graph = deepcopy(self.dependency_graph)

        while dependency_graph.adjacency_list:
            # Retrieves nodes with no dependencies
            nodes_with_no_dependencies = {
                k for k, v in dependency_graph.adjacency_list.items() if not v
            }

            if not nodes_with_no_dependencies:
                raise ValueError("Circular Dependency Found")

            for node in nodes_with_no_dependencies:
                del dependency_graph.adjacency_list[node]

            for deps in dependency_graph.adjacency_list.values():
                deps.difference_update(nodes_with_no_dependencies)

            batches.append({name for name in nodes_with_no_dependencies})

        return batches


class SpectrumFlow:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

        graph = DependencyGraph(vertices, edges)

        self.graph = graph.graph.adjacency_list
        self.dependency_graph = graph.dependency_graph.adjacency_list
        self.batched_tasks = graph.batched_tasks

        self.edge_validation = {}
        (self.is_valid, self.is_valid_description) = self.run(mode="VALIDATE")

    def _get_block_by_id(self, block_id):
        """
        Retrieves a block by its ID

        block_id: ID of block in flow
        """
        try:
            return self.vertices[block_id]
        except KeyError:
            raise Exception(f"The Block ID {block_id} could not be found")

    @staticmethod
    def _get_block_data_from_registry(block_type, block_id):
        try:
            return (
                BlockRegistry.objects.all()
                .filter(block_type=block_type)
                .filter(block_id=block_id)
                .first()
            )
        except Exception as e:
            raise Exception(e)

    def _dfs(
        self,
        visited,
        block_id_in_flow,
        allowed_block_data,
        target_block_data,
        blocks_found,
    ):
        """
        Recursively iterates through directed adjancency list

        Attempts to determine which blocks downstream in the sequence have required data

        Attributes:
            visited: Set of blocks that have been traversed
            block_id_in_flow: Current block ID being unpacked
            allowed_block_data: List of allowed input blocks
            target_block_data: Block Type and Number of Blocks being searched for
        """
        block_data = self._get_block_by_id(block_id_in_flow)

        if block_data["blockType"] == target_block_data["blockType"]:
            for allowed_block in allowed_block_data:
                if str(block_data["blockType"]) == str(
                    allowed_block["blockType"]
                ) and str(block_data["blockId"]) == str(allowed_block["blockId"]):
                    blocks_found.append(block_id_in_flow)

                    if len(blocks_found) == int(target_block_data["number"]):
                        return

        if block_id_in_flow not in visited:
            visited.add(block_id_in_flow)

            for neighbor in self.dependency_graph[block_id_in_flow]:
                self._dfs(
                    visited,
                    neighbor,
                    allowed_block_data,
                    target_block_data,
                    blocks_found,
                )

    def _make_run_request(
        self, block_id_in_flow, block_registry_data, input_payload, output_payload
    ):
        """
        Hits the `/run` endpoint for each block to complete the request

        Attributes
        block_id_in_flow: Block ID generated by the frontend
        block_registry_data: Block Data queried from the frontend
        input_payload: Input Payload
        output_payload: Output Payload
        """

        request_url = f"{environ['API_BASE_URL']}/{block_registry_data.block_type}/{block_registry_data.block_id}/run"

        # Input Transformation
        input_cleaned_payload = {}
        for k, v in input_payload.items():
            if type(v) is dict and "value" in v:
                input_cleaned_payload[k] = v["value"]

        request_payload = {"input": input_cleaned_payload, "output": output_payload}

        r = requests.post(request_url, json=request_payload)

        output = {}
        if r.status_code == 200:
            block_type_id_key = f"{block_registry_data.block_type}-{block_registry_data.block_id}-{block_id_in_flow}"

            if block_type_id_key not in output.keys():
                output[block_type_id_key] = {}

            try:
                response_json = r.json()
                if "response" in response_json:
                    output[block_type_id_key] = response_json["response"]
                else:
                    raise Exception("JSON Key 'response' could not be found")

            except json.decoder.JSONDecodeError as e:
                raise Exception("JSON Decode Error")
            except Exception as e:
                raise Exception("Unhandled Exception: ", e)
        else:
            print("Error: ", r.json())

        return output

    def run(self, mode="VALIDATE"):
        """
        Validates a flow to ensure that all nodes are connected correctly
        """

        output_cache = {}

        def _get_data_from_cache(block_id_in_flow):
            """
            Retrieves data about block from cache

            Attributes:
            block_id: Block ID from Flow
            """
            block_data = self._get_block_by_id(block_id_in_flow)
            block_registry_data = self._get_block_data_from_registry(
                block_data["blockType"], block_data["blockId"]
            )

            cache_key = f"{block_registry_data.block_type}-{block_registry_data.block_id}-{block_id_in_flow}"

            if cache_key in output_cache.keys():
                return cache_key, output_cache[cache_key]
            else:
                raise Exception(
                    f"Data does not exist in cache for {block_id_in_flow} with {cache_key}"
                )

        is_valid = True

        if len(self.batched_tasks) == 0:
            is_valid = False

        for task in self.batched_tasks:
            for task_to_be_run in task:
                block_data = self._get_block_by_id(task_to_be_run)
                block_registry_data = self._get_block_data_from_registry(
                    block_data["blockType"], block_data["blockId"]
                )

                # Iterate through block data to gauge whether inputs exist
                for key, value in block_data.items():
                    if type(value) is dict and "value" in value.keys():
                        if value["value"] == "":
                            is_valid = False

                # Checks if the graph has an edge
                if len(self.dependency_graph[task_to_be_run]) == 0:
                    is_valid = (
                        is_valid
                        and len(block_registry_data.validations["input"]["required"])
                        == 0
                    )

                    if mode == "RUN":
                        response = self._make_run_request(
                            task_to_be_run, block_registry_data, block_data, {}
                        )

                        # Adds to a cache to ensure that requests don't need to be re-run
                        output_cache = {**output_cache, **response}
                else:
                    blocks_found = []
                    for required_block in block_registry_data.validations["input"][
                        "required"
                    ]:
                        visited = set()
                        self._dfs(
                            visited,
                            task_to_be_run,
                            block_registry_data.validations["input"]["allowed_blocks"],
                            required_block,
                            blocks_found,
                        )

                    output_payload = {}
                    assembled_dependency_list_from_flow = {}
                    for item in set(blocks_found):
                        item_block_data = self._get_block_by_id(item)

                        if (
                            item_block_data["blockType"]
                            not in assembled_dependency_list_from_flow
                        ):
                            assembled_dependency_list_from_flow[
                                item_block_data["blockType"]
                            ] = 0
                        assembled_dependency_list_from_flow[
                            item_block_data["blockType"]
                        ] += 1

                        if mode == "RUN":
                            cache_key, response = _get_data_from_cache(item)
                            output_payload = {**output_payload, cache_key: response}

                    if mode == "RUN":
                        response = self._make_run_request(
                            task_to_be_run,
                            block_registry_data,
                            block_data,
                            output_payload,
                        )

                        # Adds to a cache to ensure that requests don't need to be re-run
                        output_cache = {**output_cache, **response}

                    for required in block_registry_data.validations["input"][
                        "required"
                    ]:
                        if required["blockType"] in assembled_dependency_list_from_flow:
                            is_valid = (
                                is_valid
                                and assembled_dependency_list_from_flow[
                                    required["blockType"]
                                ]
                                == required["number"]
                            )
                        else:
                            is_valid = False

        if mode == "VALIDATE":
            # Edge Validation Logic
            for edge in self.edges:
                source_block = self._get_block_by_id(edge["source"])
                target_block = self._get_block_by_id(edge["target"])

                target_block_data = self._get_block_data_from_registry(
                    target_block["blockType"], target_block["blockId"]
                )

                is_edge_valid = False
                for allowed_block in target_block_data.validations["input"][
                    "allowed_blocks"
                ]:
                    is_edge_valid = is_edge_valid or (
                        (str(allowed_block["blockId"]) == str(source_block["blockId"]))
                        and (
                            str(allowed_block["blockType"])
                            == str(source_block["blockType"])
                        )
                    )

                target_block = self._get_block_data_from_registry(
                    target_block["blockType"], target_block["blockId"]
                )

                allowed_connections = []
                if not is_edge_valid:
                    for allowed_block in target_block_data.validations["input"][
                        "allowed_blocks"
                    ]:
                        block_data = self._get_block_data_from_registry(
                            allowed_block["blockType"], allowed_block["blockId"]
                        )
                        allowed_connections.append(block_data.block_name)

                self.edge_validation[edge["id"]] = {
                    "status": is_edge_valid,
                    "target_block": target_block.block_name,
                    "allowed_connections": allowed_connections,
                }

            # If any edges are invalid, returns False
            all_valid = map(
                lambda edge: True if edge["status"] else False, self.edge_validation
            )
            if not all_valid:
                return (False, "Edge connections are invalid")

            # Validates single backtest block per strategy
            backtest_block = [
                value["blockType"]
                for _, value in self.vertices.items()
                if "STRATEGY_BLOCK" in value["blockType"]
            ]

            if len(backtest_block) > 1:
                return (False, "You may only have one backtest block per strategy")

            return (is_valid, "")

        elif mode == "RUN":
            backtest_block = [
                string for string in output_cache.keys() if "STRATEGY_BLOCK" in string
            ]

            # Creates the result matrix associated with the backtest
            if len(backtest_block) == 1:
                output_cache["results"] = main(output_cache[backtest_block[0]])

            return output_cache
        else:
            return None
