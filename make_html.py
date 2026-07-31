# -*- coding: utf-8 -*-
"""Convert 计网27重新起航.md to a self-contained HTML with embedded images."""
import re, os, base64, markdown

def img_to_base64(path):
    """Read image file and return base64 data URI."""
    if not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    mime = {
        '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.gif': 'image/gif', '.webp': 'image/webp'
    }.get(ext, 'image/png')
    with open(path, 'rb') as f:
        data = f.read()
    return f'data:{mime};base64,{base64.b64encode(data).decode("ascii")}'

def find_in_vault(filename, vault_root):
    """Find an image file, searching the whole vault if direct path fails (like Obsidian)."""
    # Direct path first
    if os.path.exists(filename):
        return filename
    # Search whole vault by filename
    for root, dirs, files in os.walk(vault_root):
        if '.git' in root:
            continue
        if filename in files:
            return os.path.join(root, filename)
    return None

def replace_images(md_text, vault_root):
    """Replace ![[image]] with <img src='data:...'> in markdown."""
    def repl(match):
        img_path = match.group(1)
        full = find_in_vault(img_path, vault_root)
        data_uri = img_to_base64(full) if full else None
        if data_uri:
            return f'<img class="embed-img" src="{data_uri}" alt="{os.path.basename(img_path)}">'
        else:
            return f'<div class="missing-img">[缺失图片: {img_path}]</div>'
    return re.sub(r'!\[\[([^\]]+)\]\]', repl, md_text)

def convert_callouts(text):
    """Convert Obsidian callouts [!important] etc. to styled divs."""
    # Pattern: > [!important] title\n> content...
    # Simplest: handle the common ones by regex on the blockquote content
    return text

vault = r'D:\Obsidian\ObsidianNote'
md_path = os.path.join(vault, '计网27重新起航.md')

with open(md_path, 'r', encoding='utf-8') as f:
    md = f.read()

# 1. Replace images first
md = replace_images(md, vault)

# 2. Basic markdown → html
html_body = markdown.markdown(
    md,
    extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'sane_lists'],
    extension_configs={'codehilite': {'guess_lang': False}}
)

# 3. Style Obsidian callouts (post-process)
# Convert [!important] blocks into colored boxes
html_body = re.sub(
    r'<blockquote>\s*<p>\[!important\](.*?)</p>(.*?)</blockquote>',
    r'<div class="callout important"><div class="callout-title">📌 重点</div>\1\2</div>',
    html_body, flags=re.DOTALL
)
html_body = re.sub(
    r'<blockquote>\s*<p>\[!sidenote\](.*?)</p>(.*?)</blockquote>',
    r'<div class="callout sidenote"><div class="callout-title">💡 新理解</div>\1\2</div>',
    html_body, flags=re.DOTALL
)

# Generate full HTML
html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>计网27重新起航</title>
<style>
body {{ font-family: 'PingFang SC','Microsoft YaHei',sans-serif; max-width: 900px; margin: 0 auto; padding: 24px; line-height: 1.7; color: #222; }}
h1 {{ font-size: 1.8em; border-bottom: 2px solid #4CAF50; padding-bottom: 6px; margin-top: 40px; color: #2c3e50; }}
h2 {{ font-size: 1.4em; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 32px; color: #2c3e50; }}
h3 {{ font-size: 1.15em; margin-top: 24px; color: #34495e; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
th {{ background: #f5f5f5; }}
code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.92em; }}
pre {{ background: #282c34; color: #abb2bf; padding: 14px; border-radius: 6px; overflow-x: auto; }}
pre code {{ background: none; color: inherit; }}
.embed-img {{ max-width: 100%; margin: 12px 0; border: 1px solid #eee; border-radius: 4px; }}
.missing-img {{ color: #e74c3c; background: #fdecea; padding: 10px; border-radius: 4px; margin: 8px 0; }}
blockquote {{ border-left: 4px solid #4CAF50; margin: 16px 0; padding: 8px 16px; background: #f9f9f9; color: #555; }}
.callout {{ border-radius: 6px; padding: 4px 16px; margin: 16px 0; }}
.callout-title {{ font-weight: bold; font-size: 1em; }}
.callout.important {{ background: #fff8e1; border-left: 4px solid #ff9800; }}
.callout.important .callout-title {{ color: #e65100; }}
.callout.sidenote {{ background: #e8f5e9; border-left: 4px solid #4CAF50; }}
.callout.sidenote .callout-title {{ color: #2e7d32; }}
hr {{ border: none; border-top: 1px solid #eee; margin: 24px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

out = os.path.join(vault, '计网27重新起航.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

# Count images embedded
embedded = html.count('data:image')
missing = html.count('missing-img')
print(f'Done! {out}')
print(f'Embedded images: {embedded}')
print(f'Missing images: {missing}')
