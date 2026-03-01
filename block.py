import models.cube

#
# Block - Each block in the game is an instantiation of this class.
# It manages block models and textures.
#
class Block:

    #
    # __init__ - Constructor, on instantiation of a Block object.
    #
    def __init__(self, texture_manager, name = "block", block_face_textures = {"all": "texture"}, model = models.cube):

        self.name = name
        self.block_face_textures = block_face_textures
        self.model = model

        #--- READ MODEL DATA ----------------------------------------

        self.transparent = model.transparent
        self.is_cube = model.is_cube
        self.glass = model.glass
        self.vertex_positions = model.vertex_positions
        self.tex_coords = model.tex_coords.copy() # deep copy to modify texture coords
        self.shading_values = model.shading_values

        #
        # set_block_face - Set a specific face of the block to a certain texture.
        # The texture is passed in as an index in the texture array.
        #
        def set_block_face(face, texture):
            if (face > len(self.tex_coords)-1): return

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
                for i in range(len(self.tex_coords)):
                    set_block_face(i, texture_index)

            elif face == "sides":
                set_block_face(0, texture_index) # right
                set_block_face(1, texture_index) # left
                set_block_face(4, texture_index) # front
                set_block_face(5, texture_index) # back
                
            elif face == "x":
                set_block_face(0, texture_index)
                set_block_face(1, texture_index)

            elif face == "y":
                set_block_face(2, texture_index)
                set_block_face(3, texture_index)

            elif face == "z":
                set_block_face(4, texture_index)
                set_block_face(5, texture_index)

            else:
                set_block_face(
                    ["right", "left", "top", "bottom", "front", "back"].index(face), 
                    texture_index # set texture for a specified face
                )



            