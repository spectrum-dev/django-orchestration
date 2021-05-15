from copy import deepcopy

from orchestrator.models import BlockRegistry


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
            nodes_with_no_dependencies = {k for k, v in dependency_graph.adjacency_list.items() if not v}

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

        self.is_valid = self.validate()

    def _get_block_by_id(self, block_id):
        """
            Retrieves a block by its ID

            block_id: ID of block in flow
        """
        try:
            return self.vertices[block_id]
        except KeyError:
            raise Exception(f'The Block ID {block_id} could not be found')

    @staticmethod
    def _get_block_data_from_registry(block_type, block_id):
        try:
            return BlockRegistry. \
                objects. \
                all(). \
                filter(block_type=block_type). \
                filter(block_id=block_id). \
                first()
        except Exception as e:
            raise Exception(e);

    def _dfs(self, visited, block_id_in_flow, allowed_block_data, target_block_data, blocks_found):
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
                if (
                        str(block_data["blockType"]) == str(allowed_block["blockType"])
                        and str(block_data["blockId"]) == str(allowed_block["blockId"])
                ):
                    blocks_found.append(block_id_in_flow)

                    if len(blocks_found) == int(target_block_data["number"]):
                        return

        if block_id_in_flow not in visited:
            visited.add(block_id_in_flow)

            for neighbor in self.dependency_graph[block_id_in_flow]:
                self._dfs(visited, neighbor, allowed_block_data, target_block_data, blocks_found)

    def validate(self):
        """
            Validates a flow to ensure that all nodes are connected correctly

            TODO: Also validate input data
        """
        is_valid = True

        for task in self.batched_tasks:
            for task_to_be_run in task:
                block_data = self._get_block_by_id(task_to_be_run)
                block_registry_data = self._get_block_data_from_registry(block_data["blockType"], block_data["blockId"])

                if len(self.dependency_graph) == 0:
                    is_valid = is_valid and len(block_registry_data.validations["input"]["required"]) == 0
                else:
                    blocks_found = []
                    for required_block in block_registry_data.validations["input"]["required"]:
                        visited = set()
                        self._dfs(visited, task_to_be_run, block_registry_data.validations["input"]["allowed_blocks"],
                                  required_block, blocks_found)

                    assembled_dependency_list_from_flow = {}
                    for item in set(blocks_found):
                        item_block_data = self._get_block_by_id(item)
                        if item_block_data["blockType"] not in assembled_dependency_list_from_flow:
                            assembled_dependency_list_from_flow[item_block_data["blockType"]] = 0
                        assembled_dependency_list_from_flow[item_block_data["blockType"]] += 1

                    for required in block_registry_data.validations["input"]["required"]:
                        is_valid = is_valid and assembled_dependency_list_from_flow[required["blockType"]] == required[
                            "number"]

        return is_valid

    def run(self):
        """
            Runs a flow
        """
        pass
