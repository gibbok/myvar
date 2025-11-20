+++
title = 'A Quick Guide to Hugo’s Core Directory Structure'
date = 2025-11-18T09:00:00-11:00
draft = false
tags = ['hugo', 'go']
description = 'Master the Hugo directory structure. Essential guides to organizing files and content for seamless static site generation.'
+++

A Hugo site is powered by five key directories: **content**, **layouts**, **archetypes**, **static**, and **themes**. Here’s a concise guide to what each does and why it matters.

## 1. Content: Your Site’s Words

Everything you publish lives in `content/`.

**How content is structured:**

- **Sections:** Folders like `blog/` or `work/` containing multiple posts.
- **Static pages:** Standalone Markdown files such as `about.md`.

**Key concepts:**

- **List vs. single pages:**  
  Sections need an `_index.md` to render list pages; individual posts use their own `.md` files.
- **Homepage:** Defined by `content/_index.md`.
- **Content types:** Inferred from folder name or set explicitly in front matter.

## 2. Layouts: How Everything Looks

`layouts/` holds the templates that render all content.

**How Hugo selects templates:**

- **Single vs. list templates:**  
  `single.html` renders individual pages; `list.html` renders section indexes.
- **Lookup order:**  
  Hugo picks the most specific template available.
- **Default fallback:**  
  `layouts/_default/` should include baseline `single.html` and `list.html`.
- **Custom types:**  
  Add folders such as `layouts/blog/` for type-specific templates.
- **Base templates:**  
  Shared structure lives in `baseof.html`.

## 3. Archetypes: Faster Content Creation

Archetypes provide default front matter for new content.

- Files inside `archetypes/` match content types (e.g., `blog.md`).
- Running `hugo new blog/my-post.md` uses the matching archetype if available.
- Helps enforce consistent metadata and reduce repetitive setup.

## 4. Static: Your Assets

Everything in `static/` is published as-is.

Common contents:

- CSS, JS, fonts, images
- Referenced in templates with paths like `/css/styles.css`

Hugo doesn’t enforce an asset pipeline—your tooling decides what ends up here.

## 5. Themes: Drop-In Site Designs

The `themes/` directory allows you to plug in complete design packages.

Each theme typically includes its own:

- `layouts/` (templates)
- `static/` assets
- `archetypes/`
- `theme.toml` configuration

Your project will use these files unless you override them in your root directories. This structure makes customizing or extending a theme straightforward while keeping project-specific changes cleanly separated.

Example of Hugo’s Core Directory Structure:

```text
my-hugo-site/
├── archetypes/
│   ├── default.md
│   └── blog.md
├── content/
│   ├── _index.md
│   ├── about.md
│   └── blog/
│       ├── _index.md
│       └── first-post.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   └── single.html
│   └── blog/
│       └── single.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo.png
├── themes/
│   └── my-theme/
│       ├── layouts/
│       ├── static/
│       ├── archetypes/
│       └── theme.toml
└── config.toml
```
