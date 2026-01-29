import pyglet

pyglet.options["shadow window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

class Window(pyglet.window.Window):
    def __init__(self, **args):
        super(Window, self).__init__(**args)
    
    def on_draw(self):
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.clear()
    
    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")

class Game:
    def __init__(self):
        # Had to add "double_buffer = True" to get screen to work.
        self.config = gl.Config(major_version = 3, double_buffer=True)
        self.window = Window(config = self.config, width=800, height=600, caption="PyCraft", resizable=True, vsync=False)
        
    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()