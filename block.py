import numbers

#
# Block - Each block in the game is an instantiation of this class.
# It manages block models and textures.
#
class Block:

    #
    # __init__ - Constructor, on instantiation of a Block object.
    #
    def __init__(self, texture_manager, name = "block", block_face_textures = {"all": "texture"}):

        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.tex_coords = numbers.tex_coords.copy() # deep copy to modify texture coords
        self.shading_values = numbers.shading_values

        #
        # set_block_face - Set a specific face of the block to a certain texture.
        # The texture is passed in as an index in the texture array.
        #
        def set_block_face(face, texture):
            self.tex_coords[face] = self.tex_coords[face].copy()
            
            for vertex in range(4):
                self.tex_coords[face][vertex * 3 + 2] = texture

        #
        # Load all textures for this block into the texture manager. Runs on each
        # specified face in the __init__ param array, ensuring the texture manager
        # contains the texture and that the texture coordinate array is mapping
        # texture to the face.
        #
        for face in block_face_textures:
            
            texture = block_face_textures[face]
            texture_manager.add_texture(texture)
            texture_index = texture_manager.textures.index(texture)

            if face == "all":
                set_block_face(0, texture_index) # right
                set_block_face(1, texture_index) # left
                set_block_face(2, texture_index) # top
                set_block_face(3, texture_index) # bottom
                set_block_face(4, texture_index) # front
                set_block_face(5, texture_index) # back

            elif face == "sides":
                set_block_face(0, texture_index) # right
                set_block_face(1, texture_index) # left
                set_block_face(4, texture_index) # front
                set_block_face(5, texture_index) # back

            else:
                set_block_face(
                    ["right", "left", "top", "bottom", "front", "back"].index(face), 
                    texture_index # set texture for a specified face
                )



            