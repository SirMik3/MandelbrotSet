
# Mandelbrot Set Renderer

This repository contains a Python-based application to render and explore the Mandelbrot set using OpenGL and GLSL shaders. It employs vertex and fragment shaders to efficiently render the Mandelbrot fractal, providing a highly customizable visual experience with zoom capabilities, color schemes, and precision adjustments.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Shader Details](#shader-details)
  - [Vertex Shader](#vertex-shader)
  - [Fragment Shader](#fragment-shader)
- [Mandelbrot Set Explained](#mandelbrot-set-explained)
- [Customization](#customization)
- [Advanced Features](#advanced-features)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The **Mandelbrot Set** is a mathematical fractal named after Benoît Mandelbrot. This project visualizes the Mandelbrot set in real-time using modern OpenGL shaders, allowing users to interactively explore the fractal's infinite complexity. By leveraging GPU computing power, this implementation renders high-resolution views of the fractal, with adjustable color schemes and zoom capabilities for deep exploration of the set's intricate details.

## Installation

### Prerequisites

Before running the project, ensure that you have the following installed on your machine:

- Python 3.6 or higher
- OpenGL-compatible graphics card with GLSL shader support

You can install the required Python libraries using `pip`:

```bash
pip install numpy PyOpenGL glfw
```

### OpenGL Setup

Ensure that your system supports OpenGL, and the necessary drivers are up to date. This is especially important for smooth rendering and shader support.

## Usage

To start the Mandelbrot renderer, run the following command in your terminal:

```bash
python mandelbrotset_v2.py
```

Once the program starts, a window will open, displaying the Mandelbrot set. You can interact with the visualization in the following ways:

- **Zoom in/out**: Use the scroll wheel of your mouse or touchpad to zoom into or out of the fractal.
- **Pan the view**: Click and drag with your mouse to move around the fractal.
- **Reset view**: Press the `B` (back) key to reset the view to the default zoom level and position.

For advanced users, command-line arguments or configuration files may be used in future versions to set initial parameters like zoom level, iteration depth, and color schemes.

## Repository Structure

The repository is organized as follows:

- **`mandelbrotset_v2.py`**: This is the core Python script. It sets up the OpenGL context, initializes the GLFW window, and handles input and rendering calls. It also compiles the vertex and fragment shaders.
- **`colors.vert`**: This GLSL vertex shader manages the basic geometry of the view and passes data (such as vertex coordinates) to the fragment shader. In this case, it doesn't perform heavy transformations but serves as the entry point to the GPU rendering pipeline.
- **`fragment.frag`**: The fragment shader is responsible for computing whether each pixel in the window belongs to the Mandelbrot set. It calculates the escape time for each point in the complex plane and assigns colors based on this value, creating the fractal's visual patterns.

## Shader Details

### Vertex Shader (`colors.vert`)

The vertex shader processes each vertex in the scene, preparing the necessary data for the fragment shader. Since we're rendering a full-screen quad to display the fractal, the vertex shader's primary role is minimal, passing coordinates and any required uniform values.

### Fragment Shader (`fragment.frag`)

The fragment shader handles the core computation for rendering the Mandelbrot set. For each pixel on the screen, it calculates whether the corresponding complex number diverges under iteration of the Mandelbrot function:

$$z_{n+1} = z_n^2 + c$$

Where $$c$$ is a complex number representing the point on the complex plane corresponding to the pixel, and $$z_0 = 0$$. The shader iterates this function for each pixel and assigns a color based on how quickly the point "escapes" to infinity, or if it remains within a bounded region (part of the Mandelbrot set).

#### Key Parameters in the Shader:

- **Max Iterations**: Controls the level of detail in the fractal. Higher values increase precision but may reduce performance.
- **Escape Radius**: Determines how quickly a point is deemed to have "escaped" the Mandelbrot set.
- **Color Mapping**: The color assigned to each pixel is based on the number of iterations before escape or if the point remains in the set.

## Mandelbrot Set Explained

The **Mandelbrot Set** is a collection of points in the complex plane. It is defined by the behavior of the function:

$$f(z) = z^2 + c$$

Starting with $$z = 0$$, we apply the function iteratively, checking whether the value remains bounded. If it does, the point $$c$$ is part of the Mandelbrot set. Otherwise, it "escapes" to infinity, and we assign a color based on how fast this escape happens.

One of the most fascinating aspects of the Mandelbrot set is its infinite complexity. No matter how much you zoom in, new patterns emerge, revealing intricate, self-similar structures.

## Customization

This project is designed to be highly customizable. You can tweak various parameters to control how the Mandelbrot set is rendered:

- **Iteration Depth**: Modify the `max_iterations` value in the Python or shader code to increase the fractal's detail level.
- **Color Scheme**: The colors are determined by escape time and can be customized by altering the color functions in `fragment.frag`. Experiment with different gradient techniques to achieve unique visual effects.
- **Zoom Speed**: You can adjust the zoom speed in the Python file to change how quickly the fractal zooms in and out.

## Advanced Features

Here are some features that can be added or customized further:

- **Dynamic Coloring**: Add dynamic color palettes that change over time or based on zoom levels, creating animated fractal exploration.
- **Julia Set Mode**: Implement a mode where users can explore Julia sets by fixing a point in the complex plane.
- **Performance Optimizations**: Use double-precision floats for deeper zoom levels or introduce multi-threading to offload computations from the GPU.
- **Saving Images**: Add functionality to export the current view as a high-resolution image.

## Contributing

Contributions are welcome! If you'd like to improve the renderer, add new features, or optimize performance, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make your changes and commit them (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes tests for any new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Happy fractal exploring!
