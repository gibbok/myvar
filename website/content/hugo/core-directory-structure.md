+++
title = 'A Quick Guide to Hugo’s Core Directory Structure'
date = 2025-11-18T09:00:00-11:00
draft = false
tags = ['hugo', 'go']
+++

When you first open a Hugo project, the folder structure can feel abstract — lots of conventions, lookup rules, and special filenames. But once you understand the core pieces, the design becomes clean and intuitive.

At its heart, a Hugo site is powered by four key directories: **content**, **layouts**, **archetypes**, and **static**. Here’s a concise guide to what each does and why it matters.

## 1. Content: Your Site’s Words

Everything you publish lives in `content/`.

**How content is structured:**

- **Sections:** Folders like `blog/` or `work/` that contain multiple posts.
- **Static pages:** Single Markdown files such as `about.md`.

**Key concepts:**

- **List vs. single pages:**  
  Sections need an `_index.md` file to display a list page. Individual posts use their own `.md` files.
- **Homepage:** Controlled by `content/_index.md`.
- **Content types:** Inferred from the folder name (`content/blog/` → type `blog`) or set in front matter.

## 2. Layouts: How Everything Looks

`layouts/` holds the templates that render your content. It’s the most important directory for defining your site’s design.

**How Hugo chooses templates:**

- **Single vs. list templates:**  
  `single.html` renders individual pages; `list.html` renders section lists.
- **Lookup order:**  
  Hugo searches for the most specific template first.
- **Default fallback:**  
  `layouts/_default/` must contain baseline `single.html` and `list.html`.
- **Custom types:**  
  Add folders like `layouts/blog/` to create type-specific templates.
- **Base templates:**  
  Shared structure comes from `baseof.html`, usually in `layouts/_default/`.

## 3. Archetypes: Faster Content Creation

Archetypes provide template front matter for new content.

**How they work:**

- The directory includes files named after content types, such as `blog.md`.
- Running `hugo new blog/my-post.md` tells Hugo to use `archetypes/blog.md`, if it exists.
- The default project includes only `default.md`.

Archetypes help you enforce consistent metadata and avoid repetitive setup.

## 4. Static: Your Assets

`static/` stores everything that should be published as-is.

Common contents:

- CSS, JS, fonts, images
- Referenced in templates using paths like `/css/styles.css`

Hugo doesn’t enforce an asset pipeline, so you decide how your build process places files here.

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
