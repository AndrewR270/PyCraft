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
                            # Potential blocks are 0, 9, and 10, with probabilities 20, 2, and 1. Access element 0 of the returned list.
                            if chunk_y == 15: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = random.choices([0, 8, 9], [20, 2, 1])[0]
                            elif chunk_y == 14: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = 1
                            elif chunk_y > 12: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = 2
                            else: current_chunk.blocks[chunk_x][chunk_y][chunk_z] = 4

                self.chunks[chunk_position] = current_chunk

        for chunk_position in self.chunks:
            self.chunks[chunk_position].update_subchunk_meshes()
            self.chunks[chunk_position].update_mesh()

    # Find chunk position based on multiples of chunk size
    def get_chunk_position(self, position):
        x, y, z = position # location of the block in the world
        return(
            math.floor(x / chunk.CHUNK_WIDTH),
            math.floor(y / chunk.CHUNK_HEIGHT),
            math.floor(z / chunk.CHUNK_LENGTH)
        )
    
    # Find block position within a chunk
    def get_local_position(self, position):
        x, y, z = position # location of the block in the world
        return(
            math.floor(x % chunk.CHUNK_WIDTH),
            math.floor(y % chunk.CHUNK_HEIGHT),
            math.floor(z % chunk.CHUNK_LENGTH)
        )

    def get_block_number(self, position):
        x,y,z = position # location of the block in the world
        
        # Check if the chunk exists
        chunk_position = self.get_chunk_position(position)
        if chunk_position not in self.chunks: return 0 # air
        
        # Find block position within our chunk
        local_x, local_y, local_z = self.get_local_position(position)

        #Return the block at the local position in the chunk at the chunk position
        return self.chunks[chunk_position].blocks[local_x][local_y][local_z]
    
    def is_transparent_block(self, position):
        block = self.block_types[self.get_block_number(position)]
        if not block: return True # true if block is air
        return block.transparent # true if block is transparent
    
    def set_block(self, position, number):
        x,y,z = position # location of the block in the world
        chunk_position = self.get_chunk_position(position)

        # Make new chunk if a non-air block is placed out of bounds
        if not chunk_position in self.chunks and number:
            self.chunks[chunk_position] = chunk.Chunk(self, chunk_position)

        # Make no change if the block as the position is already there
        if self.get_block_number(position) == number: return

        # Set block at local position in chunk
        local_x, local_y, local_z = self.get_local_position(position)
        self.chunks[chunk_position].blocks[local_x][local_y][local_z] = number
        self.chunks[chunk_position].update_at_position((x, y, z))
        self.chunks[chunk_position].update_mesh()

        # Update neighboring chunk if block was changed at border
        chunk_x, chunk_y, chunk_z = chunk_position

        def try_update_chunk_mesh_at_position(chunk_position, position):
            if chunk_position in self.chunks:
                self.chunks[chunk_position].update_at_position(position)
                self.chunks[chunk_position].update_mesh()

        if local_x == chunk.CHUNK_WIDTH - 1: try_update_chunk_mesh_at_position((chunk_x+1, chunk_y, chunk_z), (x+1, y, z)) # right border
        elif local_x == 0: try_update_chunk_mesh_at_position((chunk_x-1, chunk_y, chunk_z), (x-1, y, z)) # left border

        if local_y == chunk.CHUNK_HEIGHT - 1: try_update_chunk_mesh_at_position((chunk_x, chunk_y+1, chunk_z), (x, y+1, z)) # top border
        elif local_y == 0: try_update_chunk_mesh_at_position((chunk_x, chunk_y-1, chunk_z), (x, y-1, z)) # bottom border

        if local_z == chunk.CHUNK_LENGTH - 1: try_update_chunk_mesh_at_position((chunk_x, chunk_y, chunk_z+1), (x, y, z+1)) # far border
        elif local_z == 0: try_update_chunk_mesh_at_position((chunk_x, chunk_y, chunk_z-1), (x, y, z-1)) # close border


    def draw(self):
        for chunk_position in self.chunks:
            self.chunks[chunk_position].draw()