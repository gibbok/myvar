+++
title = 'How to Generate an HTML Sitemap in Hugo'
date = 2025-11-20T09:00:00-11:00
draft = false
tags = ['hugo', 'go']
description = 'Learn how to create a user-friendly HTML sitemap in Hugo and complement the automatically generated sitemap.xml.'
+++

An HTML sitemap is a simple yet powerful way to help both users and search engines understand the structure of your website. Unlike an XML sitemap—which (Hugo also automatically generates a `sitemap.xml` file for search engines) is mainly designed for search engine crawlers—an HTML sitemap provides a human-readable overview of your pages and taxonomies.

Below is a quick example of how to add a clean, automatically generated HTML sitemap to your HUGO site.

Create a new file at `layouts/sitemap/single.html` and place the following code inside:

```html
{{ define "main" }}
<h1>Sitemap</h1>

<h2>Content</h2>
<ul>
  {{- range .Site.RegularPages }} {{- if ne .Type "sitemap" }}
  <li><a href="{{ .Permalink }}">{{ .Title }}</a></li>
  {{- end }} {{- end }}
</ul>

<h2>Tags</h2>
<ul>
  {{- range .Site.Taxonomies.tags }}
  <li><a href="{{ .Page.Permalink }}">{{ .Page.Title }}</a></li>
  {{- end }}
</ul>
{{ end }}
```

This template renders a complete list of all regular pages on your site (excluding the sitemap itself) along with a list of all tags, each linking to its respective taxonomy page.

Benefits of an HTML Sitemap:

- **Improved navigation:** Helps visitors find pages not linked in your main menu.
- **Better content discovery:** Makes long-form or nested content easier to reach.
- **Enhanced accessibility:** Provides a clear, screen-reader-friendly overview of your site.
- **SEO support:** Assists search engines in understanding your site structure for better crawling.
- **Maintenance clarity:** Gives you a quick snapshot of all published content as your site grows.
