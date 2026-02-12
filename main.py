import math
import ctypes
import pyglet
import pyglet.gl as gl
import matrix
import shader
import block
import texture_manager
import camera
import chunk
import world

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

#
# Window - Overloads Pyglet Window. Calls super() to initialize the 
# window and additionally instantiates the necessary graphical 
# components for our specific rendering purposes.
#
class Window(pyglet.window.Window):

    #
    # __init__ - Constructor, on instantiation of a Window object.
    #
    def __init__(self, **args): 
        
        super().__init__(**args) # creates pyglet window

        #### create world ###########################################

        self.world = world.World()

        #### create shaders #########################################

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_sampler_location = self.shader.find_uniform(b"texture_array_sampler")
        self.shader.use()

        #### set window settings ####################################

        pyglet.clock.schedule_interval(self.update, 1.0 / 60) # framerate = 60fps
        self.mouse_captured = False

        #### camera setup ###########################################

        self.camera = camera.Camera(self.shader, self.width, self.height, )

    #
    # update - Runs every scheduled interval to perform some function.
    #
    def update(self, delta_time):
        #print(f"FPS: {1.0/delta_time}")
        if not self.mouse_captured: self.camera.input = [0,0,0]
        self.camera.update_camera(delta_time)
    
    #
    # on_draw - Called every frame to redraw the contents of our window. 
    # Responsible for graphical rendering.
    #
    def on_draw(self):
        self.camera.update_matrices()
        
        #### bind textures ##########################################

        gl.glActiveTexture(gl.GL_TEXTURE0) # first texture unit
        # bind our texture manager's texture
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.world.texture_manager.texture_array)
        # tell sampler that the texture is bound to the first texture unit
        gl.glUniform1i(self.shader_sampler_location, 0)
        
        #### draw shapes ############################################

        gl.glEnable(gl.GL_DEPTH_TEST) # Enables depth
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT) # clears depth bits for screen
        gl.glEnable(gl.GL_CULL_FACE) # Enables back face culling
        gl.glClearColor(0.0, 0.0, 0.0, 1.0) # Sets screen color
        self.clear()

        self.world.draw()

        gl.glFinish()
    
    #
    # on_resize - Called when window changes size.
    #
    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        #gl.glViewport(0,0,width,height)
        self.camera.width = width
        self.camera.height = height

    #
    # on_mouse_press - Called when mouse is pressed.
    #
    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_captured = not self.mouse_captured
        self.set_exclusive_mouse(self.mouse_captured)

    #
    # on_mouse_motion - Called when mouse is moved.
    #
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        if self.mouse_captured:
            sensitivity = 0.004

            self.camera.rotation[0] -= delta_x * sensitivity
            self.camera.rotation[1] += delta_y * sensitivity
            # ensure y rotation does not exceed quarter from normal in either direction
            self.camera.rotation[1] = max(-math.tau/4, min(math.tau/4, self.camera.rotation[1]))

    #
    # on_key_press - Called upon keyboard input.
    #
    def on_key_press(self, key, modifiers):
        if not self.mouse_captured: return

        if key == pyglet.window.key.D or key == pyglet.window.key.RIGHT: self.camera.input[0] += 1 # RIGHT
        elif key == pyglet.window.key.A or key == pyglet.window.key.LEFT: self.camera.input[0] -= 1 # LEFT
        elif key == pyglet.window.key.W or key == pyglet.window.key.UP: self.camera.input[2] += 1 # FORWARD
        elif key == pyglet.window.key.S or key == pyglet.window.key.DOWN: self.camera.input[2] -= 1 # BACK
        elif key == pyglet.window.key.SPACE or key == pyglet.window.key.ENTER: self.camera.input[1] += 1 # UP
        elif key == pyglet.window.key.LSHIFT or key == pyglet.window.key.RSHIFT: self.camera.input[1] -= 1 # DOWN

    #
    # on_key_release - Called upon keyboard release, stops motion. Resets input to 0.
    #
    def on_key_release(self, key, modifiers):
        if not self.mouse_captured: return

        if key == pyglet.window.key.D or key == pyglet.window.key.RIGHT: self.camera.input[0] -= 1 # RIGHT
        elif key == pyglet.window.key.A or key == pyglet.window.key.LEFT: self.camera.input[0] += 1 # LEFT
        elif key == pyglet.window.key.W or key == pyglet.window.key.UP: self.camera.input[2] -= 1 # FORWARD
        elif key == pyglet.window.key.S or key == pyglet.window.key.DOWN: self.camera.input[2] += 1 # BACK
        elif key == pyglet.window.key.SPACE or key == pyglet.window.key.ENTER: self.camera.input[1] -= 1 # UP
        elif key == pyglet.window.key.LSHIFT or key == pyglet.window.key.RSHIFT: self.camera.input[1] += 1 # DOWN


#
# Game - Class which runs the PyCraft simulation. Configures graphical 
# settings and creates a Window object for displaying graphics.
#
class Game:
    
    #
    # __init__ - Constructor, on instantiation of the game.
    #
    def __init__(self):
        self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3, depth_size = 16)
        self.window = Window(config = self.config, width=800, height=600, caption="PyCraft", resizable=True, vsync=False)

    #
    # run - Starts the game.
    #  
    def run(self):
        pyglet.app.run()


#
# Allows main.py to create an instance of 
# the Game class and run it.
#
if __name__ == "__main__":
    game = Game()
    game.run()