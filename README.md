# PyCraft
An exercise in **Python** programming and rendering which creates **an interactable world in the style of Minecraft**.
It uses ctype functionality to use **C** variables and **OpenGL** to handle rendering.

*This project was originally created by* https://github.com/obiwac *on the YouTube series located at*
https://www.youtube.com/playlist?list=PL6_bLxRDFzoKjaa3qCGkwR5L_ouSreaVP.

## Table of Contents

1. Setup and Requirements
2. How I Explain the Code
3. Tools Used

## 1. Setup and Requirements

This is the setup procedure I followed for this project.

You need Python to be installed on your device - I had version 3.13.5.

The graphical library I used is **pyglet**. You can install it in the terminal using *pip*, the standard package manager for Python. Install pyglet and update pip below:

    pip install --user pyglet
    python -m pip install --upgrade pip

Test your installation using these lines. It should not throw errors:

    python
    import pyglet
    exit()

I used **Visual Studio** and **VSCode** to develop the code.

In order to make the shaders, I had to install **OpenGL**. The Open Graphics Library is a cross-platform API for vector graphics rendering. We need this for more complex graphics. *Pyglet has OpenGL functionality already, but I wanted to be safe.* To use it with Python, use:
    
    pip install PyOpenGL

I had to install **GLSL Syntax** for VS Code to apply syntax highlighting to GL Shader Language files. These shaders are essential for this project.

## 2.  How I Explain the Code

### Graphics

In this program, we are essentially rendering **vectors** which run from the origin to a **vertex**. These collections of *vertices* form shapes together. In this program we render Minecraft's squares using two **triangles**, since a triangle *is the simplest planar shape* that can be made, and we verifiably know that *all vertexes in a triangle are co-planar*. This simplifies calculation.

**Vector graphics** create images directly from mathematical computations of geometric shapes. This is exactly what we need for 3D rendering blocks or *voxels*, where the mathematical information of the cubes can be recorded with accuracy. However, since computer monitors use **raster** graphics, where images are created from a set of pixel colors, our *vector graphics* must undergo **rasterization** to convert our mathematical information to a set of pixels.

### Memory

We start with the following to manage the **memory for rendering.** The descriptions come from 
https://developers-heaven.net/blog/vertex-buffers-and-vertex-arrays-sending-geometry-to-the-gpu/:

- Vertex Array Objects (VAOs): Allow switching between sets of vertex data and attribute configurations. It holds references to the vertex buffers and the index buffer rather than actual data.
- Vertex Buffer Objects (VBOs): Memory regions on the GPU where you store vertex data, such as positions, normals, and texture coordinates. Multiple VBOs may be used, such as one for vertex positions and one for texture coordinates in this project.
- Index Buffer Objects (IBOs): An array of indices which map to vertices in a vertex buffer. This allows us to access vertex coordinates with an index, which can be reused if mutiple vectors need to be drawn from a single vertex.

### Drawing

For example, to draw a square, we need four vertices to load into the vertex buffer object. These vertices are 3-tuples of *x, y, and z coordinates.*

Vertices:

|   x  |   y  |  z  |    Vertex    |
|------|------|-----|--------------|
| -0.5 |  0.5 | 1.0 |   Top Left   |
| -0.5 | -0.5 | 1.0 | Bottom Left  |
|  0.5 | -0.5 | 1.0 | Bottom Right |
|  0.5 |  0.5 | 1.0 |  Top Right   |

We will then create a list of *indices* to draw which *match to our vertices.* This is loaded into the index buffer object. You can see that we are reusing some of the indices, since we have a vertex which serves as the starting point for more than one vector.

Indices:

| Index |    Vertex    | Triangle |
|-------|--------------|----------|
|   0   |   Top Left   |    •     |
|   1   | Bottom Left  |    ↓     |
|   2   | Bottom Right | ↓➝ = ◣  |
|   0   |   Top Left   |    •     |
|   2   | Bottom Right |    ➘     |
|   3   |  Top Right   | ➘↑ = ◥  |
|       |              | ◣+◥ = ⬔ |

Here's what that looks like in Python:

        vertex_positions = [
            -0.5, 0.5, 1.0,
            -0.5, -0.5, 1.0,
            0.5, -0.5, 1.0,
            0.5, 0.5, 1.0,
        ]

        indices = [
            0, 1, 2,  # first triangle
            0, 2, 3,  # second triangle
        ]


