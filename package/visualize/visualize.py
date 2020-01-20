from PIL import Image, ImageDraw

padding = (50, 50)
margin = (50, 50)
node_dim = (50, 20)

def calculate_pos(node, offset=(0,0)):
    if len(node.children) == 0:
        node.pos = offset
        return node_dim

    current_pos = (offset[0], offset[1] + margin[1] + node_dim[1])
    node.pos = (0, 0)
    height = 0
    for child in node.children:
        width, h = calculate_pos(child, current_pos)

        height = max(h, height)
        current_pos = (current_pos[0] + width + margin[0], current_pos[1])
        node.pos = (node.pos[0] + child.pos[0], 0)

    node.pos = (node.pos[0]/len(node.children), offset[1])

    return current_pos[0] - margin[0] - offset[0], node_dim[1] + margin[1] + height

def make_shapes(tree, draw):
    for child in tree.children:
        draw.line(tree.pos + child.pos, fill=0)
        make_shapes(child, draw)

    draw.ellipse((tree.pos[0]-node_dim[0]//2, tree.pos[1]-node_dim[1]//2,
                  tree.pos[0]+node_dim[0]//2, tree.pos[1]+node_dim[1]//2), fill=1, outline=0)
    draw.text((tree.pos[0]-3, tree.pos[1]-6), tree.symb, fill=0)

def draw(tree):
    width, height = calculate_pos(tree, padding)

    im = Image.new("1", (width+padding[0], height+2*padding[1]), 1)
    draw = ImageDraw.Draw(im)
    make_shapes(tree, draw)
    del draw

    im.save("drawing.png")