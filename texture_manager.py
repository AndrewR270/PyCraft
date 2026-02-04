import ctypes
import pyglet
import pyglet.gl as gl

#
# Texture_manager - Handles the texture encoding of all blocks. Class 
# is instantiated in main.py, and one instance of the manager is used 
# by all blocks. Formats textures for samping and generates mipmaps.
#
class Texture_manager:

    #
    # __init__ - Constructor, on instantiation of a Texture_manager.
    #
    def __init__(self, texture_width, texture_height, max_textures):

        self.texture_width = texture_width
        self.texture_height = texture_height
        self.max_textures = max_textures
        self.textures = [] # list of all added textures

        ##### create 3D texture array ###############################

        self.texture_array = gl.GLuint(0)
        gl.glGenTextures(1, self.texture_array)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

        # stop OpenGL from linear interpolation of neighboring pixels, producing blurriness.
        # instead, we tell OpenGL to select the nearest pixel's color when sampling.
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY, 0, gl.GL_RGBA, # target, level, internal format
            self.texture_width, self.texture_height, self.max_textures, # width, height, depth
            0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None # border, format, type, pixels
        )

    #
    # generate_mipmaps - Make smaller textures for further distances.
    #
    def generate_mipmaps(self):
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D_ARRAY)

    #
    # add_texture - Writes a new texture to the 3D array if not already handled.
    #
    def add_texture(self, texture):
        if not texture in self.textures:
            self.textures.append(texture) # add texture to list
            texture_image = pyglet.image.load(f"textures/{texture}.png").get_image_data()
            gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array) # ensure texture array is bound

            # copy texture data into array
            gl.glTexSubImage3D(
                gl.GL_TEXTURE_2D_ARRAY, 0, # target, level
                0, 0, self.textures.index(texture), # x offset, y offset, z offset (layer)
                self.texture_width, self.texture_height, 1, # width, height, depth
                gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, # format, type
                texture_image.get_data("RGBA", texture_image.width * 4) # pixels (data)
            )