+++
title = 'Integrating Silktide and Google Analytics with Astro Starlight'
date = 2026-03-01T18:47:47.775466
draft = false
tags = ['Astro-Starlight', 'Google-Analytics', 'Silktide']
description = 'Learn to integrate Silktide Consent Manager and Google Analytics into your Astro Starlight project via `astro.config.mjs`.'
+++

### Overview
Integrate Silktide Consent Manager and Google Analytics into an Astro Starlight project by configuring the `astro.config.mjs` file to inject necessary scripts and stylesheets into the document head.

Silktide Consent Manager is a lightweight cookie consent solution that helps websites comply with privacy regulations like GDPR by managing user consent for analytics and advertising scripts.

### Key Insights
*   **Centralized Configuration:** All external scripts and stylesheets are managed within the `head` array of the `starlight` integration in `astro.config.mjs`.
*   **Local Asset Management:** Silktide Consent Manager assets (`.css` and `.js`) are referenced locally, requiring **path updates** to match your project's `public` directory structure.
*   **Google Analytics ID:** Replace `YOUR-ID` placeholders with your specific **Google Analytics Measurement ID** for proper tracking.
*   **Silktide Manager Code:** The `code here for silktideCookieBannerManager` placeholder requires replacement with the **actual Silktide initialization script**.

### Technical Details
To embed Silktide Consent Manager and Google Analytics, modify your `astro.config.mjs` file. This configuration injects the required `<link>` and `<script>` tags directly into the `<head>` of your Starlight application.

#### `astro.config.mjs` Configuration
Update your `astro.config.mjs` file with the following code snippet. **Ensure you replace placeholders** for asset paths, Silktide manager code, and Google Analytics IDs.

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://YOUR-USER.github.io', // Update with your site URL
  base: '/YOUR-FOLDER', // Update with your base path if applicable
  build: {
    assets: 'app_assets', // Define your asset build directory
  },
  integrations: [
    starlight({
      head: [
        // Silktide Consent Manager Stylesheet
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            id: 'silktide-consent-manager-css',
            href: 'cookie-banner/silktide-consent-manager.css', // **Update path as needed**
          },
        },
        // Silktide Consent Manager Script
        {
          tag: 'script',
          attrs: {
            src: 'cookie-banner/silktide-consent-manager.js', // **Update path as needed**
          },
        },
        // Silktide Cookie Banner Manager Initialization
        {
          tag: 'script',
          content: `// Place your SilktideCookieBannerManager initialization code here` // **Add your Silktide code**
        },
        // Google Analytics Global Site Tag (gtag.js)
        {
          tag: 'script',
          attrs: {
            src: 'https://www.googletagmanager.com/gtag/js?id=YOUR-ID', // **Replace YOUR-ID**
          },
        },
        // Google Analytics Initialization
        {
          tag: 'script',
          content: `
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'YOUR-ID'); // **Replace YOUR-ID**
`
        }
      ],
    }),
  ],
});
```

#### Customization Steps
*   **Silktide Asset Paths:** Adjust the `href` for `silktide-consent-manager.css` and `src` for `silktide-consent-manager.js` to correctly point to the files within your project's `public` directory. For example, if your files are in `public/cookie-banner/`, the provided paths are correct relative to the base URL.
*   **Silktide Initialization:** Replace the placeholder comment `// Place your SilktideCookieBannerManager initialization code here` with the **actual JavaScript code provided by Silktide** for initializing their consent manager. This typically involves configuring consent options.
*   **Google Analytics ID:** Update both instances of `YOUR-ID` with your specific **Google Analytics 4 (GA4) Measurement ID** (e.g., `G-XXXXXXXXXX`). This ID ensures data is sent to your Analytics property.