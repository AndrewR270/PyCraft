import ctypes
import pyglet.gl as gl

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
CHUNK_LENGTH = 16

class Chunk:

    def __init__(self, chunk_position):

        self.chunk_position = chunk_position

        self.position = (
            self.chunk_position[0] * CHUNK_WIDTH,
            self.chunk_position[1] * CHUNK_HEIGHT,
            self.chunk_position[2] * CHUNK_LENGTH
        )

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


    def update_mesh(self, block):
        self.has_mesh = True
        self.mesh_vertex_positions = []
        self.mesh_index_counter = 0
        self.mesh_indices = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []

        # Loop from front to back of each "roll" of 16 blocks.
        # Move from up until 16 "rolls" are made.
        # Move right to next slice.
        for local_x in range(CHUNK_WIDTH): # 0 to 15
            for local_y in range(CHUNK_HEIGHT): # 0 to 15
                for local_z in range(CHUNK_LENGTH): # 0 to 15
                    x,y,z = (
                        self.position[0] + local_x, # location of chunk + x offset in chunk
                        self.position[1] + local_y, # location of chunk + y offset in chunk
                        self.position[2] + local_z, # location of chunk + z offset in chunk
                    )

                    vertex_positions = block.vertex_positions.copy()

                    # Loop through each vertex in our cube. Each of the 24 vertices has x,y,z
                    # Add our coordinate offsets depending on what block is in the chunk.
                    for i in range(24):
                        vertex_positions[i * 3 + 0] += x
                        vertex_positions[i * 3 + 1] += y
                        vertex_positions[i * 3 + 2] += z

                    self.mesh_vertex_positions.extend(vertex_positions) # add vertex positions of our block to mesh

                    indices = block.indices.copy()

                    # There are 6 indexes per face, since 2 triangles of 3 vertices are drawn.
                    # Multiplied by 6 faces, this is 36 indices.
                    # In our chunk, we have one giant set of vertices. 
                    # There are 24 different unique vertices in the 36.
                    # So, for every block, we add 24 * block number to all the vertices.
                    # This is so multiple blocks do not share the same vertices.
                    for i in range(36):
                        indices[i] += self.mesh_index_counter

                    self.mesh_indices.extend(indices)
                    self.mesh_index_counter += 24

                    self.mesh_tex_coords.extend(block.tex_coords) # tex coords are same
                    self.mesh_shading_values.extend(block.shading_values) # shading values are same


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


