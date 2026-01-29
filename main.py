import ctypes # allows you to manipulate C types
import pyglet # provides windowing, game control, and display

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl # reference for Open Graphics Library (OpenGL)

vertex_positions = [
    -0.5, 0.5, 1.0,
    -0.5, -0.5, 1.0,
    0.5, -0.5, 1.0,
    0.5, 0.5, 1.0,
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
    
    def on_draw(self):

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