import sys, os
import OpenGL.GL as gl
import glfw
import numpy as np

WIN_WIDTH = 800
WIN_HEIGHT = 600

triangle = np.array([-0.25, -0.25, 0.5,
                     -0.25, -0.25, 0.5,
                     -0.25, 0.25, 0.5,
                     0.25, 0.25, 0.5], dtype=np.float32)

vertexShaderSource = """
#version 420 core
layout(location = 0) in vec3 pos;
void main(void)
{
	gl_Position =vec4(pos.x,pos.y,pos.z,1.0);	
}
"""

fragmentShaderSource = """
#version 420 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0,0.0,0.0, 1.0);
}
"""
tcsShaderSource = """
#version 420 core
layout(vertices = 4) out;
void main(void)
{
	if (gl_InvocationID == 0)
    {
		gl_TessLevelInner[0] = 2.0;
		gl_TessLevelOuter[0] = 2.0;
		gl_TessLevelOuter[1] = 2.0;
		gl_TessLevelOuter[2] = 2.0;
	}
	gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
}

"""

tesShaderSource = """
#version 420 core
layout(triangles, equal_spacing, cw) in;
void main(void)
{
	gl_Position = (gl_TessCoord.x * gl_in[0].gl_Position) +
	              (gl_TessCoord.y * gl_in[1].gl_Position) +
	              (gl_TessCoord.z * gl_in[2].gl_Position);
}

"""


geometryShaderSource = """
#version 420 core
layout(triangles) in;
layout(points,max_vertices = 3) out;
void main()
{	
	gl_Position = gl_in[0].gl_Position + vec4(-0.1, 0.0, 0.0, 0.0);
	EmitVertex();
	gl_Position = gl_in[0].gl_Position + vec4(0.0, 0.1, 0.0, 0.0);
	EmitVertex();
	EndPrimitive();

	gl_Position = gl_in[1].gl_Position + vec4(-0.1, 0.0, 0.0, 0.0);
	EmitVertex();
	gl_Position = gl_in[1].gl_Position + vec4(0.0, 0.1, 0.0, 0.0);
	EmitVertex();
	EndPrimitive();

	gl_Position = gl_in[2].gl_Position + vec4(0.1, 0.0, 0.0, 0.0);
	EmitVertex();
	gl_Position = gl_in[2].gl_Position + vec4(0.0, 0.1, 0.0, 0.0);
	EmitVertex();
	EndPrimitive();
}
"""


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
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "Gs Triangle", None, None)
    if window == 0:
        print("failed to create window")
        glfw.glfwTerminate()

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vertexShaderSource)
    gl.glCompileShader(vertexShader)

    tcsShader = gl.glCreateShader(gl.GL_TESS_CONTROL_SHADER)
    gl.glShaderSource(tcsShader, tcsShaderSource)
    gl.glCompileShader(tcsShader)

    tesShader = gl.glCreateShader(gl.GL_TESS_EVALUATION_SHADER)
    gl.glShaderSource(tesShader, tesShaderSource)
    gl.glCompileShader(tesShader)

    geometryShader = gl.glCreateShader(gl.GL_GEOMETRY_SHADER)
    gl.glShaderSource(geometryShader, geometryShaderSource)
    gl.glCompileShader(geometryShader)

    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragmentShaderSource)
    gl.glCompileShader(fragmentShader)



    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    #gl.glAttachShader(shaderProgram, tcsShader)
    #gl.glAttachShader(shaderProgram, tesShader)
    gl.glAttachShader(shaderProgram, geometryShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)
    #gl.glDeleteShader(tesShader)
    #gl.glDeleteShader(tcsShader)
    gl.glDeleteShader(geometryShader)

    #gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4);
    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)

    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(triangle), triangle, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,3*sys.getsizeof(float), None)
    gl.glEnableVertexAttribArray(0)

    # 解除VAO VBO绑定
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
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