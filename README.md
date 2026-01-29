# PyCraft
An exercise in **Python** programming and rendering which creates **an interactable world in the style of Minecraft**.
It uses ctype functionality to use **C** variables and **OpenGL** to handle rendering.

*This project was originally created by* https://github.com/obiwac *on the YouTube series located at*
https://www.youtube.com/playlist?list=PL6_bLxRDFzoKjaa3qCGkwR5L_ouSreaVP.

## Table of Contents

1. Setup and Requirements
2. How I Explain the Code
3. What I Learned

### 1. Setup and Requirements

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

In order to make the shaders, I had to install **OpenGL**. The Open Graphics Library is a cross-platform APL for vector graphics rendering. We need this for more complex graphics. *Pyglet has OpenGL functionality already, but I wanted to be safe.* To use it with Python, use:
    
    pip install PyOpenGL

I had to install **GLSL Syntax** for VS Code to apply syntax highlighting to GL Shader Language files. These shaders are essential for this project.

### 2.  How I Explain the Code



### 3. What I Learned