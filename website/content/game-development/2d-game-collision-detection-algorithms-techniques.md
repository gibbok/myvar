+++
title = '2D Game Collision Detection: Algorithms & Techniques'
date = 2025-12-27T09:19:00.284378
draft = false
tags = ['game-dev', '2d-games', 'collision']
description = 'Learn about 2D game collision detection, exploring bounding object methods, pixel-based approaches, and algorithm choices for optimal performance and accuracy.'
+++

## Understanding Collision Detection in 2D Game Development

Collision detection determines when objects in a game world interact, enabling realistic and intuitive gameplay.

This article provides a basic introduction to common 2D collision detection algorithms, focusing on widely used, easy-to-understand techniques such as bounding volumes and simple shape tests. It outlines their advantages, disadvantages, and general implementation considerations.

More advanced approaches—including broad-phase optimizations, spatial partitioning, continuous collision detection, and algorithms like GJK or BVH—are intentionally out of scope for this article and may be explored in future, more in-depth discussions.

### Key Insights

- **Bounding Object Efficiency:** For performance, pixel-level collision detection is generally avoided in favor of bounding object methods, which approximate object shapes with simpler geometric forms.
- **Trade-offs in Accuracy vs. Performance:** Simpler bounding shapes (circles, axis-aligned boxes) offer higher performance at the cost of potential false positives or missed collisions. More complex shapes (polygons) increase accuracy but demand more computational resources.
- **Algorithm Selection is Crucial:** The choice of collision detection algorithm significantly impacts development time, performance, and the overall player experience. Modern engines often combine multiple approaches.

### Technical Details

#### Collision Detection Fundamentals

Collision detection is the process of identifying when two or more game objects intersect. This is critical for simulating realistic interactions, such as bullets hitting enemies or characters colliding with obstacles.

- **Pixel-Based Collision Detection:** Directly checks for overlapping pixels between object images. Offers high precision but is computationally expensive, especially for complex textures.
- **Bounding Object-Based Collision Detection:** Employs simpler geometric shapes (e.g., circles, boxes, polygons) that enclose game objects. Collision is determined by checking for overlaps between these bounding shapes. This approach is significantly more performant.

#### Bounding Circle Collision

The simplest bounding object method encloses each object within a circle.

- **Implementation:** Defined by a center point and a radius.
- **Collision Test:** Two circles collide if the distance between their centers is less than or equal to the sum of their radii.
- **Formula:** `distance(center1, center2) <= radius1 + radius2`
- **Pros:** Extremely simple to implement, computationally inexpensive.
- **Cons:** Poor approximation for non-circular objects, leading to false collisions or missed detections if the circle doesn't fit well. Best suited for objects that naturally approximate a circle.

#### Bounding Box Collision

Bounding boxes, typically rectangles, are a widely used method for collision detection.

- **Axis-Aligned Bounding Boxes (AABB):** Rectangles with edges parallel to the coordinate axes.
  - **Definition:** Defined by minimum and maximum points (e.g., bottom-left and top-right corners).
  - **Collision Test (Box-Box Overlap):** Two AABBs collide if they overlap on both the X and Y axes. This is efficiently checked by verifying that there is no separation:
    - `!(box1.max.x < box2.min.x || box1.min.x > box2.max.x || box1.max.y < box2.min.y || box1.min.y > box2.max.y)`
  - **Pros:** Simple to implement and computationally cheap for overlap tests.
  - **Cons:** Can result in false collisions for "holey" objects or when only transparent areas overlap. Its effectiveness diminishes with object rotation.
- **Oriented Bounding Boxes (OBB):** Rectangles that rotate with the object.
  - **Pros:** More accurately conforms to the shape of rotated objects compared to AABB.
  - **Cons:** Collision detection is mathematically more complex.
- **AABB Rotation:** Rotating an AABB involves:
  1.  Transforming its corner points.
  2.  Finding the new minimum and maximum points to define a new AABB.
  3.  **Challenge:** Rotation often increases the AABB's size, reducing collision accuracy. Developers may pre-render rotated sprites with their own bounding boxes.
- **Multiple Bounding Boxes:** Using several AABBs to cover an object improves accuracy for complex shapes, mitigating the "holey" object problem.
- **Moving Bounding Boxes:** Bounding boxes are translated with their associated game objects. Accurate collision requires synchronizing CPU-side calculations with GPU-side rendering positions. Storing both original and transformed box versions is recommended.

#### Mixed Bounding Object Collision

- **Circle-AABB Collision:** Detects collisions between a bounding circle and a bounding box.
  - **Algorithm:**
    1.  Determine the vector between the circle's center and the box's center.
    2.  **Clamp** this vector to the box's dimensions to find the **closest point (P)** on the box to the circle's center.
    3.  Calculate the distance between the circle's center and point P.
    4.  If this distance is less than or equal to the circle's radius, a collision occurs.

#### Bounding Polygon Collision

For maximum accuracy, bounding polygons (convex or concave) precisely enclose object shapes.

- **Separating Axis Theorem (SAT):**
  - **Principle:** Two convex shapes do _not_ intersect if there exists at least one axis onto which their projections do not overlap.
  - **Application:** Tests axes perpendicular to the edges of the polygons. If projections overlap on _all_ tested axes, the shapes collide.
  - **Pros:** Accurate for convex polygons, efficient due to early exit on finding a separating axis.
  - **Cons:** Requires more complex geometric calculations than AABB or circle collision. Primarily suited for convex shapes.

#### Choosing the Right Approach

- **Simple, Fast Games:** Bounding circles or AABBs are often sufficient.
- **Complex Shapes/High Accuracy Needs:** Consider multiple bounding boxes or bounding polygons with SAT.
- **Performance Considerations:** Always prioritize simpler methods where accuracy permits. Profile collision detection performance to identify bottlenecks.
- **Engine Capabilities:** Leverage built-in collision systems provided by game engines, which often optimize and combine various techniques.
