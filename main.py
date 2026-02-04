import math
import ctypes
import pyglet
import pyglet.gl as gl
import matrix
import shader
import block
import texture_manager

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

#
# Window - Overloads Pyglet Window. Calls super() to initialize the 
# window and additionally instantiates the necessary graphical 
# components for our specific rendering purposes.
#
class Window(pyglet.window.Window):

    #
    # __init__ - Constructor, on instantiation of a Window object.
    #
    def __init__(self, **args): 
        
        super().__init__(**args) # creates pyglet window

        ##### define blocks #########################################

        self.texture_manager = texture_manager.Texture_manager(16, 16, 256) # w16, h16, 256 textures

        # define each block, pass in texture manager and a list of faces and associated textures
        self.grass = block.Block(self.texture_manager, "grass", {"top":"grass", "bottom":"dirt", "sides":"grass_side"} )
        self.dirt = block.Block(self.texture_manager, "dirt", {"all":"dirt"})
        self.cobblestone = block.Block(self.texture_manager, "cobblestone", {"all":"cobblestone"})
        self.stone = block.Block(self.texture_manager, "stone", {"all":"stone"})
        self.sand = block.Block(self.texture_manager, "sand", {"all":"sand"})
        self.log = block.Block(self.texture_manager, "log", {"top":"log_top", "bottom":"log_top", "sides":"log_side"})
        self.planks = block.Block(self.texture_manager, "planks", {"all":"planks"})

        self.texture_manager.generate_mipmaps()


        #### allocate memory ########################################

        #--- VERTEX ARRAY OBJECT (VAO) ------------------------------
 
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        #--- VERTEX POSITIONS (VBO) ---------------------------------

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vertex_position_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_positions)), # size
            (gl.GLfloat * len(self.grass.vertex_positions)) (*self.grass.vertex_positions), # data
            gl.GL_STATIC_DRAW # usage
        )

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0) # array of generic vertex data
        gl.glEnableVertexAttribArray(0) # attribute index 0

        #--- TEXTURE COORDINATES (VBO) ------------------------------

        self.tex_coord_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.tex_coord_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_coord_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.grass.tex_coords)), # size
            (gl.GLfloat * len(self.grass.tex_coords)) (*self.grass.tex_coords), # data
            gl.GL_STATIC_DRAW # usage
        )

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0) # array of generic vertex data
        gl.glEnableVertexAttribArray(1) # attribute index 1

        #--- INDEX BUFFER OBJECT (IBO) ------------------------------

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLuint * len(self.grass.indices)), # size
            (gl.GLuint * len(self.grass.indices)) (*self.grass.indices), # data
            gl.GL_STATIC_DRAW # usage
        )


        #### create shaders and matrices ############################

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader_sampler_location = self.shader.find_uniform(b"texture_array_sampler")
        self.shader.use()

        self.mv_matrix = matrix.Matrix() # ModelView
        self.p_matrix = matrix.Matrix() # Projection


        #### rotation animation #####################################

        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60) # every 60th of a second

    #
    # update - Runs every scheduled interval to perform some function.
    #
    def update(self, delta_time):
        self.x += delta_time
    
    #
    # on_draw - Called every frame to redraw the contents of our window. 
    # Responsible for graphical rendering.
    #
    def on_draw(self):

        #### initialize matrices ####################################
        
        #--- PROJECTION MATRIX --------------------------------------

        self.p_matrix.load_identity() # neutral, doesn't transform
        self.p_matrix.perspective(
            90, # FOV in degrees
            float(self.width) / self.height, # aspect ratio
            0.1, # minimum distance
            500 # maximum distance
        )

        #--- MODEL-VIEW MATRIX --------------------------------------

        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -3) # "Camera" position
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)

        #--- MODEL-VIEW-PROJECTION MATRIX ---------------------------

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        
        #### bind textures ##########################################

        gl.glActiveTexture(gl.GL_TEXTURE0) # first texture unit
        # bind our texture manager's texture
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_manager.texture_array)
        # tell sampler that the texture is bound to the first texture unit
        gl.glUniform1i(self.shader_sampler_location, 0)
        
        
        #### draw shapes ############################################

        gl.glEnable(gl.GL_DEPTH_TEST) # Enables depth
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT) # clears depth bits for screen
        gl.glClearColor(0.0, 0.0, 0.0, 1.0) # Sets screen color
        self.clear()

        # render primitive using indexed vertex data
        gl.glDrawElements(
            gl.GL_TRIANGLES, # type of primitive to render
            len(self.grass.indices), # number of indices
            gl.GL_UNSIGNED_INT, # data type of indices
            None # pointer to index array
        )
    
    #
    # on_resize - Called when window changes size.
    #
    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        #gl.glViewport(0,0,width,height)


#
# Game - Class which runs the PyCraft simulation. Configures graphical 
# settings and creates a Window object for displaying graphics.
#
class Game:
    
    #
    # __init__ - Constructor, on instantiation of the game.
    #
    def __init__(self):
        self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3, depth_size = 16)
        self.window = Window(config = self.config, width=800, height=600, caption="PyCraft", resizable=True, vsync=False)

    #
    # run - Starts the game.
    #  
    def run(self):
        pyglet.app.run()


#
# Allows main.py to create an instance of 
# the Game class and run it.
#
if __name__ == "__main__":
    game = Game()
    game.run()