+++
title = 'Understanding GLSL Shaders for Web Graphics'
date = 2025-12-27T10:16:41.592905
draft = false
tags = ['GLSL', 'WebGL', 'GPU-graphics']
description = 'Understand GLSL for web graphics. Learn about GPU-executed Vertex and Fragment shaders for advanced visual effects, complementing WebGL.'
+++

## Understanding GLSL Shaders for Web Graphics

### Overview

GLSL (OpenGL Shading Language) is a C-like, strongly-typed language executed directly by the GPU's graphics pipeline. It enables advanced visual effects and computations in web-based 3D graphics, complementing JavaScript rendering APIs like WebGL.

### Key Insights

- **GPU Offloading:** Shaders run on the GPU, optimizing computationally intensive graphics operations and freeing the CPU.
- **Core Shader Types:** **Vertex Shaders** and **Fragment (Pixel) Shaders** are primary for web graphics.
- **Vertex Shader Function:** Transforms 3D vertex positions, defining object geometry and scene placement.
- **Fragment Shader Function:** Computes pixel colors and attributes, determining an object's visual appearance.
- **Complexity:** GLSL involves significant vector and matrix mathematics, making it more complex than JavaScript.
- **Three.js Integration:** Libraries like Three.js abstract WebGL complexity, simplifying shader implementation and scene management.

### Technical Details

Shaders are fundamental GPU-processed functions for rendering graphics. They operate in parallel, simultaneously processing numerous vertices or pixels.

### Core Shader Types

#### Vertex Shaders

A vertex shader executes once per vertex, manipulating 3D vertex coordinates and projecting them onto a 2D screen.

- **Purpose:** Sets the built-in **`gl_Position`** variable, storing the final projected vertex position.
- **Execution:** The **`void main()`** function defines the vertex's transformation logic.

#### Fragment Shaders

A fragment shader executes once per pixel (or fragment), determining its final color.

- **Purpose:** Sets the built-in **`gl_FragColor`** variable, specifying the fragment's RGBA (red, green, blue, alpha) color.
- **Color Representation:** RGBA values are floating-point numbers from `0.0` (minimum intensity/transparency) to `1.0` (maximum intensity/opacity).

### Implementing Shaders with Three.js

Integrate custom GLSL shaders into a Three.js scene to render a simple cube. Three.js simplifies the underlying WebGL setup.

#### Environment Setup

A basic Three.js project requires the Three.js library and a `<canvas>` element.

#### HTML Structure

Embed GLSL shader code and main JavaScript logic within script tags in the HTML:

```html
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>MDN Games: Shaders demo</title>
    <style>
      html,
      body,
      canvas {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        font-size: 0;
      }
    </style>
    <script src="three.min.js"></script>
  </head>
  <body>
    <script id="vertexShader" type="x-shader/x-vertex">
      // Vertex shader code here
    </script>
    <script id="fragmentShader" type="x-shader/x-fragment">
      // Fragment shader code here
    </script>
    <script>
      // Three.js scene setup and application logic here
    </script>
  </body>
</html>
```

#### Cube Integration

Begin with a standard Three.js cube setup. Modify its material to utilize custom shaders, reusing existing renderer, camera, and lights.

#### Vertex Shader Implementation

This shader translates the cube's position:

```glsl
void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position.x+10.0, position.y, position.z+5.0, 1.0);
}
```

- **`gl_Position`**: The output variable for the vertex's final position.
- **`projectionMatrix`**, **`modelViewMatrix`**: Three.js-provided matrices for camera projection and model-view transformations.
- **`vec4(position.x+10.0, position.y, position.z+5.0, 1.0)`**: Defines the new vertex position, shifting the cube 10 units along the X-axis and 5 units along the Z-axis. The fourth component (`1.0`) is for homogeneous coordinates.

#### Fragment Shader Implementation

This shader assigns a static blue color to the cube:

```glsl
void main() {
    gl_FragColor = vec4(0.0, 0.58, 0.86, 1.0);
}
```

- **`gl_FragColor`**: The output variable for the pixel's final RGBA color.
- **`vec4(0.0, 0.58, 0.86, 1.0)`**: Sets the color to light blue (0% red, 58% green, 86% blue, 100% opaque).

#### Applying the Shaders

Integrate GLSL code into the Three.js scene by creating a `ShaderMaterial`:

```javascript
// Comment out or remove the basic material
// const basicMaterial = new THREE.MeshBasicMaterial({color: 0x0095DD});

// Create ShaderMaterial
const shaderMaterial = new THREE.ShaderMaterial({
  vertexShader: document.getElementById("vertexShader").textContent,
  fragmentShader: document.getElementById("fragmentShader").textContent,
});

// Assign the shader material to the cube
// const cube = new THREE.Mesh(boxGeometry, basicMaterial);
const cube = new THREE.Mesh(boxGeometry, shaderMaterial);
```

This configuration instructs Three.js to compile and execute the provided GLSL shaders for the `cube` object, overriding default material properties.

### Complete Code Example

```html
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>MDN Games: Shaders demo</title>
    <style>
      body {
        margin: 0;
        padding: 0;
        font-size: 0;
      }
      canvas {
        width: 100%;
        height: 100%;
      }
    </style>
    <script src="https://end3r.github.io/MDN-Games-3D/Shaders/js/three.min.js"></script>
  </head>
  <body>
    <script id="vertexShader" type="x-shader/x-vertex">
      void main() {
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position.x+10.0, position.y, position.z+5.0, 1.0);
      }
    </script>
    <script id="fragmentShader" type="x-shader/x-fragment">
      void main() {
          gl_FragColor = vec4(0.0, 0.58, 0.86, 1.0);
      }
    </script>
    <script>
      const WIDTH = window.innerWidth;
      const HEIGHT = window.innerHeight;

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(WIDTH, HEIGHT);
      renderer.setClearColor(0xdddddd, 1);
      document.body.appendChild(renderer.domElement);

      const scene = new THREE.Scene();

      const camera = new THREE.PerspectiveCamera(70, WIDTH / HEIGHT);
      camera.position.z = 50;
      scene.add(camera);

      const boxGeometry = new THREE.BoxGeometry(10, 10, 10);

      const shaderMaterial = new THREE.ShaderMaterial({
        vertexShader: document.getElementById("vertexShader").textContent,
        fragmentShader: document.getElementById("fragmentShader").textContent,
      });

      const cube = new THREE.Mesh(boxGeometry, shaderMaterial);
      scene.add(cube);
      cube.rotation.set(0.4, 0.2, 0);

      function render() {
        requestAnimationFrame(render);
        renderer.render(scene, camera);
      }
      render();
    </script>
  </body>
</html>
```
