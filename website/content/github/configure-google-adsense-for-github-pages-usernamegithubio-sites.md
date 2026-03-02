+++
title = 'Configure Google AdSense for GitHub Pages `username.github.io` sites'
date = 2026-03-01T18:32:59.052998
draft = false
tags = ['AdSense', 'GitHub-Pages', 'ads.txt']
description = 'Configure Google AdSense and verify `ads.txt` for GitHub Pages `username.github.io` sites without custom domains.'
+++

### Overview
Configure Google AdSense and verify `**ads.txt**` for GitHub Pages sites utilizing the `**username.github.io**` domain, specifically addressing setups without custom domains.

### Key Insights

*   A GitHub repository named `**<GITHUB_USERNAME>.github.io**` automatically deploys its content to the root URL `https://<GITHUB_USERNAME>.github.io/`.
*   This **root repository** serves as the base for other GitHub Pages sites, allowing shared assets like `favicon.ico` to be placed here and inherited by `https://<GITHUB_USERNAME>.github.io/<REPO_NAME>/` pages.
*   The `**ads.txt**` file for Google AdSense verification **must** reside in the `**root directory**` of the `**username.github.io**` repository.
*   AdSense verification can take several days to complete after file upload.

### Technical Details

### GitHub Pages `**username.github.io**` Setup

GitHub Pages typically hosts content at `https://<GITHUB_USERNAME>.github.io/<REPO_NAME>/`. A special convention exists for personal and organization homepages:

*   **Root Domain Hosting:** Creating a repository named `**<GITHUB_USERNAME>.github.io**` (or `**<GITHUB_ORGANIZATION>.github.io**` for organizations) automatically publishes its content directly to `https://<GITHUB_USERNAME>.github.io/`.
    *   **Organization Example:** `https://brickmmo.github.io/` is served from the `brickmmo.github.io` repository.

*   **Shared Root Functionality:** This **root domain** setup provides a central location for shared web assets. Files placed in the `**username.github.io**` repository's **root**, such as `favicon.ico`, are accessible to and can be utilized by sub-pages like `https://<GITHUB_USERNAME>.github.io/<REPO_NAME>/`.

### Google AdSense `**ads.txt**` Verification

Verify your site with Google AdSense by uploading an `**ads.txt**` file containing your publisher information to your site's `**root directory**`.

1.  **Create `**ads.txt**` File:** Create a plain text file named `**ads.txt**`.
2.  **Add Publisher ID:** Insert the following line into the `**ads.txt**` file, replacing `pub-0000000000000000` with your actual Google AdSense publisher ID:
    ```
    google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
    ```
3.  **Upload to `**Root Directory**`:** Upload the `**ads.txt**` file to the `**root directory**` of your `**<GITHUB_USERNAME>.github.io**` repository.
    *   **Crucial:** The file must be directly accessible at `https://<GITHUB_USERNAME>.github.io/ads.txt`, not within any subdirectories.
4.  **Verify Accessibility:** Confirm the `**ads.txt**` file is publicly accessible via its direct URL (e.g., `https://codeadamca.github.io/ads.txt`).
5.  **Initiate AdSense Check:** Navigate to your AdSense account's site list and click "Check for updates" for your verified site.
6.  **Verification Time:** AdSense verification can take up to a few days.