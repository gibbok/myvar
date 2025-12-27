#!/bin/bash
# Setup script to configure git hooks

HOOK_PATH=".git/hooks/post-checkout"

echo "Creating post-checkout hook..."
cat <<EOF > "$HOOK_PATH"
#!/bin/sh
# Automatically assume-unchanged for generator/drafts/content.md after checkout
git update-index --assume-unchanged generator/drafts/content.md
echo "Applied assume-unchanged to generator/drafts/content.md"
EOF

chmod +x "$HOOK_PATH"
echo "Hook created and made executable at $HOOK_PATH"

./"$HOOK_PATH"
