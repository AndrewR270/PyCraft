import math
import random
import chunk
import block
import texture_manager
import models
import save

class World:

    def __init__(self):

        ##### define blocks #########################################

        self.texture_manager = texture_manager.Texture_manager(16, 16, 256) # w16, h16, 256 textures
        self.block_types = [None] #0, air

        #--- OPEN AND READ BLOCK DATA SOURCE FILE -------------------

        blocks_data_file = open("data/blocks.mcpy")
        blocks_data = blocks_data_file.readlines()
        blocks_data_file.close()

        #--- ITERATE THROUGH EACH LINE IN FILE ----------------------

        for block_type in blocks_data:
            if block_type[0] in ["\n", "#"]: continue # ignore if empty or comment

            number, properties = block_type.split(":", 1) # split once at colon
            number = int(number) # new block index number
            name = "Unknown" # default block name
            model = models.cube # default block model
            texture = {"all" : "unknown"} # default block texture

            #--- READ PROPERTIES ------------------------------------

            for prop in properties.split(","): # separate properties by comma
                prop = prop.strip() # remove spaces around each property
                prop = list(filter(None, prop.split(' ', 1))) # separate into name (0) and data (1)

                if prop[0] == "sameas": # set equal to an existing block
                    sameas_number = int(prop[1])
                    name = self.block_types[sameas_number].name
                    texture = self.block_types[sameas_number].block_face_textures
                    model = self.block_types[sameas_number].model

                elif prop[0] == "name": name = eval(prop[1]) # set name

                # if first 7 characters = "texture", as some lines may have "textures" instead
                elif prop[0][:7] == "texture":
                    _, side = prop[0].split(".") # "_" = texture and "side" = the texture side
                    texture[side] = prop[1].strip() # set the texture at the side to the data

                elif prop[0] == "model": model = eval(prop[1]) # set model

            #--- ADD BLOCK TYPE -------------------------------------

            new_block = block.Block(self.texture_manager, name, texture, model)

            if number < len(self.block_types):self.block_types[number] = new_block
            else: self.block_types.append(new_block)

        self.texture_manager.generate_mipmaps()

        # load the world

        self.save = save.Save(self)

        self.chunks = {}
        self.save.load()

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
        self.chunks[chunk_position].modified = True

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