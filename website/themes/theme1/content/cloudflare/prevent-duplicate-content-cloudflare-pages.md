+++
title = 'Prevent SEO Issues on Cloudflare Pages with `X-Robots-Tag`'
date = 2025-11-18T09:00:00-08:00
draft = false
tags = ['frontend-development', 'cloudflare', 'seo']
+++

If you're hosting any website on Cloudflare Pages, you face a common SEO issue: content duplication. Cloudflare Pages automatically serves your site on two domains: your custom domain (e.g., https://mysite.com/) and a default Cloudflare domain (e.g., https://mysite.pages.dev/).

This dual indexing can harm your Search Engine Optimization (SEO). The solution is to use a custom header to apply the X-Robots-Tag HTTP header, which instructs search engine crawlers not to index the default Cloudflare domain.

Prevent Content Duplication with the `_headers` File
To prevent search engines from indexing the `*.pages.dev` domain, you must configure a custom header file.

Create the `_headers` File: In the root of your site's build output directory (the folder containing your static files, often dist or public before the build), create a file named `_headers`.

Add the X-Robots-Tag Rule: Add the following content to the `_headers file`. Crucially, replace mysite.pages.dev with your site's actual Cloudflare domain.

```text
https://mysite.pages.dev/*
  X-Robots-Tag: noindex
```

The first line targets all paths on your specific Cloudflare Pages domain.

The second line applies the directive X-Robots-Tag: noindex.

How the Header Works
When a user or a search engine crawler accesses any page on the specified https://mysite.pages.dev/ domain, Cloudflare Pages will include the following HTTP header in the response:

```text
x-robots-tag: noindex
```

This header instructs search engines not to index the page, effectively solving the content duplication issue by funneling search traffic exclusively to your custom domain (https://mysite.com/).

Cloudflare Pages Automatic Preview Handling
Note: Cloudflare Pages automatically applies the noindex tag to all Preview Deployments (e.g., https://myhash.mysite.pages.dev and https://mybranch.mysite.pages.dev). This ensures your development and staging environments are not indexed. The custom `_headers` rule discussed here is only necessary to specifically target and de-index your production Cloudflare Pages domain.
