# Queries
def get_output_interface_from_block_mapping(*_, nodeList, edgeList):
    """
    Resolve a mapping mapping from nodes and edges for output_interface data

    Arguments
    ---
    nodeList: Dict of nodes
    edgeList: List of edge mappings

    Example
    ---
    {
        [target_block_id]: [output_interface_value]
    }
    """
    flow = SpectrumEventFlow(nodeList, edgeList)

    pass