We can use this command in the **on_draw method** of the Window class to render:

        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

Which draws triangles using our buffer data, together producing a square face.

If we want to draw a cube, it means drawing 12 triangles, two for each face. A total of 24 vertices, 4 per face, will need to be defined. The z coordinate will be used in this case.

The vertices and indices to render a cube can be found in *numbers.py*.

There are also some window settings we need to use from pyglet:

        gl.glEnable(gl.GL_DEPTH_TEST)
        
This enables depth.
        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

This clears depth bits for the screen.

        double_buffer = True 
        
A buffer is a region of memory - double buffering renders a new image to the "back" while displaying the "front" and then switches out, to prevent incomplete renders.

        depth_size = 16
        
This will prevent back faces from rendering over front.

### Matrices

If we want to move our rendered objects in real time, we need to use a **matrix** or **matrices** to modify our vertices.
This following description of vertices derives from the YouTube tutorial and https://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/:

A matrix has x, y, and z components to transform a set of vertices and produce motion effects. It also has a fourth component, w. If w is 0, then the coordinates represent a direction. If w is 1, it is a position in the world space. In OpenGL, matrices are separated by column into the xyzw components.

In rendering, the "camera" does not move - **the scene is transformed around the viewport** to simulate motion. We transform the scene's vertices in a *model matrix*, and transform it around the camera in a view *matrix*. These are locked together into the modelview matrix, which by **scaling and moving vertices simulate motion.** A *projection matrix* handles field of view, compressing viewable objects into the screen position. The farther from  the camera, the more objects can be seen, but they must be rendered as smaller.

To sum it up, Projection (FOV) x ModelView (Scene-Camera) = ModelViewProjection. ModelViewProjection x a Vertex vector = 3D Movement!

Matrices work in OpenGL like this:

<table>
<tr><td>

|   |   |   |   |
|---|---|---|---|
| a | b | c | d | 
| e | f | g | h |
| i | j | k | l | 
| m | n | o | p |

</td><td>×</td><td>

|   |
|---|
| x |
| y |
| z |
| w |

</td><td>=</td><td>

|   |
|---|
| ax + by + cz + dw | 
| ex + fy + gz + hw |
| ix + jy + kz + lw | 
| mx + ny + oz + pw |

</td></tr> </table>

Here are some common types of matrices:

<table>
<tr><th>Identity Matrix</th><th>Translation Matrix</th><th>Scaling Matrix</th></tr>
<tr>
<td>Often used as the default value of a new matrix, this simply multiplies all existing coordinates in a vector or position by 1.</td>
<td>Used to transform a vector or position by moving it a set amount. Useful when moving shapes across the screen. An identity matrix is just a translation matrix with an offset of 0 for X, Y, and Z.</td>
<td>Can scale a vector or position up or down, to make it larger or smaller. Useful in depth rendering when a rendered shapes moves closer or farther in relation to the player.</td>
</tr>
<tr><td>

|   |   |   |   |
|---|---|---|---|
| 1 | 0 | 0 | 0 | 
| 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 
| 0 | 0 | 0 | 1 |

</td><td>

|   |   |   |   |
|---|---|---|---|
| 1 | 0 | 0 | X | 
| 0 | 1 | 0 | Y |
| 0 | 0 | 1 | Z | 
| 0 | 0 | 0 | 1 |

</td><td>

|   |   |   |   |
|---|---|---|---|
| X | 0 | 0 | 0 | 
| 0 | Y | 0 | 0 |
| 0 | 0 | Z | 0 | 
| 0 | 0 | 0 | 1 |

</td></tr> </table>

EXAMPLE: Use a transform matrix to move the starting coordinates (10,10,10,1) by 10 in the X direction. 

**(X-Offset = 10)**

<table>
<tr><td>

|   |   |   |   |
|---|---|---|---|
| 1 | 0 | 0 | 10 | 
| 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 
| 0 | 0 | 0 | 1 |

</td><td>×</td><td>

|   |
|---|
| 10 |
| 10 |
| 10 |
| 1 |

</td><td>=</td><td>

|   |
|---|
| 1×10 + 0 + 0 + 10×1 | 
| 0 + 1×10 + 0 + 0 |
| 0 + 0 + 1×10 + 0 | 
| 0 + 0 + 0 + 1×1 |

