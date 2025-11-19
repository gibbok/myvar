+++
title = 'Cloudflare Web Analytics on Astro Starlight'
date = 2025-11-18T09:00:00-07:00
draft = false
tags = ['frontend-development', 'cloudflare', 'astro', 'web-analytics']
+++

To integrate Cloudflare Web Analytics into your Astro Starlight documentation site, you must insert the beacon script into the `<head>` of all pages via the `astro.config.mjs` file.

1. **Retrieve Token:** Get your unique analytics token (e.g., 9692482312d8a417...) from the Cloudflare Web Analytics dashboard.
2. **Update Configuration:** Open `astro.config.mjs` and add the following configuration block within the starlight integration. Replace "YOUR_TOKEN_HERE" with your actual token.

```javascript
export default defineConfig({
  ...
  integrations: [
    starlight({
      head: [
        {
          tag: "script",
          attrs: {
            defer: true,
            src: "https://static.cloudflareinsights.com/beacon.min.js",
            "data-cf-beacon": '{"token": "YOUR_TOKEN_HERE"}',
          },
        },
      ],
    }),
  ],
});
```

3. **Deploy:** Build and deploy your updated site. Data will start appearing in your Cloudflare dashboard after users begin visiting your site.
