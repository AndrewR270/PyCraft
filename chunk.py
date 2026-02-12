import ctypes
import pyglet.gl as gl

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
CHUNK_LENGTH = 16

class Chunk:

    def __init__(self, world, chunk_position):

        self.chunk_position = chunk_position

        self.position = (
            self.chunk_position[0] * CHUNK_WIDTH,
            self.chunk_position[1] * CHUNK_HEIGHT,
            self.chunk_position[2] * CHUNK_LENGTH
        )

        self.world = world

        self.blocks = [[[0 # block number
            for z in range (CHUNK_LENGTH)]
            for y in range (CHUNK_HEIGHT)]
            for x in range (CHUNK_WIDTH)]
        

        #--- MEMORY OBJECT DATA ARRAYS ------------------------------

        self.has_mesh = False
        self.mesh_vertex_positions = []
        self.mesh_index_counter = 0
        self.mesh_indices = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []
        
        #### allocate memory ########################################

        #--- VERTEX ARRAY OBJECT (VAO) ------------------------------
 
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        #--- VERTEX POSITIONS (VBO) ---------------------------------

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vertex_position_vbo))

        #--- TEXTURE COORDINATES (VBO) ------------------------------

        self.tex_coords_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.tex_coords_vbo))
        
        #--- SHADING VALUES (VBO) -----------------------------------

        self.shading_values_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.shading_values_vbo))

        #--- INDEX BUFFER OBJECT (IBO) ------------------------------

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)


    def update_mesh(self):
        self.has_mesh = True
        self.mesh_vertex_positions = []
        self.mesh_index_counter = 0
        self.mesh_indices = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []

        def add_face(face):
            # update vertices
            vertex_positions = block.vertex_positions[face].copy()
            for i in range(4):
                vertex_positions[i * 3 + 0] += x
                vertex_positions[i * 3 + 1] += y
                vertex_positions[i * 3 + 2] += z

            self.mesh_vertex_positions.extend(vertex_positions)

            # update indices
            indices = [0, 1, 2, 0, 2, 3]
            for i in range(6):
                indices[i] += self.mesh_index_counter

            self.mesh_indices.extend(indices)
            self.mesh_index_counter += 4
                        
            # add texture coordinates and shading values unchanged
            self.mesh_tex_coords.extend(block.tex_coords[face])
            self.mesh_shading_values.extend(block.shading_values[face])


        # loop through each block position in chunk
        for local_x in range(CHUNK_WIDTH):
            for local_y in range(CHUNK_HEIGHT):
                for local_z in range(CHUNK_LENGTH):

                    block_number = self.blocks[local_x][local_y][local_z]

                    # update array if block is not empty
                    if block_number:

                        block = self.world.block_types[block_number]

                        x,y,z = (
                            self.position[0] + local_x,
                            self.position[1] + local_y,
                            self.position[2] + local_z,
                        )

                        if not self.world.get_block_number((x+1, y, z)): add_face(0) # draw right face
                        if not self.world.get_block_number((x-1, y, z)): add_face(1) # draw left face
                        if not self.world.get_block_number((x, y+1, z)): add_face(2) # draw top face
                        if not self.world.get_block_number((x, y-1, z)): add_face(3) # draw bottom face
                        if not self.world.get_block_number((x, y, z+1)): add_face(4) # draw front face
                        if not self.world.get_block_number((x, y, z-1)): add_face(5) # draw back face

        #### pash mesh data to gpu ##################################

        if not self.mesh_index_counter:
            return

        #--- VERTEX ARRAY OBJECT (VAO) ------------------------------

        gl.glBindVertexArray(self.vao)

        #--- VERTEX POSITIONS (VBO) ---------------------------------

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.mesh_vertex_positions)), # size
            (gl.GLfloat * len(self.mesh_vertex_positions)) (*self.mesh_vertex_positions), # data
            gl.GL_STATIC_DRAW # usage
        )

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0) # array of generic vertex data
        gl.glEnableVertexAttribArray(0) # attribute index 0

        #--- TEXTURE COORDINATES (VBO) ------------------------------
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_coords_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.mesh_tex_coords)), # size
            (gl.GLfloat * len(self.mesh_tex_coords)) (*self.mesh_tex_coords), # data
            gl.GL_STATIC_DRAW # usage
        )

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0) # array of generic vertex data
        gl.glEnableVertexAttribArray(1) # attribute index 1

        #--- SHADING VALUES (VBO) -----------------------------------

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.shading_values_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.mesh_shading_values)), # size
            (gl.GLfloat * len(self.mesh_shading_values)) (*self.mesh_shading_values), # data
            gl.GL_STATIC_DRAW # usage
        )

        gl.glVertexAttribPointer(2, 1, gl.GL_FLOAT, gl.GL_FALSE, 0, 0) # array of generic vertex data
        gl.glEnableVertexAttribArray(2) # attribute index 2

        #--- INDEX BUFFER OBJECT (IBO) ------------------------------

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLuint * len(self.mesh_indices)), # size
            (gl.GLuint * len(self.mesh_indices)) (*self.mesh_indices), # data
            gl.GL_STATIC_DRAW # usage
        )


    def draw(self):
        if not self.mesh_index_counter:
            return
        
        gl.glBindVertexArray(self.vao)

        # render primitive using indexed vertex data
        gl.glDrawElements(
            gl.GL_TRIANGLES, # type of primitive to render
            len(self.mesh_indices), # number of indices
            gl.GL_UNSIGNED_INT, # data type of indices
            None # pointer to index array
        )


