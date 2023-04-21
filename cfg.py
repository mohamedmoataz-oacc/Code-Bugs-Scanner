class Node():
    # Node types: normal, if, def, for, while
    def __init__(self, code, node_type = 'normal', condition_to_reach = None, parent = None):
        self.code = code
        self.node_type = node_type
        self.parent = parent
        self.condition_to_reach = condition_to_reach
        self.children = dict()  # contains {Node: Edge}

    def __str__(self):
        return self.code + " | Type: " + self.node_type + " | CTR: " + str(self.condition_to_reach)

    def extract_condition(self):
        if self.node_type not in ['for', 'while', 'if']:
            return
        else:
            return self.code[len(self.node_type)+1:-1]

    def addNodeChild(self, child_node, edge):
        if child_node in self.children: return
        self.children[child_node] = edge
        return child_node
    
    def addChild(self, child, node_type, edge):
        child_node = Node(child, node_type, self.extract_condition(), self)
        return self.addNodeChild(child_node, edge)

class Edge:
    def __init__(self, edge, visited = False):
        self.edge = edge
        self.visited = visited

class CFG():
    def __init__(self, code, indentation):
        self.root = Node('Start')
        self.size = 1
        self.indentation = indentation
        self.code_lines = code.split('\n')
        self.code_lines.append('End')
        # self.child_graphs = dict()

    def printCFG(self):
        queue = []
        current = self.root
        queue.append(current)
        while len(queue) > 0:
            x = queue.pop(0)
            try: print(x, f" | P: {x.parent.code}")
            except AttributeError: print(x, f" | P: None")
            for i in x.children:
                queue.append(i)

    def construct_graph(self):
        current = self.root     # Current node pointer
        indents = dict()        # Dictionary of the lines that causes indentation
        the_if_list = []        # List of nodes containing if and elif statements
        current_indent = 0      # How much is the current line indented. (number of tabs)

        added_indent = 0        # if 1 this indicates a new indentation has happened,
                                # if -1 this indicates an indentation was closed

        for line in self.code_lines:
            if len(line.strip()) == 0: continue # If the line was empty

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
            
            if line_indent < current_indent:
                different_indent = current_indent - line_indent
                # print('m: ', different_indent, current_indent, line_indent)
                for i in range(different_indent):
                    print(current_indent, i, {i:j.code for i,j in indents.items()})
                    if indents[current_indent - i].node_type in ['for', 'while']:
                        current.addNodeChild(indents[current_indent - i], False)
                        for i in the_if_list:
                            i.addNodeChild(indents[current_indent - i], False)
                        current = indents.pop(current_indent - i)
                    else:
                        if i == different_indent - 1:
                            indents.pop(current_indent - i).addChild(line.strip(), n_type, False)
                        else:
                            the_if_list.append(indents[current_indent - i])
                added_indent = -1
                # print('c-d: ', current_indent - different_indent)
                current_indent -= different_indent

            # Determine edge type
            if current.node_type == 'normal':
                edge = Edge(None)
            elif current.node_type in ['for', 'while', 'if', 'elif']:
                if added_indent > 0: edge = Edge(True)
                elif added_indent < 0: edge = Edge(False)


            if n_type in ['for', 'while']:
                current_indent += 1
                added_indent = 1
                indents[current_indent] = current.addChild(line.strip(), n_type, edge)
                current = indents[current_indent]
            elif n_type in ['if', 'elif']:
                current_indent += 1
                added_indent = 1
                indents[current_indent] = current.addChild(line.strip(), n_type, edge)
                for i in the_if_list:
                    i.addNodeChild(indents[current_indent], False)
                current = indents[current_indent]
            elif n_type == 'def':
                pass
            else:
                current = current.addChild(line.strip(), n_type, edge)
            

            
                    