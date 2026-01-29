# an array of indices lists indexes.
# an array of vertices lists vertex positions.
# an array of colors holds potential vertex colors.
# indexes can match vertex positions to their corresponding color.

# Indices = [1,2,3] 
# Vertices: [(0,0), (1,0), (0,1)]
# Colors: [(1,0,0), (0,1,0), (0,0,1)]

import ctypes
import pyglet.gl as gl

class Shader_error(Exception):
    def __init__(self, message):
        self.message = message

# target = shader we are creating
# source_path = source code of shader
def create_shader(target, source_path):
    #
    # read shader source
    #

    # "r" = read, "b" = binary
    source_file = open(source_path, "rb")
    source = source_file.read()
    source_file.close()

    source_length = ctypes.c_int(len(source) + 1) # c_int = signed

    # creates a ctypes array of c_char
    source_buffer = ctypes.create_string_buffer(source)

    # returns an instance of type pointing to the same memory block as obj
    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)), # obj
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char)) # type
    )

    #
    # compile shader
    #

    # set source code for shader object - shader, count, string, length
    gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
    gl.glCompileShader(target)
    
    #
    # handle potential errors
    #

    log_length = gl.GLint(0)
    gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))

    log_buffer = ctypes.create_string_buffer(log_length.value)
    gl.glGetShaderInfoLog(target, log_length, None, log_buffer)

    #if log_length:
        #raise Shader_error(str(log_buffer.value))
    

class Shader:
    def __init__(self, vert_path, frag_path):
        self.program = gl.glCreateProgram()

        #
        # create vertex shader and attach it to program.
        # processes vertex attributes such as position and color.
        # essential in controlling geometry for rasterization.
        #

        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        gl.glAttachShader(self.program, self.vert_shader)

        #
        # create fragment shader and attach it to program.
        # runs on each pixel, or fragment, and outputs it.
        #

        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)

        # link shaders and delete shader profiles after completion

        gl.glLinkProgram(self.program)
        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)
    
    def __del__(self):
        gl.glDeleteProgram(self.program)

    # shader uniforms allow us to pass data from outside the shader
    def find_uniform(self, name):
        return gl.glGetUniformLocation(
            self.program, 
            ctypes.create_string_buffer(name)
        )
    
    # take matrix and set uniform to it
    def uniform_matrix(self, location, matrix):
        gl.glUniformMatrix4fv(
            location, 
            1, 
            gl.GL_FALSE,
            (gl.GLfloat * 16) (*sum(matrix.data, []))
        )

    def use(self):
        gl.glUseProgram(self.program)
