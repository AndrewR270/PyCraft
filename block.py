# Manages block textures and models.

import numbers

class Block:
    # Assigning values to parameters initializes default values
    def __init__(self, texture_manager, name = "unknown", block_face_textures = {"all": "cobblestone"}):
        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.indices = numbers.indices

        # load all textures for this block into the manager
        for face in block_face_textures:
            texture = block_face_textures[face]
            texture_manager.add_texture(texture)