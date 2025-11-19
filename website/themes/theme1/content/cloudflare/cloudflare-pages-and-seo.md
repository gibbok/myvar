+++
title = 'Cloudflare Web Analytics on Astro Starlight'
date = 2025-11-18T09:00:00-07:00
draft = false
tags = ['frontend-development', 'cloudflare', 'astro', 'web-analytics']
+++

Cloudflare Pages a platform for building, deploying, and hosting modern web applications, especially Jamstack sites.

After a basic setup for Cloudflare Pages Cloudflare will make visible your site at this address: `https://mysite.pages.dev/` even after your setup CNET domains for your site, let's call it `https://mysite.com/` .

Unfortuantelly this is problematic for SEO, as the content of your site could result as duplicated as visible in two different sites.

A simple an effective solutio to this issue is to inform the SEO crawer to do not index pages from the domain `https://mysite.pages.dev/`.

In order to achieve this we need to set CloudFlare custom headers.

Create a file `_headers` in the `static` (or other folder to write the static files for your site) add this content:

```text
https://mysite.pages.dev/*
  X-Robots-Tag: noindex
```

This will instruct CloudFlare to add this header on every response for your site:

```text
x-robots-tag: noindex
```

The X-Robots-Tag: noindex HTTP header is used to instruct search engines not to index a specific page or resource, preventing it from appearing in search results.

CloudFlare autoamtically setup these header on pull request like:

Preview URL: https://myhash.mysite.pages.dev
Branch Preview URL: https://mybranch.mysite.pages.dev

Which is very handly.
