+++
title = 'Effective JavaScript Bundle Optimization: Reducing the No-Interactivity Gap'
date = 2025-12-09T09:00:00-00:00
draft = false
tags = ['javascript', 'performance', 'bundling', 'tree-shaking']
description = 'A practical guide to reducing JavaScript bundle size by analyzing bundle contents, fixing tree-shaking issues, removing duplicates, and eliminating heavy transitive dependencies to improve page interactivity.'
+++

• Old React utilized a recursive tree walker that locked the main thread of the browser because recursion in JavaScript is not interruptible, causing performance issues and jank when dealing with large UI trees.
• React Fiber is a literal, fake callstack implemented as a linked structure of nodes, allowing React to take control away from the JavaScript engine's stack.
• Each fiber node acts like a memory cell, storing information such as the component type, props, state, priority, and pointers to siblings and children.
• This manual control enables React to move from recursive rendering to iterative stepping, allowing it to pause mid-render, let the browser repaint or handle input, and then resume precisely where it left off.
• Fiber allows for scheduling, meaning React can prioritize urgent updates (like typing) over lower-priority tasks, ensuring the application remains smooth even during heavy work.
• The system uses a double-tree structure (the current tree and the work-in-progress tree) to run the render phase as a simulation, building an offscreen version of the UI without touching the actual DOM.
• The real DOM is only mutated during the commit phase after the offscreen UI is complete and consistent, which ensures the user never sees broken or half-updated states.
• Fiber's capabilities—such as the custom stack and double-tree structure—are fundamental to modern features like Suspense and smooth transitions.
