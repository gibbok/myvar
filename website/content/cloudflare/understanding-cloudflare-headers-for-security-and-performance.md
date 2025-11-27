+++
title = 'Understanding Cloudflare Headers for Security and Performance'
date = 2025-11-26T09:00:00-08:00
draft = false
tags = ['cloudflare', 'hugo', 'security']
description = 'A quick overview of common Cloudflare headers that improve security, privacy, and caching.'
+++

This article explains a set of Cloudflare Rules that apply security, privacy, and performance-related headers across different paths of your site.

Create a file named `_headers` in your Hugo `static/` folder with the following content:

```bash
https://yoursite.pages.dev/*
  X-Robots-Tag: noindex

/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/images/*.png
  Cache-Control: public, max-age=31536000, immutable
```

## X-Robots-Tag: noindex

Prevents search engines from indexing your site. Useful for staging domains, previews, or private environments where you don’t want content appearing in search results.

## X-Frame-Options: DENY

Blocks your site from being embedded inside iframes. This protects against clickjacking attacks.

## X-Content-Type-Options: nosniff

Prevents browsers from MIME–sniffing files, reducing exposure to certain injection attacks.

## Referrer-Policy: strict-origin-when-cross-origin

Limits what referrer information is sent when navigating away from your site. It preserves referrer data for same-origin requests while protecting privacy for external requests.

## Permissions-Policy

Controls access to browser features.
In this case, geolocation, microphone, and camera APIs are fully disabled:

- geolocation=() – no access
- microphone=() – no access
- camera=() – no access

## Content-Security-Policy (CSP)

A strong defense layer to restrict what resources the browser can load.

- default-src 'self' — Everything must come from your own domain unless otherwise allowed.
- script-src 'self' 'unsafe-inline' — Scripts must come from your domain; inline scripts allowed (useful for Hugo/Cloudflare Pages but reduces strictness).
- style-src 'self' 'unsafe-inline' — Same idea for stylesheets.
- img-src 'self' data: — Images must come from your site or embedded as data URIs.
- font-src 'self' data: — Fonts from your domain or data URIs.

## Asset Caching for /css/\*

Sets long-term caching (1 year). Because CSS files rarely change their names, versioned filenames (e.g., style.abcd.css) should be used to avoid stale caching.

## Asset Caching for /js/\*

JavaScript files also get a 1-year immutable cache. This greatly improves performance for returning visitors.

## Caching for PNG Images

Large, static assets like PNGs benefit the most from long cache lifetimes. This reduces bandwidth usage and speeds up page loads.

These Cloudflare rules collectively help secure your site, protect user privacy, and enhance performance through optimized caching.
