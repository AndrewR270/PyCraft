import math

HIT_RANGE = 3

class Hit_ray:
    def __init__(self, world, rotation, starting_position):
        self.world = world
        # ray extending from camera is q

        # Make unit direction vector u, <cos(Rx)*cos(Ry), sin(Ry), sin(Rx)*cos(Ry)>
        # unit vectors have a length of 1, so we can change length to translate points different distances
        self.vector = (
            math.cos(rotation[0]) * math.cos(rotation[1]),
            math.sin(rotation[1]),
            math.sin(rotation[0]) * math.cos(rotation[1])
        )

        # Position of tracing point P
        self.position = list(starting_position)
        # get block surrounding our raycast point; works because blocks are 1 unit wide, centered on integer coords
        self.block = tuple(map(lambda x: int(round(x)), self.position))

        self.distance = 0

    def check(self, hit_callback, distance, current_block, next_block):
        if self.world.get_block_number(next_block):
            hit_callback(current_block, next_block)
            return True

        self.position = list(map(lambda x: self.position[x] + self.vector[x] * distance, range(3)))
        self.block = next_block
        self.distance += distance

        return False


    def step(self, hit_callback):
        block_x, block_y, block_z = self.block
        # takes point position and subtracts block from it

        #L = <Px-Bx, Py-By, Pz-Bz>
        local_position = list(map(lambda x: self.position[x] - self.block[x], range(3)))

        # disregard all negative faces, instead flip around origin in center of block
        # takes absolute value of vector, so we don't have to worry about sign for intersection
        
        sign = [1, 1, 1] # 1=pos, -1=neg
        absolute_vector = list(self.vector)

        for component in range(3):
            if self.vector[component] < 0:
                sign[component] = -1

                absolute_vector[component] = -absolute_vector[component]
                local_position[component] = -local_position[component]

        lx, ly, lz = local_position
        vx, vy, vz = absolute_vector

        # absolute vector v = <|Ux|,|Uy|,|Uz|>
        # Nearest intersection to L between r and our three faces
        # r = Parametric, (1/vector x)(x - point x) and so on
        # r = (x-Lx/vx) = (y-Ly/vy) = (z-Lz/vz)
        # F = faces, Fx, Fy, Fz

        # Intersection of Face F with r, is plane of F (p) intersection with r
        # x = 1/2 because plane is axis aligned, 1/2 to either side
        #System: x=1/2 and (x-Lx/vx) = (y-Ly/vy) = (z-Lz/vz)
        # so x = 1/2
        # so y = (1/2-Lx/vx)vy + Ly
        # so y = (1/2-Lx/vx)vz + Lz
        # if vx = 0, r and Fx = p are parallel, not perpendicular, and so don't intersect,
        # since vector is on yz plane

        if vx:
            x = 0.5
            y = (((0.5 - lx) / vx) * vy) + ly
            z = (((0.5 - lx) / vx) * vz) + lz

            # now we know where in space the intersection with the plane is
            # check if intersection is situated inside our face
            # (x coordinate may be valid, but is it out of the y or z bounds?)

            if (y >= -0.5 and y <= 0.5 and z >= -0.5 and z <= 0.5):
                # take magnitude of vector, which is distance between two points
                # distance between point of intersection and L, so we know how much to move P along q
                distance = math.sqrt((x-lx) ** 2 + (y-ly) ** 2 + (z-lz) ** 2)

                # distance, block, adjacent block either left or right depending on sign of face
                return self.check(hit_callback, distance, self.block, (block_x + sign[0], block_y, block_z))

        if vy:
            x = (((0.5 - ly) / vy) * vx) + lx
            y = 0.5
            z = (((0.5 - ly) / vy) * vz) + lz

            # now we know where in space the intersection with the plane is
            # check if intersection is situated inside our face
            # (y coordinate may be valid, but is it out of the x or z bounds?)

            if (x >= -0.5 and x <= 0.5 and z >= -0.5 and z <= 0.5):
                # take magnitude of vector, which is distance between two points
                # distance between point of intersection and L, so we know how much to move P along q
                distance = math.sqrt((x-lx) ** 2 + (y-ly) ** 2 + (z-lz) ** 2)

                # distance, block, adjacent block either up or down depending on sign of face
                return self.check(hit_callback, distance, self.block, (block_x, block_y + sign[1], block_z))

        if vz:
            x = (((0.5 - lz) / vz) * vx) + lx
            y = (((0.5 - lz) / vz) * vy) + ly
            z = 0.5

            # now we know where in space the intersection with the plane is
            # check if intersection is situated inside our face
            # (z coordinate may be valid, but is it out of the x or y bounds?)

            if (x >= -0.5 and x <= 0.5 and y >= -0.5 and y <= 0.5):
                # take magnitude of vector, which is distance between two points
                # distance between point of intersection and L, so we know how much to move P along q
                distance = math.sqrt((x-lx) ** 2 + (y-ly) ** 2 + (z-lz) ** 2)

                # distance, block, adjacent block either up or down depending on sign of face
                return self.check(hit_callback, distance, self.block, (block_x, block_y, block_z + sign[2]))