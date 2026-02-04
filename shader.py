import ctypes
import pyglet.gl as gl

#
# Shader_error - Class is instantiated whenever a 
# shader error is thrown.
#
class Shader_error(Exception):
    def __init__(self, message):
        self.message = message


#
# create_shader - A method which takes a target, or shader we are
# creating, and a source path, the code of our shader.
#
def create_shader(target, source_path):

    #### read shader source and compile #############################

    source_file = open(source_path, "rb") # "rb" = read binary
    source = source_file.read()
    source_length = ctypes.c_int(len(source) + 1) # c_int = signed
    source_buffer = ctypes.create_string_buffer(source) # array of c_char
    source_file.close()

    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)), # object
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char)) # type to cast
    )

    gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
    gl.glCompileShader(target)
    
    #### handle potential errors ####################################

    log_length = gl.GLint(0)
    gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
    log_buffer = ctypes.create_string_buffer(log_length.value)
    gl.glGetShaderInfoLog(target, log_length, None, log_buffer)
    

#
# Shader - Class which handles shader programs. This handles both a
# vertex shader for position and raster geometry as well as a 
# fragment shader for dividing shapes into color or texture areas.
#
class Shader:

    #
    # __init__ - Constructor, on instantiation of a Shader object.
    #
    def __init__(self, vert_path, frag_path):
        self.program = gl.glCreateProgram()

        #### create vertex shader ###################################

        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        gl.glAttachShader(self.program, self.vert_shader)

        #### create fragment shader #################################

        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)

        #### link shaders and delete after completion ###############

        gl.glLinkProgram(self.program)
        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)
    
    #
    # __del__ - Stops shader program from running.
    #
    def __del__(self):
        gl.glDeleteProgram(self.program)
    
    #
    # find_uniform - Returns a shader uniform, or a global shader
    # variable which does not change. This will allow us to pass data 
    # from outside the shader.
    #
    def find_uniform(self, name):
        return gl.glGetUniformLocation(
            self.program, 
            ctypes.create_string_buffer(name)
        )
    
    #
    # uniform_matrix - Takes matrix and set uniform to it.
    #
    def uniform_matrix(self, location, matrix):
        gl.glUniformMatrix4fv(
            location, 
            1, 
            gl.GL_FALSE,
            (gl.GLfloat * 16) (*sum(matrix.data, []))
        )

    #
    # use - Sets shader into action.
    #
    def use(self):
        gl.glUseProgram(self.program)
