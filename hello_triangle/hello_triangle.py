if __name__ == '__main__':
    import sys
    import glfw
    import OpenGL.GL as gl

    def on_key(window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window,1)

    # Initialize the library
    if not glfw.init():
        sys.exit()

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Make the window's context current
    glfw.make_context_current(window)

    # Install a key handler
    glfw.set_key_callback(window, on_key)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here
        width, height = glfw.get_framebuffer_size(window)
        ratio = width / float(height)
        gl.glViewport(0, 0, width, height)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-ratio, ratio, -1, 1, 1, -1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        # gl.glRotatef(glfw.get_time() * 50, 0, 0, 1)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3f(1, 0, 0)
        gl.glVertex3f(-0.6, -0.4, 0)
        gl.glColor3f(0, 1, 0)
        gl.glVertex3f(0.6, -0.4, 0)
        gl.glColor3f(0, 0, 1)
        gl.glVertex3f(0, 0.6, 0)
        gl.glEnd()

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()