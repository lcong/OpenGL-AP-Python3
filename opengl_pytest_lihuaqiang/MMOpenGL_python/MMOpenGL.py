#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import OpenGL.GL as gl
import glfw
import numpy as np

WIN_WIDTH = 800
WIN_HEIGHT = 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
out vec3 outPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    outPos = aPos;
}
"""

fragmentShaderSource = """
#version 330 core
out vec4 FragColor;
in vec3 outPos;
void main()
{
    FragColor = vec4(outPos, 1.0);
}
"""

vertices = np.array([-0.5, -0.5, 0.0,
                     0.5,-0.5, 0.0,
                    0.0,0.5, 0,], dtype = np.float32)

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

    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "Hello OpenGL", None, None)
    if window == 0:
        print("failed to create window")
        glfw.glfwTerminate()

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vertexShaderSource)
    gl.glCompileShader(vertexShader)

    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragmentShaderSource)
    gl.glCompileShader(fragmentShader)

    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)

    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(gl.glGetAttribLocation(shaderProgram, 'aPos'), 3, gl.GL_FLOAT, gl.GL_FALSE, 12, None)
    gl.glEnableVertexAttribArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    while not glfw.window_should_close(window):
        processInput(window)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shaderProgram)
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)

        glfw.swap_buffers(window)
        glfw.poll_events()


    glfw.terminate()

if __name__ == "__main__":
    main()