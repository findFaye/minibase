# common_db.py

BLOCK_SIZE = 4096

global_lexer = None
global_parser = None
global_syn_tree = None
global_logical_tree = None

class Node:
    def __init__(self, value, children=None, varList=None):
        self.value = value
        self.var = varList
        self.children = children if children else []

def show(node, indent=0):
    prefix = " " * indent
    if isinstance(node, Node):
        print(f"{prefix}{node.value}")
        if node.var:
            print(f"{prefix}var: {node.var}")
        for child in node.children:
            show(child, indent + 2)
    else:
        print(f"{prefix}{node}")
