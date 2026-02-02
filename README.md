# PyCraft
An exercise in **Python** programming and rendering which creates **an interactable world in the style of Minecraft**.
It uses ctype functionality to use **C** variables and **OpenGL** to handle rendering.

*This project was originally created by* https://github.com/obiwac *on the YouTube series located at*
https://www.youtube.com/playlist?list=PL6_bLxRDFzoKjaa3qCGkwR5L_ouSreaVP.

## Table of Contents

1. Setup and Requirements
2. How I Explain the Code
3. What I Learned

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

#### Graphics

In this program, we are essentially rendering **vectors** which run from the origin to a **vertex**. These collections of *vertices* form shapes together. In this program we render Minecraft's squares using two **triangles**, since a triangle *is the simplest planar shape* that can be made, and we verifiably know that *all vertexes in a triangle are co-planar*. This simplifies calculation.

#### Memory

We start with the following to manage the **memory for rendering.** The descriptions come from 
https://developers-heaven.net/blog/vertex-buffers-and-vertex-arrays-sending-geometry-to-the-gpu/:

- Vertex Array Objects (VAOs): Allow switching between sets of vertex data and attribute configurations.
- Vertex Buffer Objects (VBOs): Memory regions on the GPU where you store vertex data, such as positions, normals, and texture coordinates.
- Index Buffer Objects (IBOs): An array of indices that point to vertices in a vertex buffer; allows for reordering and reusing vertex data.

#### Drawing

For example, to draw a square, we need four vertices to load into the vertex buffer object. These vertices are 3-tuples of *x, y, and z coordinates.*

Vertices:

|   x  |   y  |  z  |    Vertex    |
|------|------|-----|--------------|
| -0.5 |  0.5 | 0.0 |   Top Left   |
| -0.5 | -0.5 | 0.0 | Bottom Left  |
|  0.5 | -0.5 | 0.0 | Bottom Right |
|  0.5 |  0.5 | 0.0 |  Top Right   |

We will then create a list of indices to draw which *match to our vertices.* This is loaded into the index buffer object.

Indices:

| Index |    Vertex    | Triangle |
|-------|--------------|----------|
|   0   |   Top Left   |    ◣    |
|   1   | Bottom Left  |    ◣    |
|   2   | Bottom Right |    ◣    |
|   0   |   Top Left   |    ◥    |
|   2   | Bottom Right |    ◥    |
|   3   |  Top Right   |    ◥    |

We can use this command in the **on_draw method** of the Window class to render:

        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

Which draws triangles using our buffer data, together producing a square face.

If we want to draw a cube, it means drawing 12 triangles, two for each face. A total of 24 vertices, 4 per face, will need to be defined. The z coordinate will be used in this case.

The vertices and indices to render a cube can be found in *numbers.py*.

#### Shaders

Next, **shaders** convert input data into graphics outputs on the GPU. **Rasterization** is the process of converting our vector geometry into a raster image of pixels. Shaders are needed to control how this is rendered.

- Vertex Shaders run on each vertex. They control geometry for rasterization, determining which vertices are visible to the camera.
- Fragment Shaders run on each fragment, a group of pixels created by rasterization. They control colorization.

#### Matrices

If we want to move our rendered objects in real time, we need to use a **matrix** or **matrices** to modify our vertices.
This following description of vertices derives from the YouTube tutorial and https://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/:

- In rendering, the "camera" does not move - the scene is transformed around the viewport to simulate motion.
- Each vertex in the scene can be represented as a vector from the origin.
- We transform the scene's vertices in a model matrix, and transform it around the camera in a view matrix.
- These are locked together into the modelview matrix, which by scaling and moving vertices simulate motion.
- A projection matrix handles field of view, compressing viewable  objects into the screen position. The farther from  the camera, the more objects can be seen, but they must be rendered as smaller.
- A matrix has x, y, and z components to transform a set of vertices and produce motion effects. It also has a fourth component, w. The axis which extends straight out from the camera is the W or depth component axis. This lets us know which objects are in front of others.
- In OpenGL, matrices are separated by column into the xyzw components.
- Thus, Projection x ModelView = ModelViewProjection matrix x Vertex vector = 3D Rendering!

#### Textures

We will pass a **texture sampler** to our fragment shader. However, the amount of textures we can have is tied to the amount of texture units in the GPU. To solve this, we use a **texture array**. This will stack textures on top of one another in a 3D data storage object. *We access different textures using the z component of the texture array.*

We also generate mipmaps - creating smaller versions of each texture to be used as the distance of the texture from our camera increases.

## 3. What I Learned