+++
title = 'Understanding Cloudflare Headers for Security and Performance'
date = 2025-11-26T09:00:00-08:00
draft = false
tags = ['cloudflare', 'hugo', 'security']
description = 'A quick overview of common Cloudflare headers that improve security, privacy, and caching.'
+++

This article explains how to configure security, privacy, and performance-related headers for Cloudflare Pages using the `_headers` file.

Note: This configuration example includes commonly used tools like Google Fonts and Pagefind (WebAssembly-based search). Adjust the CSP directives based on your actual dependencies. Test your site thoroughly after applying these headers to ensure nothing breaks.

Create a file named `_headers` in your Hugo `static/` folder with the following content:

```text
https://yoursite.pages.dev/*
  X-Robots-Tag: noindex

/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval' https://static.cloudflareinsights.com; style-src 'self' https://fonts.googleapis.com; img-src 'self' data:; font-src 'self' data: https://fonts.gstatic.com; connect-src 'self' https://cloudflareinsights.com; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests

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

Blocks your site from being embedded inside iframes. This protects against clickjacking attacks. Note: This is redundant with `frame-ancestors 'none'` in CSP but included for older browser compatibility.

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

- **default-src 'self'** — Everything must come from your own domain unless otherwise allowed.
- **script-src 'self' 'wasm-unsafe-eval' https://static.cloudflareinsights.com** — Scripts from your domain, WebAssembly compilation allowed, and Cloudflare Insights analytics. Note: `'wasm-unsafe-eval'` is only needed if you use WebAssembly-based tools like Pagefind for search functionality. While safer than `'unsafe-eval'`, it still allows some eval-like behavior. Remove it if you don't use WebAssembly for better security.
- **style-src 'self' https://fonts.googleapis.com** — Stylesheets from your domain and Google Fonts CSS. Note: Remove `https://fonts.googleapis.com` if you're not using Google Fonts.
- **img-src 'self' data:** — Images from your site or embedded as data URIs.
- **font-src 'self' data: https://fonts.gstatic.com** — Fonts from your domain, data URIs, or Google Fonts CDN. Note: Remove `https://fonts.gstatic.com` if you're not using Google Fonts.
- **connect-src 'self' https://cloudflareinsights.com** — Network requests to your domain and Cloudflare analytics endpoints. Note: Both `static.cloudflareinsights.com` (for loading the script) and `cloudflareinsights.com` (for sending analytics data) are needed for Cloudflare Web Analytics.
- **base-uri 'self'** — Prevents base tag hijacking attacks.
- **form-action 'self'** — Forms can only submit to your own domain.
- **frame-ancestors 'none'** — Prevents your site from being embedded in iframes (modern alternative to X-Frame-Options).
- **object-src 'none'** — Blocks plugins like Flash and Java applets.
- **upgrade-insecure-requests** — Automatically upgrades HTTP requests to HTTPS.

## Asset Caching for /css/\*

Sets long-term caching (1 year). Because CSS files rarely change their names, versioned filenames (e.g., style.abcd.css) should be used to avoid stale caching.

## Asset Caching for /js/\*

JavaScript files also get a 1-year immutable cache. This greatly improves performance for returning visitors.

## Caching for PNG Images

Large, static assets like PNGs benefit the most from long cache lifetimes. This reduces bandwidth usage and speeds up page loads.

These Cloudflare Pages headers collectively help secure your site, protect user privacy, and enhance performance through optimized caching.

## Testing

After deploying these headers, test your site thoroughly to ensure all functionality works correctly. Use browser developer tools to check for CSP violations and adjust directives as needed.
