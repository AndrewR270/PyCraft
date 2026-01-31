import math
import ctypes # allows you to manipulate C types
import pyglet # provides windowing, game control, and display

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl # reference for Open Graphics Library (OpenGL)

import matrix
import shader
import block
import texture_manager

class Window(pyglet.window.Window):

    # "__init__" is a constructor.
    # the tutorial uses the keyword "self" instead of "this".
    def __init__(self, **args): 
    
        super().__init__(**args)

        #
        # create blocks
        #

        self.texture_manager = texture_manager.Texture_manager(16, 16, 256) # texture manager object, w16, h16, 256 textures

        self.grass = block.Block(self.texture_manager, "grass", {"top" : "grass", "bottom" : "dirt", "sides" : "grass_side"} )
        self.dirt = block.Block(self.texture_manager, "dirt", {"all" : "dirt"})
        self.cobblestone = block.Block(self.texture_manager, "cobblestone", {"all" : "cobblestone"})
        self.stone = block.Block(self.texture_manager, "stone", {"all" : "stone"})
        self.sand = block.Block(self.texture_manager, "sand", {"all" : "sand"})
        self.log = block.Block(self.texture_manager, "log", {"top": "log_top", "bottom" : "log_top", "sides" : "log_side"})
        self.planks = block.Block(self.texture_manager, "planks", {"all" : "planks"})

        self.texture_manager.generate_mipmaps()

        #
        # create vertex array object (vao).
        # it holds references to the vertex buffers and the index buffer.
        #

        self.vao = gl.GLuint(0) # unsigned integer
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        #
        # create vertex buffer array object (vbo).
        # a buffer object stores an array of unformatted memory.
        #

        self.vbo = gl.GLuint(0) # unsigned binary integer
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        # initialize the buffer object
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_positions)), # size
            (gl.GLfloat * len(self.grass.vertex_positions)) (*self.grass.vertex_positions), # data
            gl.GL_STATIC_DRAW # usage
        )
        
        # create an array of generic vertex attribute data
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        #
        # create index buffer object (ibo)
        #

        self.ibo = gl.GLuint(0) # unsigned binary integer
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        # initialize the buffer object
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLuint * len(self.grass.indices)), # size
            (gl.GLuint * len(self.grass.indices)) (*self.grass.indices), # data
            gl.GL_STATIC_DRAW # usage
        )

        #
        # create shader
        #

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader.use()

        #
        # create matrices
        #

        self.mv_matrix = matrix.Matrix() # ModelView
        self.p_matrix = matrix.Matrix() # Projection

        # update runs every 60th of a second to increment x
        # by bits each frame in a draw function
        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def update(self, delta_time):
        self.x += delta_time
    
    def on_draw(self):

        # create projection matrix

        self.p_matrix.load_identity() # neutral, doesn't transform
        self.p_matrix.perspective(
            90, # FOV in degrees
            float(self.width) / self.height, # aspect ratio
            0.1, # minimum distance
            500 # maximum distance
        )

        # create modelview matrix

        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -3) # "Camera" position
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)

        # modelviewprojection matrix

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        #
        # DRAW SHAPES
        #

        gl.glEnable(gl.GL_DEPTH_TEST) # Enables depth
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT) # clears depth for scren
        gl.glClearColor(0.0, 0.0, 0.0, 1.0) # Sets screen color
        self.clear()

        # render primitive using indexed vertex data
        gl.glDrawElements(
            gl.GL_TRIANGLES, # type of primitive to render
            len(self.grass.indices), # number of indices
            gl.GL_UNSIGNED_INT, # data type of indices
            None # pointer to index array
        )
    
    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        #gl.glViewport(0,0,width,height)

class Game:
    def __init__(self):
        # Had to add "double_buffer = True" to get screen to work.
        # A buffer is a region of memory - double buffering renders a new image to the "back"
        # while displaying the "front" and then switches out, to prevent incomplete renders.
        # Had to add depth_size = 16 to prevent back faces from rendering over front.
        self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3, depth_size = 16)
        self.window = Window(config = self.config, width=800, height=600, caption="PyCraft", resizable=True, vsync=False)
        
    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()