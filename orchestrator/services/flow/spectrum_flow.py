import json
import logging
import requests
from copy import deepcopy

from orchestration.settings import env
from orchestrator.models import BlockRegistry
from orchestrator.services.flow.graph import Graph

class SpectrumFlow:
    """
        Ingests a list of vertices and edges to create a representation of a "spectrum flow"
    """
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

        self.graph = self.generate_adjacency_list()
        self.dependency_graph = self.generate_dependency_graph()
        self.batched_tasks = self.get_batched_tasks()
    
    def generate_adjacency_list(self):
        """
            Creates an adjacency list when passed in a list of nodes and edges
        """
        graph = Graph()
        
        # Initializes the adjacency list with initial values
        for vertex in self.vertices:
            id = vertex["id"]
            if not id in graph.adjacency_list:
                graph.adjacency_list[id] = set()

        # Iterates through the edges and populates the values in the adjacency list
        for edge in self.edges:
            graph.insert(edge["source"], edge["target"])

        return graph

    def generate_dependency_graph(self):
        """
            Creates a depedency graph by transposing the adjacency list
        """
        dependency_graph = Graph()
        
        # Initializes the adjacency list with initial values
        for source_vertex, _ in self.graph.adjacency_list.items():
            if not source_vertex in dependency_graph.adjacency_list:
                dependency_graph.adjacency_list[source_vertex] = set()

        # Reverses the direction of the node connections
        for source_vertex, dest_vertices in self.graph.adjacency_list.items():
            if not source_vertex in dependency_graph.adjacency_list:
                dependency_graph.adjacency_list[source_vertex] = set()
            
            for dest_vertex in dest_vertices:
                dependency_graph.insert(dest_vertex, source_vertex)
        
        return dependency_graph
    
    def get_batched_tasks(self):
        """
            Traverses through the adjacency list to sequence through tasks
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
    
    def run_batched_tasks_v3(self):
        def get_block_by_id(id):
            """
                Retrieves a block from the list of vertices passed in initially
                Attributes:
                id: ID of Block in Flow
            """
            for vertex in self.vertices:
                if (vertex["id"] == id):
                    return vertex
        
        def dfs(visited, block_id_in_flow, allowed_block_data, target_block_data, blocks_found):
            """
                Performs a DFS recursively that iterates through the directed adjacency list.
                It attempts to determine which blocks downstream in the sequence have their required data

                Attributes:
                visited: Set of blocks that have already been traversed
                block_id_in_flow: The current block ID being iterated on
                allowed_block_data: List of permitted input blocks
                target_block_data: States the block type and number of blocks being searched for
            """
            
            block_data = get_block_by_id(block_id_in_flow)

            if (block_data["data"]["metadata"]["blockType"] == target_block_data["blockType"]):
                for allowed_block in allowed_block_data:
                    if (str(block_data["data"]["metadata"]["blockType"]) == str(allowed_block["blockType"])
                    and str(block_data["data"]["metadata"]["blockId"]) == str(allowed_block["blockId"])):
                        blocks_found.append(block_id_in_flow)

                        # Stopping Condition
                        if (len(blocks_found) == int(target_block_data["number"])):
                            return
            
            if block_id_in_flow not in visited:
                visited.add(block_id_in_flow)
                for neighbor in self.dependency_graph.adjacency_list[block_id_in_flow]:
                    dfs(visited, neighbor, allowed_block_data, target_block_data, blocks_found)

        def get_block_data_from_registry(block_data, block_id_in_flow):
            """
                Retrieves the Block Data from the registry given the block ID in the flow

                Attributes:
                block_data: Full JSON of Block Data from Front-End
                block_id_in_flow: The Block ID generated by the front-end when assembling a flow
            """
            # Block Data from Block Registry
            # TODO: Maybe this should be optimized since its querying the whole table
            block_registry_data = BlockRegistry.\
                objects.\
                all().\
                filter(block_type=block_data["data"]["metadata"]["blockType"]).\
                filter(block_id=block_data["data"]["metadata"]["blockId"])[0]

            return block_registry_data

        def make_run_request(block_id_in_flow, block_registry_data, input_payload, output_payload):
            """
                Makes a request against remote resources to complete the request

                Attributes:
                block_id_in_flow: The Block ID generated by the front-end when assembling a flow
                block_registry_data: Block Data queried from the front-end
                input_payload: JSON Payload of Form Inputs
                output_payload: JSON Payload of required information from previous steps
            """
            # Make a POST request to a run endpoint to run the block
            request_url = f"{env('API_BASE_URL')}/{block_registry_data.block_type}/{block_registry_data.block_id}/run"

            request_payload = {
                "input": input_payload,
                "output": output_payload,
            }

            r = requests.post(request_url, json=request_payload)
            
            output = {}
            if (r.status_code == 200):       
                # Updates the Block Outputs overall JSON
                block_type_id_key = f"{block_registry_data.block_type}-{block_registry_data.block_id}"
                if block_type_id_key not in output:
                    output[block_type_id_key] = {}

                try:
                    output[block_type_id_key][block_id_in_flow] = r.json()
                except json.decoder.JSONDecodeError as e:
                    print ("JSON Decode Error")
            else:
                logging.error(f"A Response {r.status_code} when querying URL {request_url} with payload {request_payload}")

            return output


        output_cache = {}
        def get_data_from_cache(block_id_in_flow):
            """
                Makes a request to the output cache to retrieve data

                Attributes:
                block_id_in_flow: The Block ID generated by the front-end when assembling a flow
            """
            block_data = get_block_by_id(block_id_in_flow)
            block_registry_data = get_block_data_from_registry(block_data, block_id_in_flow)

            cache_key = f"{block_registry_data.block_type}-{block_registry_data.block_id}"

            if cache_key in list(output_cache.keys()):
                return output_cache[cache_key]
            else:
                print ("Cache Key: ", cache_key)
                print ("Output Cache: ", output_cache.keys())
                raise f"Data does not exist in cache for {block_id_in_flow} with {cache_key}"
        
        # Main Running Code
        for task in self.batched_tasks:
            # Goes through a set of tasks. Each FOR loop should make a request
            # TODO: This part of the process can be asynchronous
            for task_to_be_run in task:
                # Gets the full sent data about the block
                block_data = get_block_by_id(task_to_be_run)
                block_registry_data = get_block_data_from_registry(block_data, task_to_be_run)
                
                # If the task has no dependencies, make the request immediately,
                # otherwise perform a DFS search to extract all related dependencies
                if (len(self.dependency_graph.adjacency_list[task_to_be_run]) == 0):
                    response = make_run_request(task_to_be_run, block_registry_data, block_data["data"]["input"], {})
                    
                    # Adds to a cache to ensure that requests don't need to be re-run
                    output_cache = {
                        **output_cache,
                        **response
                    }
                else:
                    # TODO: Implement DFS code to get the list of related objects

                    # The following variables are used in the DFS
                    
                    # Contains list of Block ID's from the flow that are dependencies 
                    # for running the block associated with the `task_to_be_run`
                    blocks_found = []
                    for required_block in block_registry_data.validations["required"]:
                        # Visited Set
                        visited = set()
                        
                        dfs(visited, task_to_be_run, block_registry_data.validations["allowed_blocks"], required_block, blocks_found)

                    print (f"Task {task_to_be_run} - {blocks_found}")

                    # Assembles all dependency data into the output_payload variable
                    output_payload = {}
                    for block_id in blocks_found:
                        response = get_data_from_cache(block_id)

                        output_payload = {
                            **output_payload,
                            **response
                        }
                    
                    response = make_run_request(task_to_be_run, block_registry_data, block_data["data"]["input"], output_payload)

                    print ("Response: ", response)
                    
                    # Adds to a cache to ensure that requests don't need to be re-run
                    output_cache = {
                        **output_cache,
                        **response
                    }

        return output_cache    

    # def run_batched_tasks_v2(self):
    #     # Retrieves a block from the vertices list by its ID
    #     def get_block_by_id(id):
    #         for vertex in self.vertices:
    #             if (vertex["id"] == id):
    #                 return vertex
        
    #     # Implements a DFS Search
    #     def dfs(visited, node, allowed_block_data, target_block_data, blocks_found):
    #         """
    #             Performs a recursive DFS to extrapolate the possible blocks in the sequence
    #             and attempt to match these blocks to the required_block_data and target_block_data

    #             Attributes:
    #             visited: A set of all nodes that have been viewed in the DFS
    #             node: The current node in the iteration being searched
    #             allowed_block_data: Array of JSON objects representing {"blockType": "", "blockId": ""}
    #             target_block_data: Tuple representing {"blockType": "", "number": ""}
    #         """
    #         # print ("Searching Node: ", node)
    #         # print ()
    #         # print ()

    #         block = get_block_by_id(node)
            
    #         # Ensures search is not run on the source node
    #         if (len(visited) > 0):
    #             if (block["data"]["metadata"]["blockType"] == target_block_data["blockType"]):
    #                 for allowed_block in allowed_block_data:
    #                     # print ("Block ID Being Searched: ", block["data"]["metadata"]["blockId"])
    #                     # print ("Block Type Being Searched: ", block["data"]["metadata"]["blockType"])
    #                     # print ("Allowed Block: ", allowed_block)
                        
    #                     if (str(block["data"]["metadata"]["blockId"]) == str(allowed_block["blockId"])
    #                         and block["data"]["metadata"]["blockType"] == allowed_block["blockType"]):
                            
    #                         # print ("Match!")

    #                         blocks_found.append(node)

    #                         # print ("Blocks Found: ", blocks_found)
    #                         # print ("Length of Blocks Found: ", len(blocks_found))
    #                         # print ("Target Block Data: ", target_block_data)

    #                         if (len(blocks_found) == int(target_block_data["number"])):
    #                             # print ("Returning")
    #                             return blocks_found
                
    #         if node not in visited:
    #             visited.add(node)
    #             for neighbor in self.dependency_graph.adjacency_list[node]:
    #                 dfs(visited, neighbor, allowed_block_data, target_block_data, blocks_found)
    #         # else:
    #         #     print ("Not iterating further for visited list ", visited, " and node ", node)
        
    #     for task in self.batched_tasks:
    #         for item in task:
    #             # Retrieves all block data from its ID
    #             block = get_block_by_id(item)

    #             # Block ID From React Library
    #             block_id_in_flow = block["id"]

    #             # Block ID in Block Registry
    #             block_id = block["data"]["metadata"]["blockId"]
    #             # Block Type from Block Registry
    #             block_type = block["data"]["metadata"]["blockType"]

    #             # Query the database to get all metadata pertaining to the block
    #             block_registry = BlockRegistry.objects.all().filter(block_type=block_type).filter(block_id=block_id)[0]

    #             # Amount of block data extracted
    #             i = 0
    #             for required_block in block_registry.validations["required"]:
    #                 # Visited Set
    #                 visited = set()

    #                 blocks_found = []
    #                 # Runs DFS
    #                 # TODO: Search by Block Type and ID through the DFS and get the block_id_in_flow
    #                 dfs(visited, block_id_in_flow, block_registry.validations["allowed_blocks"], required_block, blocks_found)

    #                 # print ("Found Matching Data for ", target_block_data, "which is block_id_in_flow", node)
    #                 print ("Ran DFS For Block ID: ", block_id_in_flow)                    
    #                 print ("Blocks Found: ", blocks_found)
    #                 print ()

    # def run_batched_tasks(self):
    #     """
    #         Takes a list of Batched Tasks and runs a flow
    #     """
    #     overall_outputs = {}

    #     def get_block_by_id(id):
    #         for vertex in self.vertices:
    #             if (vertex["id"] == id):
    #                 return vertex

    #     def traverse_dependency_graph(block_id):
    #         pass
        
    #     def make_run_request(block_id_in_flow, block_id, block_type, payload):
    #         """
    #             Makes request to block's service and forms the outputs JSON block

    #             Attributes:
    #             block_id_in_flow: ID of block provided from UI
    #             block_id: ID of block in block registry
    #             block_type: Type of block in block registry
    #             payload: Input payload passed in from front-end 
    #         """
    #         # Query the database to get the base URL of the block
    #         block_registry = BlockRegistry.objects.all().filter(block_type=block_type).filter(block_id=block_id)[0]

    #         # Make a POST request to a run endpoint to run the block
    #         request_url = f"{env('API_BASE_URL')}/{block_registry.block_type}/{block_registry.block_id}/run"

    #         # TODO: How do we tell the blocks that they are connected to other blocks? 
    #         #       We have the ability to get the **direct** dependencies associated with a connection to a block, but not the inherited dependencies
    #         #       How could we use the validations column in the block_register and combine this with some kind of iteration to generate
    #         #       a more custom suited payload?
    #         for required_block in block_registry.validations["required"]:
    #             # Have the specific block, now need to search for it
    #             # TODO: Recursively iterate through the flow to get the id of the block associated with the data

    #         # dependencies = self.dependency_graph.adjacency_list[block_id_in_flow]
    #         print ("Dependencies: ", dependencies)

    #         request_payload = {
    #             "input": payload,
    #             "output": overall_outputs
    #         }

    #         r = requests.post(request_url, json=request_payload)

    #         if (r.status_code == 200):       
    #             # Updates the Block Outputs overall JSON
    #             block_type_id_key = f"{block_type}-{block_id}"
    #             if block_type_id_key not in overall_outputs:
    #                 overall_outputs[block_type_id_key] = {}
                
    #             try:
    #                 overall_outputs[block_type_id_key][block_id_in_flow] = r.json()
    #             except json.decoder.JSONDecodeError as e:
    #                 pass
    #                 # print ("Json Decode Error Response: ", r.text)
    #         else:
    #             pass
    #             # logging.error(f"A Response {r.status_code} when querying URL {request_url} with payload {request_payload}")

    #     for task in self.batched_tasks:
    #         for item in task:
    #             block = get_block_by_id(item)

    #             block_id_in_flow = block["id"]
    #             block_id = block["data"]["metadata"]["blockId"]
    #             block_type = block["data"]["metadata"]["blockType"]

    #             make_run_request(block_id_in_flow, block_id, block_type, block["data"]["input"])
    
    #     # print ("Outputs: ", overall_outputs)
    #     return overall_outputs