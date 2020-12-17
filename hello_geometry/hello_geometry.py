#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import OpenGL.GL as gl
import glfw
import numpy as np

WIN_WIDTH = 800
WIN_HEIGHT = 600

vertexShaderSource = """
#version 420 core
layout (location = 0) in vec4 aPos;
vec4 aTempPos=aPos;
void main()
{
    gl_Position = vec4(aTempPos.x, aTempPos.y, aTempPos.z, aTempPos.w);
}
"""

geometryShaderSource = """
# version 420 core\n
layout(lines) in;
layout(line_strip, max_vertices=4) out;
void main()
{
    gl_Position = gl_in[0].gl_Position + vec4(-0.1, 0.0, 0.0, 0.0);
    EmitVertex();
    gl_Position = gl_in[0].gl_Position + vec4(0.1, 0.0, 0.0, 0.0);
    EmitVertex();
    EndPrimitive();

    gl_Position = gl_in[1].gl_Position + vec4(0.2, 0.0, 0.0, 0.0);
    EmitVertex();
    gl_Position = gl_in[1].gl_Position + vec4(-0.2, 0.0, 0.0, 0.0);
    EmitVertex();
    EndPrimitive();
}
"""

fragmentShaderSource = """
#version 420 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

vertices = np.array([0.5, 0.5, 0, 1,
					 0.5, -0.5, 0, 1,
					 -0.5, -0.5, 0, 1,
					 -0.5, 0.5, 0, 1], dtype=np.float32)

indices = np.array([0, 1, 3,
				   1, 2, 3], dtype=np.uint32)


def framebuffer_size_callback(window, width, height):
	gl.glViewport(0, 0, width, height)


def processInput(window):
	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		glfw.set_window_should_close()

	if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

	if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)


def main():
	glfw.init()
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "Hello Geometry", None, None)
	if window == 0:
		print("failed to create window")
		glfw.terminate()

	glfw.make_context_current(window)
	glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

	vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
	gl.glShaderSource(vertexShader, vertexShaderSource)
	gl.glCompileShader(vertexShader)

	fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
	gl.glShaderSource(fragmentShader, fragmentShaderSource)
	gl.glCompileShader(fragmentShader)

	vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
	gl.glShaderSource(vertexShader, vertexShaderSource)
	gl.glCompileShader(vertexShader)

	geometryShader = gl.glCreateShader(gl.GL_GEOMETRY_SHADER)
	gl.glShaderSource(geometryShader, geometryShaderSource)
	gl.glCompileShader(geometryShader)

	shaderProgram = gl.glCreateProgram()
	gl.glAttachShader(shaderProgram, vertexShader)
	gl.glAttachShader(shaderProgram, fragmentShader)
	gl.glAttachShader(shaderProgram, geometryShader)


	gl.glLinkProgram(shaderProgram)

	gl.glDeleteShader(vertexShader)
	gl.glDeleteShader(fragmentShader)
	gl.glDeleteShader(geometryShader)

	VAO = gl.glGenVertexArrays(1)
	VBO, EBO = gl.glGenBuffers(2)

	gl.glBindVertexArray(VAO)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, gl.GL_STATIC_DRAW)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(indices), indices, gl.GL_STATIC_DRAW)

	gl.glVertexAttribPointer(gl.glGetAttribLocation(shaderProgram, 'aPos'), 4, gl.GL_FLOAT, gl.GL_FALSE, 16, None)
	gl.glEnableVertexAttribArray(0)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
	gl.glBindVertexArray(0)

	while not glfw.window_should_close(window):
		processInput(window)
		gl.glClearColor(0.2, 0.3, 0.3, 1.0)
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)

		gl.glUseProgram(shaderProgram)
		gl.glBindVertexArray(VAO)
	#	gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)
		gl.glDrawArrays(gl.GL_LINES, 0, 4)

		glfw.swap_buffers(window)
		glfw.poll_events()

	glfw.terminate()

if __name__ == "__main__":
	main()
