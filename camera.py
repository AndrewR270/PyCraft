import math
import matrix

#
# Camera - Responsible for handling matrices in order to transform
# the scene around our viewport. It does not actually render anything;
# that is the job of a Window object in main.py.
#
class Camera:

    #
    # __init__ - Constructor, on instantiation of a Camera object.
    #
    def __init__(self, shader, width, height):

        self.width = width
        self.height = height

        self.mv_matrix = matrix.Matrix() # ModelView
        self.p_matrix = matrix.Matrix() # Projection

        self.shader = shader
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")

        self.position = [0, 0, -3] # Current Position
        self.input = [0, 0, 0] # New Offsets
        self.rotation = [math.tau / 4, 0]

    def update_camera(self, delta_time):
        speed = 7
        multiplier = speed * delta_time

        self.position[1] += self.input[1] * multiplier # Move on Y, easy up and down

        # Move on X and Z, need angle to move since based on rotation

        # check that at least one component is nonzero
        if self.input[0] or self.input[2]:
            angle = self.rotation[0] + math.atan2(self.input[2], self.input[0]) - math.tau / 4 # z, x
            self.position[0] += math.cos(angle) * multiplier # cos theta = adj/hyp
            self.position[2] += math.sin(angle) * multiplier # sin theta = opp/hyp


    def update_matrices(self):
        
        #### initialize matrices ####################################
        
        #--- PROJECTION MATRIX --------------------------------------

        self.p_matrix.load_identity() # neutral, doesn't transform
        self.p_matrix.perspective(
            90, # FOV in degrees
            float(self.width) / self.height, # aspect ratio
            0.1, # minimum distance
            500 # maximum distance
        )

        #--- MODEL-VIEW MATRIX --------------------------------------

        self.mv_matrix.load_identity()
        self.mv_matrix.rotate_2d(-(self.rotation[0] - math.tau/4), self.rotation[1])
        self.mv_matrix.translate(-self.position[0], -self.position[1], self.position[2])

        #--- MODEL-VIEW-PROJECTION MATRIX ---------------------------

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)