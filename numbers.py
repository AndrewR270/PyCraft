# Contains values for constructing block models.

# Contains coordinates for block vertices.
vertex_positions = [
    #|   TOP LEFT    |   BOTTOM LEFT   |   BOTTOM RIGHT  |   TOP RIGHT   |  
    #| x1   y1   z1  |  x2    y2   z2  |  x3    y3   z3  |  x4   y4   z4 |  
	 0.5,  0.5,  0.5,  0.5, -0.5,  0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5, # right face
	-0.5,  0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, # left face
	-0.5,  0.5,  0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5, # top face
	-0.5, -0.5,  0.5, -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,  0.5, -0.5,  0.5, # bottom face
	-0.5,  0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  0.5, # front face
	 0.5,  0.5, -0.5,  0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5, # back face
]

# Default texture coordinates for a block with the same texture on each face.
tex_coords = [
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
]

# Indexes of draw vertices.
indices = [
    #TRIANGLE1 | TRIANGLE2|
    #TL,BL,BR, | TL,BR,TR |
	 0,  1,  2,  0,  2,  3, # right face
	 4,  5,  6,  4,  6,  7, # left face
	 8,  9, 10,  8, 10, 11, # top face
	12, 13, 14, 12, 14, 15, # bottom face
	16, 17, 18, 16, 18, 19, # front face
	20, 21, 22, 20, 22, 23, # back face
]