# Manages block textures and models.

import numbers

class Block:
    # Assigning values to parameters initializes default values
    def __init__(self, texture_manager, name = "block", block_face_textures = {"all": "texture"}):
        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.indices = numbers.indices
        # we need to create a deep copy in order to modify the texture coords.
        self.tex_coords = numbers.tex_coords.copy()

        # set a specific face of the block to a certain texture
        def set_block_face(side, texture):
            for vertex in range(4):
                self.tex_coords[side * 12 + vertex * 3 + 2] = texture

        # load all textures for this block into the manager
        for face in block_face_textures:
            texture = block_face_textures[face]
            texture_manager.add_texture(texture)

            texture_index = texture_manager.textures.index(texture)

            if face == "all":
                set_block_face(0, texture_index) # right face
                set_block_face(1, texture_index) # left face
                set_block_face(2, texture_index) # top face
                set_block_face(3, texture_index) # bottom face
                set_block_face(4, texture_index) # front face
                set_block_face(5, texture_index) # back face

            elif face == "sides":
                set_block_face(0, texture_index) # right face
                set_block_face(1, texture_index) # left face
                set_block_face(4, texture_index) # front face
                set_block_face(5, texture_index) # back face

            else:
                set_block_face(
                    ["right", "left", "top", "bottom", "front", "back"].index(face), 
                    texture_index # set texture for a specified face
                )



            