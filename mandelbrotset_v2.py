import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from pathlib import Path
import os

# Initialize global variables
last_time = time.time()
frame_count = 0
fps = 0
zoom = 1
move_x, move_y = -0.3, 0.0
gen_x, gen_y = 0, 0
fine = False
colorMode = [1,1,1]
i = 0
debug = False
colorList = [[1,1,1], [1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1]]

# Shader compilation and program creation functions
def compile_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation failed: {error}")
    return shader

def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_source)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_source)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Shader linking failed: {error}")
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

# Function to create a square that takes up the whole screen
def square_fullscreen():
    vertices = np.array([
        -1.0, -1.0, 0.0,
        -1.0,  1.0, 0.0,
         1.0,  1.0, 0.0,
         1.0, -1.0, 0.0
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO, EBO

# Stats display function
def display_stats():
    global last_time, frame_count, fps
    current_time = time.time()
    frame_count += 1
    time_difference = current_time - last_time
    if time_difference >= 1.0:
        fps = frame_count / time_difference
        frame_count = 0
        last_time = current_time

    glUseProgram(0)  # Unbind any active shader programs

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glRasterPos2f(10, glutGet(GLUT_WINDOW_HEIGHT) - 20)

    debug_text = [
        f"FPS: {int(fps)}",
        f"Zoom: {zoom:.2f}",
        f"Position: ({move_x:.2f}, {move_y:.2f})",
        "Fine mode: " + ("ON" if fine else "OFF"),
        ""]
    stats_text = [
        "WASD to move",
        "B to go back",
        "R to render image",
        "C to cycle color modes",
        "V to cycle color modes backwards",
        "F to toggle fine mode",
        "Q to toggle debug",
        "Esc to close window"]
    
    if debug:
        stats_text = debug_text + stats_text

    line_height = 20  # Adjust this value to change the spacing between lines
    for i, line in enumerate(stats_text):
        glRasterPos2f(10, glutGet(GLUT_WINDOW_HEIGHT) - 20 - (i * line_height))
        for char in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# Function to render the screen
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Render the Mandelbrot set
    glUseProgram(shader_program)
    
    # Update uniforms
    resolution_loc = glGetUniformLocation(shader_program, "resolution")
    time_loc = glGetUniformLocation(shader_program, "time")
    zoom_loc = glGetUniformLocation(shader_program, "zoom")
    move_loc = glGetUniformLocation(shader_program, "move")
    color_loc = glGetUniformLocation(shader_program, "colorMode")

    glUniform2f(resolution_loc, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    glUniform1f(time_loc, time.time())
    glUniform1f(zoom_loc, zoom)
    glUniform2f(move_loc, move_x, move_y)
    glUniform3f(color_loc, colorMode[0], colorMode[1], colorMode[2])
    
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    glUseProgram(0)  # Unbind the shader program
    
    # Render the FPS counter on top
    display_stats()
    
    glutSwapBuffers()

def render_mandelbrot_to_image(width, height, filename="mandelbrot"):
    # Create a framebuffer object
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    # Create a texture to render to
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Attach the texture to the framebuffer
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)

    # Check if framebuffer is complete
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        print("Framebuffer is not complete!")
        return

    # Set up the viewport and projection
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Clear the framebuffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Render the Mandelbrot set
    glUseProgram(shader_program)
    
    # Update uniforms
    resolution_loc = glGetUniformLocation(shader_program, "resolution")
    time_loc = glGetUniformLocation(shader_program, "time")
    zoom_loc = glGetUniformLocation(shader_program, "zoom")
    move_loc = glGetUniformLocation(shader_program, "move")
    color_loc = glGetUniformLocation(shader_program, "colorMode")

    glUniform2f(resolution_loc, width, height)
    glUniform1f(time_loc, time.time())
    glUniform1f(zoom_loc, zoom)
    glUniform2f(move_loc, move_x, move_y)
    glUniform3f(color_loc, colorMode[0], colorMode[1], colorMode[2])
    
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    glUseProgram(0)  # Unbind the shader program

    # Read the pixels from the framebuffer
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Save the image
    os.makedirs(Path("/img"), exist_ok=True)
    path = Path("img/"+filename+".png")
    counter = 0
    while path.is_file():
        counter += 1
        path = Path(f"img/{filename}-{counter:02d}.png")
    image.save(path)

    # Clean up
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteFramebuffers(1, [fbo])
    glDeleteTextures(1, [texture])

    print(f"Mandelbrot set image saved as {path}")

def keyboard(key, x, y):
    global move_y, move_x, zoom, fine, i, colorMode, debug
    c = 0.01
    if not fine:
        c *= zoom
    if key == b'w':
        move_y += c
    elif key == b's':
        move_y -= c
    elif key == b'a':
        move_x -= c
    elif key == b'd':
        move_x += c
    elif key == b'b':
        move_x, move_y, zoom = -0.3, 0.0, 1
    elif key == b'f':
        fine = not fine
    elif key == b'r':
        render_mandelbrot_to_image(1920, 1080, "mandelbrot_high_res")
    elif key == b'\x1b':  # ASCII code for Escape key
        glutDestroyWindow(wind)
        glutMainLoopEvent()
    elif key == b'c':
        i += 1
        i %= len(colorList)
        colorMode = colorList[i]
    elif key == b'v':
        i -= 1
        if i < 0:
            i = len(colorList)-1
        colorMode = colorList[i]
    elif key == b'q':
        debug = not debug
        

def mouse_wheel(button, dir, x, y):
    global zoom, move_x, move_y, gen_x, gen_y
    if dir > 0:
        zoom *= 1.1
    else:
        zoom /= 1.1
    
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    move_x += (x - window_width / 2) / (window_width / 2)# / zoom
    move_y += (window_height / 2 - y) / (window_height / 2)# / zoom


# Initialization and main loop
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(800, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Mandelbrot Set Viewer")

glutFullScreen()

vertex_shader_source = Path("colors.vert").read_text()
fragment_shader_source = Path("fragment.frag").read_text()

shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)
VAO, EBO = square_fullscreen()

glutKeyboardFunc(keyboard)
glutMouseWheelFunc(mouse_wheel)

glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)

glEnable(GL_DEPTH_TEST)

glutMainLoop()
