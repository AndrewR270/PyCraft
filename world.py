import chunk
import block
import texture_manager

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

        self.texture_manager.generate_mipmaps()

        self.chunks = {}
        self.chunks[(0,0,0)] = chunk.Chunk(self, (0,0,0))

        for x in range(chunk.CHUNK_WIDTH): # 0 to 15
            for y in range(chunk.CHUNK_HEIGHT): # 0 to 15
                for z in range(chunk.CHUNK_LENGTH): # 0 to 15
                    self.chunks[(0,0,0)].blocks[x][y][z] = 1

        self.chunks[(0,0,0)].update_mesh()

    def draw(self):
        for chunk_position in self.chunks:
            self.chunks[chunk_position].draw()