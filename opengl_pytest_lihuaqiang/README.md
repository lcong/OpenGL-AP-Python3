# MMOpenGL_python

# 使用vs 与fs，将顶点数据渲染成三角形并着色

# GsLineToTriangle

使用gl.glDrawArrays(gl.GL_LINES, 0, 2)，将2个顶点数据传入gs，输出2个Triangle

# GsTriangleToTriangle

使用gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)，将3个顶点数据传入gs，输出3个Triangle

# GsPointToTriangle

使用gl.glDrawArrays(gl.GL_POINTS, 0, 4), 将4个顶点数据传入gs,输出4个Triangle

# GsTriangleToLine

使用gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3) 将3个顶点数据传入gs,输出3条Line

# GsTriangleToPoint

使用gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3) 将3个顶点数据传入gs,输出3个point

# TesTcsTriangle

tes、tcs的简单测试。gl.glDrawArrays(gl.GL_PATCHES, 0, 3)细分三角形。