margin = (20, 30)
node_dim = (30, 20)

def calculate_pos(node, offset=(0,0)):
    if len(node.children) == 0:
        node.pos = offset
        return node_dim[0]

    current_pos = (offset[0], offset[1] + margin[1])
    node.pos = (0, 0)
    for child in node.children:
        width = calculate_pos(child, current_pos)
        current_pos = (current_pos[0] + width + margin[0], current_pos[1])
        node.pos = (node.pos[0] + child.pos[0], 0)

    node.pos = (node.pos[0]/len(node.children), offset[1])

    return current_pos[0] - margin[0]

def tikz(tree):
    nodes = r"\node[draw, fill=white] at ({}, {}) ".format(tree.pos[0], -tree.pos[1]) + "{" + str(tree.symb) + "};\n"
    lines = ""
    for child in tree.children:
        lines += r"\draw ({}, {}) -- ({}, {});".format(tree.pos[0], -tree.pos[1], child.pos[0], -child.pos[1]) + "\n"
        l, n = tikz(child)
        lines += l
        nodes += n

    return lines, nodes

def draw(tree):
    calculate_pos(tree)
    lines, nodes = tikz(tree)
    with open("drawing.txt", "w") as file:
        file.write(lines)
        file.write(nodes)