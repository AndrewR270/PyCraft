import math
import matrix

class Camera:

    def __init__(self, shader, width, height):
        self.width = width
        self.height = height

        self.mv_matrix = matrix.Matrix() # ModelView
        self.p_matrix = matrix.Matrix() # Projection

        self.shader = shader
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")

        # Tau = 2pi. +Z = forward, +X = right.
        # +X = 0 Tau or Tau, +Z = Tau / 4.
        # Y rotation is in radians. +Y = up.

        # camera variables

        self.input = [0, 0, 0]
        self.position = [0, 0, -3]
        self.rotation = [math.tau / 4, 0]

    def update_camera(self, delta_time):
        speed = 7
        multiplier = speed * delta_time

        self.position[1] += self.input[1] * multiplier # Move on Y, easy up and down

        # Move on X and Z, need angle to move since based on rotation

        # check that at least one component is nonzero
        if self.input[0] or self.input[2]:
            angle = self.rotation[0] + math.atan2(self.input[2], self.input[0]) - math.tau / 4 # z, x
            # - math.tau/4 makes our angle 0 when facing forward, since we technically set it to math.tau/4
            # to begin with.

            # tan theta = opp/adj, or z/x. theta = atan(opp/adj).
            # atan2 allows us to get negative angles, since if x and z are both negative, we
            # should point behind, but we would get a positive angle instead since neg/neg = pos.
            # atan2 is a piecewise function that gives us the correct angle.

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

        # negative because we are moving scene around the camera and not other way around
        self.mv_matrix.load_identity()

        # x rotation faces +Z or tau/4 by default. When rotation is 0, this is the case.
        self.mv_matrix.rotate_2d(-(self.rotation[0] - math.tau/4), self.rotation[1]) # We do not want to tilt our camera sideways on Z.
        self.mv_matrix.translate(-self.position[0], -self.position[1], self.position[2]) # "Camera" position

        # Note! Rotating the scene before translation is 1st person. Translating before rotation is an "orbit effect".

        #--- MODEL-VIEW-PROJECTION MATRIX ---------------------------

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)