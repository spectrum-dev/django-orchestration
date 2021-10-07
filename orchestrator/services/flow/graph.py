from copy import deepcopy


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
