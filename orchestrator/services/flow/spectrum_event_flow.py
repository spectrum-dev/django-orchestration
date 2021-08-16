
from orchestrator.models import BlockRegistry
from orchestrator.services.flow.spectrum_flow import DependencyGraph

class SpectrumEventFlow:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
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
                "description": "There are no tasks to be run"
            }

        # Edge Validation -> Checks if each edge connection is valid and creates a dictionary representing edge - valid pairs
        for edge in self.edges:
            try:
                source_block = self.get_block_in_flow_by_id(edge["source"])
                target_block = self.get_block_in_flow_by_id(edge["target"])

                target_block_registry_data = BlockRegistry.objects.get(
                    block_type=target_block["blockType"],
                    block_id=target_block["blockId",]
                )
                
                # Ensures that the edge is valid
                is_valid_edge = any([
                    str(allowed_input_block["blockId"]) == str(source_block["blockId"])
                        and allowed_input_block["blockType"] == source_block["blockType"] for allowed_input_block in 
                        target_block_registry_data.validations["input"]["allowed_blocks"]
                ])

                # Error description if edge is not valid
                allowed_connections = []
                if not is_valid_edge:
                    for allowed_block in target_block_registry_data.validations["input"]["allowed_blocks"]:
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
                pass

        all_valid = map(
            lambda edge: True if edge["status"] else False, self.edge_validation
        )

        if not all_valid:
            return {
                "isValid": False,
                "code": "VALIDATE-002",
                "description": f"""
                    Input into target block with block type {source_block["blockType"]}
                    and block id {source_block["blockId"]}
                """
            }

        # Block Form Input Validation -> checks if every block has all the inputs it needs
        for task in self.batched_tasks:
            for block in task:
                block_data = self.get_block_in_flow_by_id(block)
                for key, value in block_data.items():
                    if (
                        type(value) is dict 
                        and "value" in value.keys()
                    ):
                        if value["value"] == "" or value["value"] == None:
                            return {
                                "isValid": False,
                                "code": "VALIDATE-003",
                                "description": f"The value for key {key} in block {block} is invalid / empty"
                            }

        # TODO: Block Edge Input Validation -> Checks if block "has access" to the data it needs to run correctly
        #       Important thing here is to
        for task in self.batched_tasks:
            for block in task:
                block_data = self.get_block_in_flow_by_id(block)
                for key, value in block_data.items():
                    try:
                        block_type = block_data["block_type"]
                        block_id = block_data["block_id"]

                        block_registry_data = BlockRegistry.objects.get(
                            block_type=block_type,
                            block_id=block_id,
                        )

                        # For a block with no dependencies but has multiple required attributes 
                        if len(self.dependency_graph[block]) == 0 and block_registry_data.validation["input"]["required"] != 0:
                            return {
                                "isValid": False,
                                "code": "VALIDATE-003",
                                "description": f""
                            }
                        
                        # Will search for dependencies data
                        required_blocks_found = []
                        for required_block in block_registry_data.validations["input"]["required"]:
                            pass


                    except BlockRegistry.DoesNotExist:
                        return {
                            "isValid": False,
                            "code": "VALIDATE-004",
                            "description": f"""
                                The block with parameters block type {block_type} and block ID {block_id}
                                could not be found in the database
                            """
                        }

        # TODO: Once the above three are done, we can assume (for now) that a flow is valid.
        #       Iterate through the blocks again and determine 
        pass
    def run(self):
        """
            Takes a queue of operations that need to be run and a
            dictionary mapping of what each request payload should
            look like and orchestrates the running of a flow

            Outputs:
                - An output cache
        """
        pass