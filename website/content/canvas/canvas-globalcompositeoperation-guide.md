+++
title = 'Canvas globalCompositeOperation Guide'
date = 2025-12-26T10:09:15.663655
draft = false
tags = ['html5-canvas', 'web-graphics', 'blending-modes']
description = 'A technical overview of the CanvasRenderingContext2D globalCompositeOperation property.'
+++

# CanvasRenderingContext2D: `globalCompositeOperation`

## Overview

The `globalCompositeOperation` property determines how new shapes and images (**source**) are drawn relative to existing canvas content (**destination**). It manages both alpha compositing and color blending to enable complex visual effects like masking, erasing, and lighting.

## Key Insights

- **State-Based Property:** Setting this value affects all subsequent drawing operations until it is changed or the context state is restored.
- **Source vs. Destination:** "Source" refers to the new pixels being introduced; "Destination" refers to the pixels already rendered on the canvas.
- **Reset Requirement:** Always reset the property to `source-over` after completing a specific effect to prevent unintended compositing in later operations.
- **Broad Compatibility:** Applies to all drawing actions, including shapes, paths, text, images, gradients, and patterns.

## Technical Details

### Core Compositing Modes

Compositing modes control the placement and visibility of pixels based on the overlap between source and destination.

| Mode               | Behavior                                                     | Common Use Case                   |
| :----------------- | :----------------------------------------------------------- | :-------------------------------- |
| `source-over`      | Draws source **on top** of destination (Default).            | Standard layering.                |
| `destination-over` | Draws source **behind** destination.                         | Adding backgrounds retroactively. |
| `source-in`        | Keeps source only where it **overlaps** destination.         | Clipping images to shapes.        |
| `destination-in`   | Keeps destination only where it **overlaps** source.         | Dynamic masking.                  |
| `source-out`       | Keeps source only where it **does not overlap** destination. | Drawing in negative space.        |
| `destination-out`  | Removes destination where the source **overlaps**.           | Eraser or "scratch-off" effects.  |

### Blend Modes (Color Mixing)

Unlike basic compositing, blend modes use mathematical formulas to mix the colors of overlapping pixels.

- **Darkening:** `multiply` (darkens by multiplying values), `darken` (keeps darkest pixel), `color-burn`.
- **Lightening:** `screen` (inverse of multiply), `lighten` (keeps lightest pixel), `color-dodge`.
- **Contrast/Lighting:** `overlay` (combination of multiply/screen), `hard-light`, `soft-light`.
- **Comparative:** `difference` (subtracts values), `exclusion` (lower-contrast difference).

### Implementation: Creating an Eraser

To turn a drawing tool into an eraser, switch the operation to `destination-out`.

```javascript
// Enable eraser mode
ctx.globalCompositeOperation = "destination-out";

ctx.beginPath();
ctx.arc(150, 75, 30, 0, Math.PI * 2);
ctx.fill(); // This circle now clears existing pixels

// Reset to default behavior
ctx.globalCompositeOperation = "source-over";
```

### Decision Logic: The Mental Model

When selecting a mode, evaluate the desired outcome of the overlap:

1.  **Keep Source?** Use `source-*` modes.
2.  **Keep Destination?** Use `destination-*` modes.
3.  **Only the Intersection?** Use `-in` suffixes.
4.  **Everything except the Intersection?** Use `-out` suffixes.
5.  **Mix Colors?** Use Blend Modes (`multiply`, `screen`, etc.).

## Application Scenarios

- **UI/UX:** Building scratch-card components or custom cursors.
- **Image Editing:** Implementing non-destructive masks and clipping paths.
- **Game Development:** Creating dynamic lighting, shadows, and particle blending.
- **Generative Art:** Layering complex color interactions and textures.
