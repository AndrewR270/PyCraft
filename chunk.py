import ctypes
import math
import pyglet.gl as gl

import subchunk

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 128
CHUNK_LENGTH = 16

class Chunk:

    def __init__(self, world, chunk_position):

        self.world = world

        self.modified = False

        self.chunk_position = chunk_position

        self.position = (
            self.chunk_position[0] * CHUNK_WIDTH,
            self.chunk_position[1] * CHUNK_HEIGHT,
            self.chunk_position[2] * CHUNK_LENGTH
        )

        self.blocks = [[[0 # block number
            for z in range (CHUNK_LENGTH)]
            for y in range (CHUNK_HEIGHT)]
            for x in range (CHUNK_WIDTH)]
        
        self.subchunks = {}

        for x in range(int(CHUNK_WIDTH / subchunk.SUBCHUNK_WIDTH)):
            for y in range(int(CHUNK_HEIGHT / subchunk.SUBCHUNK_HEIGHT)):
                for z in range(int(CHUNK_LENGTH / subchunk.SUBCHUNK_LENGTH)):
                    self.subchunks[(x,y,z)] = subchunk.Subchunk(self, (x,y,z))

        #--- MEMORY OBJECT DATA ARRAYS ------------------------------

        self.mesh_vertex_positions = []
        self.mesh_index_counter = 0
        self.mesh_indices = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []
        
        #### allocate memory ########################################

        #--- VERTEX ARRAY OBJECT (VAO) ------------------------------
 
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, self.vao)
        gl.glBindVertexArray(self.vao)

        #--- VERTEX POSITIONS (VBO) ---------------------------------

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.vertex_position_vbo)

        #--- TEXTURE COORDINATES (VBO) ------------------------------

        self.tex_coords_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.tex_coords_vbo)
        
        #--- SHADING VALUES (VBO) -----------------------------------

        self.shading_values_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.shading_values_vbo)

        #--- INDEX BUFFER OBJECT (IBO) ------------------------------

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)


    def update_subchunk_meshes(self):
        for subchunk_position in self.subchunks:
            subchunk = self.subchunks[subchunk_position]
            subchunk.update_mesh()

    def update_at_position(self, position):
        x, y, z = position

        local_x = int(x % subchunk.SUBCHUNK_WIDTH)
        local_y = int(y % subchunk.SUBCHUNK_HEIGHT)
        local_z = int(z % subchunk.SUBCHUNK_LENGTH)

        local_x_chunk, local_y_chunk, local_z_chunk = self.world.get_local_position(position)

        subchunk_x = math.floor(local_x_chunk / subchunk.SUBCHUNK_WIDTH)
        subchunk_y = math.floor(local_y_chunk / subchunk.SUBCHUNK_HEIGHT)
        subchunk_z = math.floor(local_z_chunk / subchunk.SUBCHUNK_LENGTH)

        self.subchunks[(subchunk_x, subchunk_y, subchunk_z)].update_mesh()

        def try_update_subchunk_mesh(subchunk_position):
            if subchunk_position in self.subchunks:
                self.subchunks[subchunk_position].update_mesh()

        if local_x == subchunk.SUBCHUNK_WIDTH - 1: try_update_subchunk_mesh((subchunk_x+1, subchunk_y, subchunk_z)) # left border
        elif local_x == 0: try_update_subchunk_mesh((subchunk_x-1, subchunk_y, subchunk_z)) # right border

        if local_y == subchunk.SUBCHUNK_HEIGHT - 1: try_update_subchunk_mesh((subchunk_x, subchunk_y+1, subchunk_z)) # top border
        elif local_y == 0: try_update_subchunk_mesh((subchunk_x, subchunk_y-1, subchunk_z)) # bottom border
    
        if local_z == subchunk.SUBCHUNK_LENGTH - 1: try_update_subchunk_mesh((subchunk_x, subchunk_y, subchunk_z+1)) # far border
        elif local_z == 0: try_update_subchunk_mesh((subchunk_x, subchunk_y, subchunk_z-1)) # close border
    
    def update_mesh(self):
        # combine all subchunks into one big chunk
        self.mesh_vertex_positions = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []
        self.mesh_indices = []
        self.mesh_index_counter = 0

        for subchunk_position in self.subchunks:
            subchunk = self.subchunks[subchunk_position]

            self.mesh_vertex_positions.extend(subchunk.mesh_vertex_positions)
            self.mesh_tex_coords.extend(subchunk.mesh_tex_coords)
            self.mesh_shading_values.extend(subchunk.mesh_shading_values)

            mesh_indices = [index + self.mesh_index_counter for index in subchunk.mesh_indices]
            self.mesh_indices.extend(mesh_indices)
            self.mesh_index_counter += subchunk.mesh_index_counter

        self.mesh_indices_length = len(self.mesh_indices)
        self.send_mesh_data_to_gpu()

        del self.mesh_vertex_positions
        del self.mesh_tex_coords
        del self.mesh_shading_values
        del self.mesh_indices

    def send_mesh_data_to_gpu(self):
    
        #### pass mesh data to gpu ##################################

        if not self.mesh_index_counter: return

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
            (gl.GLuint * self.mesh_indices_length) (*self.mesh_indices), # data
            gl.GL_STATIC_DRAW # usage
        )

    def draw(self):
        if not self.mesh_index_counter:
            return
        
        gl.glBindVertexArray(self.vao)

        # render primitive using indexed vertex data
        gl.glDrawElements(
            gl.GL_TRIANGLES, # type of primitive to render
            self.mesh_indices_length, # number of indices
            gl.GL_UNSIGNED_INT, # data type of indices
            None # pointer to index array
        )


