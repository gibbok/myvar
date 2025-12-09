+++
title = 'Incremental TypeScript Builds for Faster Compilation'
date = 2025-12-09T09:00:00-11:00
draft = false
tags = ['typescript', 'build']
description = 'Understand how TypeScript incremental compilation and project references speed up rebuilds, reduce CI/CD overhead, and improve development workflows.'
+++

Incremental compilation is a TypeScript build mode designed to speed up development by avoiding full project rebuilds on every compile.

Instead, the compiler tracks which files have changed since the previous build and recompiles only those files and their affected dependencies.

To support this, TypeScript stores build metadata in a `.tsbuildinfo` file, or in a custom file defined by the `tsBuildInfoFile` option. Reusing this information dramatically reduces rebuild times and can improve CI/CD performance when the build info file is cached between runs.

## Basic Usage

To enable incremental compilation in a single TypeScript project, include the following in your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "incremental": true
  }
}
```

Running tsc will then perform fast incremental rebuilds. If the build information ever becomes outdated or corrupted, removing the generated `.tsbuildinfo` file will force a full rebuild.

## Incremental Compilation in Project References

For larger, multi-package monorepos, TypeScript offers Project References, which create explicit build boundaries between sub-projects. When using project references:

- Each referenced project must set `"composite": true` in its `tsconfig.json`.
- Incremental compilation is enabled automatically for those projects.
- You can use build mode commands such as:

```shell
tsc --build
tsc --build --clean
```

These commands work only when using project references and provide efficient, dependency-aware builds across multiple projects.
