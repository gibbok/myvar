+++
title = 'How to Configure Pagefind in Cloudflare Pages Build Settings'
date = 2025-11-25T09:00:00-08:00
draft = false
tags = ['cloudflare', 'pagefind']
description = 'A short guide showing how to configure Pagefind in the Cloudflare Pages build settings.'
+++

To ensure Pagefind runs automatically during your Cloudflare Pages deployment, update your project’s build configuration.

In Cloudflare Pages, navigate to:

`Workers & Pages → Your Project → Settings → Build → Build configuration`

Then set the build command to:

```bash
hugo && npx pagefind --site public --output-path public/pagefind
```

This command first generates your site with Hugo, placing the output in the public directory.
Pagefind then scans that directory, builds the search index, and writes its files into public/pagefind, making the search functionality available on your deployed site.

If your build process requires more complex logic, you can instead create a build.sh script and set that file as your build command.

x