</td><td>=</td><td>

|   |
|---|
| 20 |
| 10 |
| 10 |
| 1 |

</td></tr> </table>


EXAMPLE: Use a scaling matrix to multiply the starting vector (10,10,10,0) by 2 in all directions. 

**(X-Scale = 2, Y-Scale = 2, Z-Scale = 2)**

<table>
<tr><td>

|   |   |   |   |
|---|---|---|---|
| 2 | 0 | 0 | 0 | 
| 0 | 2 | 0 | 0 |
| 0 | 0 | 2 | 0 | 
| 0 | 0 | 0 | 1 |

</td><td>×</td><td>

|   |
|---|
| 10 |
| 10 |
| 10 |
| 0 |

</td><td>=</td><td>

|   |
|---|
| 2×10 + 0 + 0 + 0 | 
| 0 + 2×10 + 0 + 0 |
| 0 + 0 + 2×10 + 0 | 
| 0 + 0 + 0 + 1×0 |

</td><td>=</td><td>

|   |
|---|
| 20 |
| 20 |
| 20 |
| 0 |

</td></tr> </table>

**The code for the matrices can be found in matrix.py.**

### Shaders

**Shaders** convert input data into graphics outputs on the GPU. **Rasterization** is the process of converting our vector geometry into a raster image of pixels. Shaders are needed to control how this is rendered. Our shaders are *vert.glsl* and *frag.glsl*.

- Vertex Shaders run on each vertex. They control geometry for rasterization, determining which vertices are visible to the camera.
- Fragment Shaders run on each fragment. This is a group of pixels created by rasterization, which can be colorized or have textures mapped onto them.

We use **shader uniforms**, global variables, to pass data to the shader. An example is our fragment shader, which takes in texture coordinates as a uniform. 

**Important!** Though we handle the mathematical computations of making the matrices in our code, **we actually apply the matrices in the shading process.** We pass our matrix as *uniform* into a **vertex shader**, which is described in the next section.

For example, in the main method of a GL Shader Language (GLSL) file:

        gl_Position = matrix * vec4(vertex_position, 1.0);

### Textures

We will pass a **texture sampler** to our fragment shader. However, the amount of textures we can have is tied to the amount of texture units in the GPU. To solve this, we use a **texture array**. This will stack textures on top of one another in a 3D data storage object. *We access different textures using the z component of the texture array.*

We also generate mipmaps - creating smaller versions of each texture to be used as the distance of the texture from our camera increases.

The fragment shader uses this to output colors as a *4d vector*. If our fragment shader outputs a value using **out vec4 fragment_color;** then in the **void main(void)** function we may use any of the following.

If we pass in local_position then this outputs a multicolor texture:

        fragment_color = vec4(local_position / 2.0 + 0.5, 1.0);

This colors our shape the same color as the middle pixel(s) of a texture. Here we pass in our 3D texture array as *texture_array_sampler*. The vector3 uses 0.5, 0.5, to reference the middle of the texture, and the *Z coordinate of 0.0 is the first texture in the array.*:

        fragment_color = texture(texture_array_sampler, vec3(0.5, 0.5, 0.0));

This will cast a texture onto our block. To sample the texture at different places depending on where the fragment is on the block face, we use a different texture coordinate for each vertex and interpolate between them for each fragment. For example, from left to right we might go from left:0 to right:1 by increments:

        fragment_color = texture(texture_array_sampler, interpolated_tex_coords);

In our texture manager, this will fix the blurriness caused by the previous implementation. It will stop OpenGL from linear interpolation of neighboring pixels, instead selecting the nearest pixel's color when sampling:

        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

*Our block script must change the array of* **tex_coords** *if certain faces need different textures than the rest of the block.*

#### Input

For mouse captures. In __init__ for window:

        self.mouse_captured = False

Then use: 

        #
        # on_mouse_press - Called when mouse is pressed.
        #
        def on_mouse_press(self, x, y, button, modifiers):
            self.mouse_captured = not self.mouse_captured
            self.set_exclusive_mouse(self.mouse_captured)

## 3. Tools Used

- import math
- import ctypes: allows you to manipulate C types
- import pyglet: provides windowing, game control, and display
- import pyglet.gl as gl: reference for Open Graphics Library (OpenGL)