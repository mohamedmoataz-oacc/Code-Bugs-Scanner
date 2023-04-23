from cfg import CFG

def detect_infinite_loops(cfg:CFG) -> list:
    """Detects infinite loops in the CFG and returns a list of nodes that are part of the loop."""
    if not cfg.constructed:
        return []

    # Initialize visited set and stack with root node
    visited = set()
    stack = [cfg.root]
    loop_nodes = set()

    while stack:
        node = stack.pop()
        visited.add(node)

        # Loop through children of current node
        for child_node in node.children.items():
             # Check if child has been visited before
            if child_node in visited:
                # Check if child has multiple parents (loop detected)
                if child_node in stack:
                    loop_nodes.add(child_node)
            else:
                # Add child to stack
                stack.append(child_node)

    # Return list of nodes that are part of the loop
    return list(loop_nodes)


if __name__ == '__main__':
    with open('buggy.py', 'r') as code_file:
        cg = CFG(code_file.read(), 4)
        cg.construct_graph()
        loopnodes=detect_infinite_loops(cg)
        if loopnodes:
            print("infinite loop detected")
            for node in loopnodes:
                print(node)
        else:
            print("no detected loop found")