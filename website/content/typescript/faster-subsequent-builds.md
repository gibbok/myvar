+++
title = 'Faster subsequent builds'
date = 2025-12-09T09:00:00-11:00
draft = false
tags = ['hugo', 'go']
description = 'Learn how to create a user-friendly HTML sitemap in Hugo and complement the automatically generated sitemap.xml.'
+++

Incremental compilation is a fundamental TypeScript build mode that significantly speeds up development by avoiding the need to rebuild an entire project from scratch during every compilation. This process tracks which files have changed since the last build and only recompiles the modified files and their dependencies. The key mechanism involves storing build information, typically in a file defined by "tsBuildInfoFile" (e.g., .tsbuildinfo), which dramatically reduces build times and offers a significant speed  and enhancing efficiency in Continuous Integration/Continuous Deployment (CI/CD) pipelines.

Basic usage requires setting the `"incremental": true` flag in the `tsconfig.json` file, and developers can use commands like `tsc` for subsequent fast builds or `tsc --build --clean` to start fresh if build info becomes stale.

For complex, multi-package monorepos, advanced usage mandates the use of Project References by enabling `"composite":` true and defining explicit "references" to ensure proper dependency management between sub-projects.
