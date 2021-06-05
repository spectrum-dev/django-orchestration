class Graph:
    def __init__(self):
        self.adjacency_list = {}

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
