import checks
import errors

class Node():
    # Node types: normal, if, elif, else, def, for, while
    def __init__(self, code, node_type = 'normal', conditions_to_reach = [], node_id = 0):
        self.id = node_id
        self.code = code
        self.node_type = node_type
        self.sources = []    # Since that this is a graph (not a tree) so a node can have more than one source.
        self.conditions_to_reach = conditions_to_reach
        self.children = dict()  # contains {Node: Edge}

    def __str__(self):
        return str(self.id) + ": " + self.code
        # return str(self.id) + ": " + self.code + " | Type: " + self.node_type + " | CTR: " + str(self.conditions_to_reach)

    def extract_condition(self, edge):
        """
        Extracts the condition of the if, elif, for or while lines.
        """
        x = self.conditions_to_reach.copy()
        if self.node_type in ['for', 'while', 'if', 'elif']:
            x.append(f'{str(edge)[0]} - {self.id}: ' + self.code[len(self.node_type)+1:-1])
        return x
    
    def findCommonConditions(self, condition1):
        new = []
        for i in range(min(len(condition1), len(self.conditions_to_reach))):
            if condition1[i] == self.conditions_to_reach[i]:
                new.append(condition1[i])
            else: break
        return new

    def addNodeChild(self, child_node, edge, called_from_add_child = False):
        """
        Used to add a node as a child to another node instead of creating a new node.
        """
        if child_node in self.children: return child_node
        self.children[child_node] = edge
        child_node.sources.append(self)
        # print(self.conditions_to_reach, child_node.conditions_to_reach)
        if len(self.conditions_to_reach) < len(child_node.conditions_to_reach) and not called_from_add_child:
            child_node.conditions_to_reach = self.conditions_to_reach.copy()
            # print("REDUCING", child_node.code, child_node.node_type, self.node_type)
            if child_node.node_type in ['elif', 'else'] and self.node_type in ['if', 'elif']:
                child_node.conditions_to_reach.append(f'{str(edge)[0]}{self.id}: ' + self.code[len(self.node_type)+1:-1])
        elif not called_from_add_child:
            child_node.conditions_to_reach = self.findCommonConditions(child_node.conditions_to_reach)
            # print("REDUCING", child_node.code)

        return child_node
    
    def addChild(self, child, node_type, edge, node_id):
        """
        Creates a new node and adds it as a child for this node.
        """
        child_node = Node(child, node_type, self.extract_condition(edge), node_id=node_id)
        return self.addNodeChild(child_node, edge, True)

class Edge:
    """
    Represents the edge between 2 nodes in the graph.
    self.edge values: None, True, False
    If the edge is directed from a normal typed node, edge is None.
    If it is directed from if, elif, for or while, then it is either True or False.
    """
    def __init__(self, edge, visited = 0):
        self.edge = edge
        self.visited = visited
    
    def __str__(self) -> str:
        return str(self.edge)
    
class Func:
    def __init__(self, scope, cfg):
        self.scope = scope
        self.cfg = cfg

