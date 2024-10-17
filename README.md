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
