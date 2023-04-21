class Node():
    # Node types: normal, if, def, for, while
    def __init__(self, code, node_type = 'normal', condition_to_reach = None):
        self.code = code
        self.node_type = node_type
        self.parent = []
        self.condition_to_reach = condition_to_reach
        self.children = dict()  # contains {Node: Edge}

    def __str__(self):
        result = self.code + " | Type: " + self.node_type + " | CTR: " + str(self.condition_to_reach)
        if self.parent: x = self.parent[0].children[self].edge
        else: x = None
        if x is not None:
            result += f" ({x})"
        return result

    def extract_condition(self):
        if self.node_type not in ['for', 'while', 'if']:
            return
        else:
            return self.code[len(self.node_type)+1:-1]

    def addNodeChild(self, child_node, edge):
        if child_node in self.children: return
        self.children[child_node] = edge
        child_node.parent.append(self)
        return child_node
    
    def addChild(self, child, node_type, edge):
        child_node = Node(child, node_type, self.extract_condition())
        return self.addNodeChild(child_node, edge)

class Edge:
    def __init__(self, edge, visited = False):
        self.edge = edge
        self.visited = visited
    
    def __str__(self) -> str:
        return f"Visited: {self.visited}"

class CFG():
    def __init__(self, code, indentation):
        self.root = Node('Start')
        self.size = 1
        self.indentation = indentation
        self.code_lines = code.split('\n')
        self.code_lines.append('End')
        # self.child_graphs = dict()    # will use it when implementing def blocks
        self.construct_graph()

    def printCFG(self):
        queue = []
        current = self.root
        queue.append(current)
        while len(queue) > 0:
            x = queue.pop(0)
            try: print(x, f" | P: {[i.code for i in x.parent]}")
            except AttributeError: print(x, f" | P: None")
            for i in x.children.keys():
                if not x.children[i].visited:
                    x.children[i].visited = True
                    queue.append(i)

    def construct_graph(self):
        current = self.root     # Current node pointer
        indents = dict()        # Dictionary of the lines that causes indentation
        the_if_list = []        # List of nodes containing if and elif statements
        current_indent = 0      # How much is the previous line indented. (number of tabs)

        added_indent = 0        # if 1 this indicates a new indentation has happened,
                                # if -1 this indicates an indentation was closed

        for line in self.code_lines:
            if len(line.strip()) == 0: continue # If the line was empty
            # If line is a string that is not used.
            elif ((line.strip().startswith("'") and line.strip().endswith("'")) or 
                  (line.strip().startswith('"') and line.strip().endswith('"'))): continue

            loop_node = None    # A pointer to the new node created in this loop so that if multiple edges
                                # point to it, we don't create multiple nodes.

            # Determine the node type to insert this line into
            if line.strip()[:3] == 'for':
                n_type = 'for'
            elif line.strip()[:2] == 'if':
                n_type = 'if'
            elif line.strip()[:4] == 'elif':
                n_type = 'elif'
            elif line.strip()[:5] == 'while':
                n_type = 'while'
            elif line.strip()[:3] == 'def':
                n_type = 'def'
            else:
                n_type = 'normal'
            
            # How much is the current line indented. (number of tabs)
            line_indent = (len(line) - len(line.lstrip())) // self.indentation

            # if this line indentation is less than the previous line indentation
            # used when a block or more are closed to correctly put edges between nodes
            # READ this block after you read the rest of the code to UNDERSTAND IT.
            if line_indent < current_indent:
                different_indent = current_indent - line_indent     # How many blockes were closed
                for i in range(different_indent):   # For each block that was closed
                    # indents[current_indent - i]: most recent block
                    if indents[current_indent - i].node_type in ['for', 'while']:
                        current.addNodeChild(indents[current_indent - i], Edge(False))
                        # If there were "if" indentations that are closed in the same line with the while
                        # or for loops, so they should point back to the loop statement.
                        for i in range(len(the_if_list)):
                            the_if_list.pop(i).addNodeChild(indents[current_indent - i], Edge(False))
                        current = indents.pop(current_indent - i)
                    else:
                        if i == different_indent - 1: # If the first indentation block was if or elif statement
                            # Make new child node to the if statement for the false branch.
                            loop_node = indents.pop(current_indent - i).addChild(line.strip(), n_type, Edge(False))
                        else:
                            # If the if statement wasn't the first indentation block
                            the_if_list.append(indents[current_indent - i])
                added_indent = -1   # Since an indentation block was closed
                current_indent -= different_indent

            # Determine edge type
            if current.node_type == 'normal':
                edge = Edge(None)
            elif current.node_type in ['for', 'while', 'if', 'elif']:
                # A node can have 2 children, one if the condition is true and other if false.
                # We traverse the true path first, so that's why when added_indent is 1, edge is true edge
                if added_indent > 0: edge = Edge(True)
                elif added_indent < 0: edge = Edge(False)


            if n_type in ['for', 'while', 'if', 'elif']:
                current_indent += 1     # We entered a new block
                added_indent = 1        # and therefore added indentation
                # We add the indentation of this block as a key to the indents dictionary, with a value of
                # node containing the line that caused the indentation (for, while, if or elif)
                if loop_node is not None: indents[current_indent] = current.addNodeChild(loop_node, edge)
                else: indents[current_indent] = current.addChild(line.strip(), n_type, edge)
                self.size += 1
                if n_type in ['if', 'elif']:
                    # Since that the loops point back to their start when they end but the if statement
                    # doesn't, so we need a "if list" containing the "if" and "elif" nodes to add the new
                    # node to them.
                    for i in range(len(the_if_list)):
                            the_if_list.pop(i).addNodeChild(indents[current_indent], Edge(False))
                current = indents[current_indent]   # Let the current pointer point to the newly added node
            elif n_type == 'def':
                pass
            else:
                # Add this line as a child to the current node and set the pointer to point at the newly added node
                # If the node already exists, use it instead of making a new one.
                if loop_node is not None: current = current.addNodeChild(loop_node, edge)
                else: current = current.addChild(line.strip(), n_type, edge)
                self.size += 1