class CFG():
    """
    Represents a control flow graph.
    """
    def __init__(self, code, indentation, parent = None, debug = False):
        self.parent = parent
        self.debug = debug
        self.root = Node('Start', node_id = 0)
        self.size = 1
        self.indentation = indentation  # What indentation is used in the code
        self.constructed = False    # indicates whether construct_graph was called on this graph or not
        self.code_lines = code.split('\n')
        self.code_lines.append('End')
        self.defs = dict()
        self.child_graphs = dict()  # contains graphs of all functions defined in the code.
                                    # if this graph contains a function, it may have another functions defined
                                    # in it, so they will also be child graphs for this function graph.

    def printCFG(self):
        if not self.constructed: return
        queue = []
        current = self.root
        visited_set_to = list(current.children.values())[0].visited
        queue.append(current)
        while len(queue) > 0:
            current = queue.pop(0)
            print(current, f" | Parents: {[i.id for i in current.sources]}")
            for i in current.children.keys():
                if current.children[i].visited == visited_set_to:
                    current.children[i].visited += 1
                    current.children[i].visited %= 2
                    queue.append(i)

    def extractAllDefs(self):
        current_indent = 0  # How much is the previous line indented. (number of tabs)
        def_code = None     # The code in the defined function
        def_name = None     # The function's name
        in_def = [False, None]  # If we are currently in a function and how much is it indented.
        to_remove = list()      # We add lines in the function to this list to be removed from the code.

        for line in self.code_lines:
            if checks.checkUnwantedLine(line): continue

            line_indent = (len(line) - len(line.lstrip())) // self.indentation
            if line_indent < current_indent:    # if we get out of def block
                new_cfg = CFG(def_code[:-1], self.indentation, self, debug=self.debug)
                self.child_graphs[def_name.split('(')[0]] = [new_cfg, def_name.split('(')[1][:-1], False]   # Add function graph to the children of this graph.
                current_indent = line_indent
                in_def = [False, None]
            
            if line.strip()[:4] == 'def ' and not in_def[0]:
                current_indent = line_indent + 1
                in_def = [True, len(line) - len(line.lstrip())]
                def_name = line.strip()[4:-1]
                if checks.checkReservedKeyword(def_name.split('(')[0]):
                    raise errors.InvalidUseOfReservedKeywordException(f"Cannot use {def_name.split('(')[0]} as function name.")
                def_code = ''
            elif not in_def[0]: continue
            else:
                def_code += line[in_def[1] + self.indentation:] + '\n'
                to_remove.append(line)
        
        for i in to_remove:
            self.code_lines.remove(i)
        return len(self.child_graphs)

    def construct_graph(self):
        if self.debug: print(self.root.code, '\t\t', self.root.node_type)
        self.extractAllDefs()
        self.constructed = True
        if self.parent is not None: self.defs.update(self.parent.defs)
        current = self.root     # Current node pointer
        indents = dict()        # Dictionary of the lines that causes indentation
        the_if_list = []        # List of nodes containing if and elif statements
        current_indent = 0      # How much is the current block indented. (number of tabs)
        prev_line_indent = 0    # How much is the previous line indented. (number of tabs).
        last = dict()       # contains nodes from if or elif blocks that are waiting for the elif or else
                            # blocks to be closed so they can point to the following line
        added_indent = 0        # if 1 this indicates a new indentation has happened,
                                # if -1 this indicates an indentation was closed
        returns = []

        for line in self.code_lines:
            if checks.checkUnwantedLine(line): continue

            common_child = None     # If a node was created but is going to be added to the children list of
                                    # more than one node, we save it to not create it again

            # Determine the node type to insert this line into
            if line.strip()[:4] == 'for ':
                n_type = 'for'
            elif line.strip()[:4] == 'def ':
                n_type = 'def'
                def_indent = len(line) - len(line.lstrip())
                line = ' ' * def_indent + line.strip()[4:-1]
            elif line.strip()[:3] == 'if ':
                n_type = 'if'
            elif line.strip()[:5] == 'elif ':
                n_type = 'elif'
            elif line.strip()[:5] == 'else:':
                n_type = 'else'
            elif line.strip()[:6] == 'while ':
                n_type = 'while'
            else:
                n_type = 'normal'
            
            # If the user initialized a block with anything other than (if, elif, else, while, for, def)
            if line[-1] == ':' and n_type == 'normal':
                x = line.split(' ')[0]
                err = f'Invalid block intializer: "{x}".'
                for i in ['for', 'while', 'if', 'elif', 'else', 'def']:
                    if line.startswith(i):
                        err += '\nDid you mean: "' + i + ' ' + line[len(i):] + '" ?'
                raise errors.InValidBlockException(err)
            
            # How much is the current line indented. (number of tabs)
            line_indent = (len(line) - len(line.lstrip())) // self.indentation
            return_continue_flag = False

            # if this line indentation is less than the previous line indentation
            # used when a block or more are closed to correctly put edges between nodes
            # READ this block after you read the rest of the code to UNDERSTAND IT.
            if line_indent < current_indent:
                if current.node_type in ['for', 'while', 'if', 'elif', 'else']:
                    raise IndentationError(f'"{line}" is not properly indented after "{current.code}"')
                return_continue_flag = True
                different_indent = current_indent - line_indent     # How many blocks were closed
                for i in range(different_indent):   # For each block that was closed
                    # indents[current_indent - i]: most recent block
                    if indents[current_indent - i].node_type == 'else':
                        the_if_list.append((indents.pop(current_indent - i), current_indent - i))
                    elif indents[current_indent - i].node_type in ['for', 'while']:
                        if current.code[:7] != 'return ' and current.code != 'return':
                            current.addNodeChild(indents[current_indent - i], Edge(False))
                        else: returns.append(current)
                        # If there were "if" indentations that are closed in the same line with the while
                        # or for loops, so they should point back to the loop statement.
                        for j in range(len(the_if_list)):
                            if the_if_list[j][0].node_type != 'else':
                                the_if_list[j][0].addNodeChild(indents[current_indent - i], Edge(False))
                        the_if_list = []
                        current = indents.pop(current_indent - i)
                    else:
                        if len(the_if_list) != 0:
                            # we don't want else statements in the_if_list because they always point to the next line
                            if the_if_list[-1][0].node_type == 'else': the_if_list.pop(-1)
                        the_if_list.append((indents.pop(current_indent - i), current_indent - i))
                if n_type == 'elif' or n_type == 'else':
                    # if the line that gets us out of an if or elif blocks is an elif or an else, we don't want
                    # the last line in the if or elif blocks to point at it, so we save it in last list.
                    if last.get(line_indent) is None:
                        last[line_indent] = []
                    if current.code[:7] != 'return ' and current.code not in ['continue', 'break', 'return']:
                        last[line_indent].append(current)
                        x = line_indent + 1
                        while last.get(x) is not None:
                            for i in last.pop(x):
                                last[line_indent].append(i)
                            x += 1
                    if len(the_if_list) > 1:
                        for i in the_if_list[:-1]:
                            last[line_indent].append(i[0])
                            x = line_indent + 1
                            while last.get(x) is not None:
                                for j in last.pop(x):
                                    last[line_indent].append(j)
                                x += 1
                        the_if_list = the_if_list[-1:]                        
                elif len([i for i in last.keys() if i >= line_indent]) != 0:
                    lasts = [last[i] for i in last.keys() if i >= line_indent]
                    lasts2 = []
                    for i in lasts:
                        lasts2.extend(i)
                    
                    if the_if_list:
                        if the_if_list[-1][0].node_type == 'else': the_if_list.pop(-1)

                    if current.node_type in ['for', 'while']: common_child = current
                    for i in lasts2:
                        if common_child is None:
                            common_child = i.addChild(line.strip(), n_type, Edge(None), node_id = self.size)
                            self.size += 1
                        else: i.addNodeChild(common_child, Edge(None))
                    if current.node_type in ['for', 'while']: common_child = None
                    
                added_indent = -1   # Since an indentation block was closed
                current_indent -= different_indent
            elif line_indent != prev_line_indent and current.node_type not in ['for', 'while', 'if', 'elif', 'else']:
                raise IndentationError(f'Line "{line}" not indented properly.')

            # Determine edge type
            if current.node_type in ['normal', 'def']:
                edge = Edge(None)
            elif current.node_type in ['for', 'while', 'if', 'elif']:
                # A node can have 2 children, one if the condition is true and other if false.
                # We traverse the true path first, so that's why when added_indent is 1, edge is true edge
                if added_indent > 0: edge = Edge(True)
                elif added_indent < 0: edge = Edge(False)

            for i in range(len(the_if_list)):
                if common_child is None:
                    common_child = the_if_list[i][0].addChild(line.strip(), n_type, Edge(False), node_id = self.size)
                    self.size += 1
                else: the_if_list[i][0].addNodeChild(common_child, Edge(False))
            the_if_list.clear()

            if self.debug: print(line, '\t\t', n_type)
            if (current.code[:7] == 'return ' or current.code in ['continue', 'break', 'return']) and return_continue_flag:
                current = common_child
            elif n_type in ['for', 'while', 'if', 'elif', 'else']:
                current_indent += 1     # We entered a new block
                added_indent = 1        # and therefore added indentation
            
                # We add the indentation of this block as a key to the indents dictionary, with a value of
                # node containing the line that caused the indentation (for, while, if or elif)
                if common_child is None:
                    indents[current_indent] = current.addChild(line.strip(), n_type, edge, node_id = self.size)
                    self.size += 1
                else:
                    if last.get(line_indent) is not None:
                        indents[current_indent] = common_child
                    else: indents[current_indent] = current.addNodeChild(common_child, edge)
                current = indents[current_indent]   # Let the current pointer point to the newly added node
            else:
                # Add this line as a child to the current node and set the pointer to point at the newly added node
                # If the node already exists, use it instead of making a new one.
                if common_child is None:
                    current = current.addChild(line.strip(), n_type, edge, node_id = self.size)
                    self.size += 1
                else:
                    current = current.addNodeChild(common_child, edge)
            
            prev_line_indent = line_indent
            if current.node_type in ['elif', 'else'] and not [1 for i in current.sources if i.node_type in ['elif', 'if']]:
                raise errors.InValidBlockException(f'Cannot use {current.node_type} statement without an if statement.')
        for i in returns:
            i.addNodeChild(current, Edge(None))