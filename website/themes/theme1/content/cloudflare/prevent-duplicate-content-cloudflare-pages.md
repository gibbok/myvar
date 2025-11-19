+++
title = 'Prevent SEO Issues on Cloudflare Pages with `X-Robots-Tag`'
date = 2025-11-18T09:00:00-08:00
draft = false
tags = ['cloudflare', 'seo']
+++

Cloudflare Pages serves your site on two domains: your custom domain (e.g., `mysite.com`) and a default `mysite.pages.dev` domain. If both get indexed, search engines may treat them as duplicate content, hurting your SEO.

To prevent this, add an `X-Robots-Tag` header to the `mysite.pages.dev` version of your site so crawlers don’t index it.

## How to set it up

1. In your site’s build output directory (usually `static` or `public`), create a file named `_headers`.
2. Add the following rule (replace `mysite.pages.dev` with your actual Cloudflare Pages domain):

```text
https://mysite.pages.dev/*
  X-Robots-Tag: noindex
```

The first line matches all paths on your Cloudflare Pages domain.  
The second line applies the `X-Robots-Tag: noindex` directive.

## How the Header Works

When a user or crawler visits any page on `https://mysite.pages.dev/`, Cloudflare Pages returns this header:

```text
x-robots-tag: noindex
```

This tells search engines not to index the page, ensuring that only your custom domain (e.g., `https://mysite.com/`) is indexed.

## Automatic Preview Handling

Cloudflare Pages already adds noindex to all Preview Deployments (e.g., `https://myhash.mysite.pages.dev`, `https://mybranch.mysite.pages.dev`).
The custom `_headers` rule is only needed to de-index the production `mysite.pages.dev` domain.
