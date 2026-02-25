import math
import random
import chunk
import block
import texture_manager
import models.plant
import models.cactus

class World:

    def __init__(self):

        ##### define blocks #########################################

        self.texture_manager = texture_manager.Texture_manager(16, 16, 256) # w16, h16, 256 textures
        self.block_types = [None] #0, air

        # define each block, pass in texture manager and a list of faces and associated textures
        self.block_types.append(block.Block(self.texture_manager, "grass", {"top":"grass", "bottom":"dirt", "sides":"grass_side"})) #1
        self.block_types.append(block.Block(self.texture_manager, "dirt", {"all":"dirt"})) #2
        self.block_types.append(block.Block(self.texture_manager, "cobblestone", {"all":"cobblestone"})) #3
        self.block_types.append(block.Block(self.texture_manager, "stone", {"all":"stone"})) #4
        self.block_types.append(block.Block(self.texture_manager, "sand", {"all":"sand"})) #5
        self.block_types.append(block.Block(self.texture_manager, "log", {"top":"log_top", "bottom":"log_top", "sides":"log_side"})) #6
        self.block_types.append(block.Block(self.texture_manager, "planks", {"all":"planks"})) #7
        self.block_types.append(block.Block(self.texture_manager, "daisy", {"all": "daisy"}, models.plant)) #8
        self.block_types.append(block.Block(self.texture_manager, "rose", {"all": "rose"}, models.plant)) #9
        self.block_types.append(block.Block(self.texture_manager, "dead_bush", {"all": "dead_bush"}, models.plant)) #10
        self.block_types.append(block.Block(self.texture_manager, "cactus", {"top":"cactus_top", "bottom":"cactus_bottom", "sides":"cactus_side"}, models.cactus)) #11

        self.texture_manager.generate_mipmaps()

        self.chunks = {}

        for x in range(8):
            for z in range(8):
                chunk_position = (x-4, -1, z-4)
                current_chunk = chunk.Chunk(self, chunk_position)

                for chunk_x in range(chunk.CHUNK_WIDTH):
                    for chunk_y in range(chunk.CHUNK_HEIGHT):
                        for chunk_z in range(chunk.CHUNK_LENGTH):
                            if chunk_y == 15: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = random.choice(
									[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 9, 10, 11])
                            elif chunk_y > 13: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = random.choice([0, 1])
                            else: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = random.choice([0, 0, 3])

                self.chunks[chunk_position] = current_chunk

        for chunk_position in self.chunks:
            self.chunks[chunk_position].update_mesh()

    def get_block_number(self, position):
        x,y,z = position # location of the block in the world

        # Find chunk position based on multiples of chunk size
        chunk_position = (
            math.floor(x / chunk.CHUNK_WIDTH),
            math.floor(y / chunk.CHUNK_HEIGHT),
            math.floor(z / chunk.CHUNK_LENGTH)
        )

        # Check if the chunk exists
        if not chunk_position in self.chunks:
            return 0 # air
        
        # Find block position within our chunk
        local_x = int(x % chunk.CHUNK_WIDTH)
        local_y = int(y % chunk.CHUNK_HEIGHT)
        local_z = int(z % chunk.CHUNK_LENGTH)

        #Return the block at the local position in the chunk at the chunk position
        block_number = self.chunks[chunk_position].blocks[local_x][local_y][local_z]
        block_type = self.block_types[block_number]

        if not block_type or block_type.transparent: return 0
        else: return block_number

    def draw(self):
        for chunk_position in self.chunks:
            self.chunks[chunk_position].draw()