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

        self.position = [0, 0, 0] # Current Position
        self.input = [0, 0, 0] # New Offsets
        self.rotation = [-math.tau / 4, 0]


    #
    # update_camera - Modifies position attributes based on current
    # inputs and current rotation.
    #
    def update_camera(self, delta_time):
        speed = 7
        multiplier = speed * delta_time

        self.position[1] += self.input[1] * multiplier # Move on Y

        # Move on X and Z, based on rotation
        if self.input[0] or self.input[2]: # Check at least one component is nonzero
            angle = self.rotation[0] - math.atan2(self.input[2], self.input[0]) + math.tau / 4
            self.position[0] += math.cos(angle) * multiplier
            self.position[2] += math.sin(angle) * multiplier


    #
    # update_matrices - Creates a modelview matrix for rotating and transforming
    # the scene relative to our camera; this changes based on our new position
    # values. Multiplies a projection matrix by it and sends to shader.py.
    #
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
        self.mv_matrix.rotate_2d(self.rotation[0] + math.tau/4, self.rotation[1])
        self.mv_matrix.translate(-self.position[0], -self.position[1], -self.position[2])

        #--- MODEL-VIEW-PROJECTION MATRIX ---------------------------

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)