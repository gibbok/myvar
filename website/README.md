# myvar-dev

myvar.dev website

## Development

Run the development server with drafts enabled:

```bash
make start
```

## Setup

Generate syntax highlighting CSS:

```bash
hugo gen chromastyles --style=dracula > assets/css/syntax.css
```

## Book banner analytics

Both links in the free TypeScript book banner send the GA4 custom event
`free_edition_banner_click`, with `link_url` containing the destination URL.
This reuses the existing Google tag and consent settings without delaying navigation.

After deployment, accept analytics cookies and click the banner title or
"Read the free book". In Google Analytics, check Realtime for
`free_edition_banner_click` (or DebugView when debug mode is enabled).
Repeat for the other link, including its nested text/arrow, and confirm that
each activation records one custom event. Links elsewhere should not send this event.
Google Analytics may also record its standard outbound `click` event separately.
