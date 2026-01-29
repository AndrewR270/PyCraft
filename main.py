import math
import ctypes # allows you to manipulate C types
import pyglet # provides windowing, game control, and display

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl # reference for Open Graphics Library (OpenGL)

import matrix
import shader

# matrices - when multiplied with a vector, they transform it
# each vertex in the scene can be represented as a vector from the origin
# this allows us to transform the scene's vertices in a model matrix.
# we can transform the scene around the camera in a view matrix.
# these can be locked into one matrix, the modelview matrix.
# a projection matrix handles field of view, compressing viewable
# objects into the screen position. The farther from  the camera, the more
# objects can be seen, but they must be rendered as smaller.
# the axis which extends straight out from the camera is the W or depth 
# component axis. This lets us know which objects are in front of others.
# ModelView x Projection = ModelViewProjection matrix
# ModelViewProjection x Vertex vector
 
vertex_positions = [
    -0.5, 0.5, 0.0,
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
    0.5, 0.5, 0.0,
] 

indices = [
    0, 1, 2, #first triangle
    0, 2, 3, #second triangle
]

class Window(pyglet.window.Window):

    # "__init__" is a constructor.
    # the tutorial uses the keyword "self" instead of "this".
    def __init__(self, **args): 
    
        super().__init__(**args)

        #
        # create vertex array object (vao)
        #

        self.vao = gl.GLuint(0) # unsigned integer
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        #
        # create vertex buffer array object (vbo).
        # a buffer object stores an array of unformatted memory.
        #

        self.vbo = gl.GLuint(0) # unsigned integer
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        # initialize the buffer object
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLfloat * len(vertex_positions)), # size
            (gl.GLfloat * len(vertex_positions)) (*vertex_positions), # data
            gl.GL_STATIC_DRAW # usage
        )
        
        # create an array of generic vertex attribute data
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        #
        # create index buffer object (ibo)
        #

        self.ibo = gl.GLuint(0) # unsigned integer
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        # initialize the buffer object
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER, # target
            ctypes.sizeof(gl.GLuint * len(indices)), # size
            (gl.GLuint * len(indices)) (*indices), # data
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
        self.mv_matrix.translate(0, 0, -1)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)

        # modelviewprojection matrix

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        # set and clear buffer to specified color
        gl.glClearColor(1.0, 0.5, 1.0, 1.0)
        self.clear()

        # render primitive using indexed vertex data
        gl.glDrawElements(
            gl.GL_TRIANGLES, # type of primitive to render
            len(indices), # number of indices
            gl.GL_UNSIGNED_INT, # data type of indices
            None # pointer to index array
        )
    
    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        #gl.glViewport(0,0,width,height)

class Game:
    def __init__(self):
        # Had to add "double_buffer = True" to get screen to work.
        self.config = gl.Config(major_version = 3, double_buffer=True)
        self.window = Window(config = self.config, width=800, height=600, caption="PyCraft", resizable=True, vsync=False)
        
    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()