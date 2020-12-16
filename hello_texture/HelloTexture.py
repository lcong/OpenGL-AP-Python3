#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

import OpenGL.GL as gl
import glfw
from ShaderProgram import ShaderProgram
import numpy as np
from ctypes import c_void_p
from PIL import Image

class MyShaderProgram(ShaderProgram):
    def __init__(self, vertPath="vertexShader.glsl", fragPath="fragmentShader.glsl"):
        super().__init__(vertPath, fragPath)

    def use(self):
        gl.glUseProgram(self.program_id)

WIN_WIDTH = 800
WIN_HEIGHT = 600

vertices = np.array([0.5, 0.5, 0,    1.0, 0.0, 0.0,   1.0, 1.0,
                     0.5,-0.5, 0,    0.0, 1.0, 0.0,   1.0, 0.0,
                    -0.5,-0.5, 0,    0.0, 0.0, 1.0,   0.0, 0.0,
                    -0.5, 0.5, 0,    1.0, 1.0, 0.0,   0.0, 1.0], dtype = np.float32)

indices = np.array([0, 1, 3,
                    1, 2, 3], dtype = np.uint32)

def framebuffer_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)

def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.glfwSetWindowShouldClose()

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "学习OpenGL", None, None)
    if window == 0:
        print("failed to create window")
        glfw.terminate()

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    myShaderProg = MyShaderProgram()

    VAO = gl.glGenVertexArrays(1)
    VBO, EBO = gl.glGenBuffers(2)

    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, gl.GL_STATIC_DRAW)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(indices), indices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 32, c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 32, c_void_p(12))
    gl.glEnableVertexAttribArray(1)
    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 32, c_void_p(24))
    gl.glEnableVertexAttribArray(2)

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    img = Image.open("container.jpg")
    width, height = img.size
    data = np.array(list(img.getdata()), dtype=np.uint8)

    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, data)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    while not glfw.window_should_close(window):
        processInput(window)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        myShaderProg.use()

        gl.glBindVertexArray(VAO)
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()