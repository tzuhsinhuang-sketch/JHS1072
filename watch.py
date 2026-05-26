"""
用法：python watch.py
存檔任何 .md 檔後自動重產對應的 .html
按 Ctrl+C 停止
"""

import time, sys, io, re
import html as _html
import markdown
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = Path(__file__).parent

def render_wf_block(content: str) -> str:
    raw = _html.unescape(content).strip()
    title = ''
    options = []
    bet = ''
    actions = []

    for line in raw.splitlines():
        line = line.strip()
        if line.startswith('title:'):
            title = line[6:].strip()
        elif line.startswith('option:'):
            parts = [p.strip() for p in line[7:].split('|')]
            desc = parts[0].replace('\\n', '<br>') if parts else ''
            price = parts[1] if len(parts) > 1 else ''
            selected = len(parts) > 2 and parts[2].strip().lower() == 'selected'
            options.append((desc, price, selected))
        elif line.startswith('bet:'):
            bet = line[4:].strip()
        elif line.startswith('action:'):
            parts = [p.strip() for p in line[7:].split('|')]
            label = parts[0]
            style = parts[1].lower() if len(parts) > 1 else 'secondary'
            actions.append((label, style))

    title_html = ''
    if title:
        title_html = (
            '<div style="text-align:center;padding:14px 16px;'
            'font-weight:700;font-size:15px;letter-spacing:.06em;'
            'background:#f6f8fa;border-bottom:1px solid #d0d7de;">'
            + _html.escape(title) +
            '</div>'
        )

    opts_parts = []
    for desc, price, selected in options:
        border = '#0969da' if selected else '#d0d7de'
        bg = '#f0f6ff' if selected else '#fff'
        p_color = '#0969da' if selected else '#1f2328'
        p_border = '#c2d8f5' if selected else '#d0d7de'
        opts_parts.append(
            f'<div style="flex:1;border:2px solid {border};border-radius:8px;'
            f'padding:14px 12px;background:{bg};display:flex;flex-direction:column;min-height:140px;">'
            f'<div style="font-size:13px;color:#656d76;text-align:center;flex:1;line-height:1.8;">{desc}</div>'
            f'<div style="text-align:center;font-weight:700;font-size:16px;color:{p_color};'
            f'padding-top:10px;border-top:1px solid {p_border};margin-top:10px;">{_html.escape(price)}</div>'
            f'</div>'
        )
    opts_html = ''.join(opts_parts)

    bet_html = ''
    if bet:
        bet_html = (
            '<div style="padding:12px 14px 12px;text-align:center;">'
            '<div style="font-size:13px;color:#656d76;letter-spacing:.08em;margin-bottom:8px;">BET</div>'
            '<div style="display:flex;justify-content:center;align-items:center;gap:12px;">'
            '<button style="width:30px;height:30px;border:1px solid #d0d7de;border-radius:6px;background:#f6f8fa;font-size:16px;cursor:default;">−</button>'
            f'<span style="font-size:13px;color:#1f2328;min-width:80px;text-align:center;">{_html.escape(bet)}</span>'
            '<button style="width:30px;height:30px;border:1px solid #d0d7de;border-radius:6px;background:#f6f8fa;font-size:16px;cursor:default;">+</button>'
            '</div>'
            '</div>'
        )

    acts_html = ''
    if actions:
        btns = ''
        for label, style in actions:
            if style == 'primary':
                btns += (
                    '<button style="flex:1;padding:9px 0;border:none;border-radius:8px;'
                    f'background:#0969da;color:#fff;font-size:14px;font-weight:600;cursor:default;">{_html.escape(label)}</button>'
                )
            else:
                btns += (
                    '<button style="flex:1;padding:9px 0;border:1px solid #d0d7de;border-radius:8px;'
                    f'background:#f6f8fa;font-size:14px;cursor:default;">{_html.escape(label)}</button>'
                )
        acts_html = f'<div style="display:flex;gap:10px;padding:0 14px 14px;">{btns}</div>'

    return (
        '<div style="display:flex;justify-content:center;padding:16px 0 24px;">'
        '<div style="border:2px solid #d0d7de;border-radius:12px;width:460px;overflow:hidden;'
        "background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
        'box-shadow:0 4px 12px rgba(0,0,0,.08);">'
        + title_html
        + '<div style="display:flex;gap:10px;padding:14px 14px 10px;">' + opts_html + '</div>'
        + bet_html
        + acts_html
        + '</div></div>'
    )


def render_board_block(content: str) -> str:
    raw = _html.unescape(content).strip()
    rows = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            rows.append([c.strip() for c in line.split('|')])

    if not rows:
        return ''

    col_count = max(len(r) for r in rows)
    CW = 58   # cell width px
    CH = 46   # cell height px  — 4 cols × CW : (header + 3 rows × CH) ≈ 6:4
    HH = 20   # header row height px

    header_base = (
        f'width:{CW}px;height:{HH}px;'
        'text-align:center;vertical-align:middle;'
        'border:1px solid #d0d7de;padding:0;'
    )
    cell_base = (
        f'width:{CW}px;height:{CH}px;'
        'text-align:center;vertical-align:middle;'
        'border:1px solid #d0d7de;padding:0;'
    )

    header_html = ''.join(
        f'<th style="{header_base}background:#f6f8fa;font-size:11px;font-weight:600;'
        f'color:#656d76;letter-spacing:.04em;">{_html.escape(rows[0][i] if i < len(rows[0]) else "")}</th>'
        for i in range(col_count)
    )

    body_html = ''
    for row in rows[1:]:
        cells = ''.join(
            f'<td style="{cell_base}font-size:13px;font-weight:600;color:#1f2328;">'
            f'{_html.escape(row[i] if i < len(row) else "")}</td>'
            for i in range(col_count)
        )
        body_html += f'<tr>{cells}</tr>'

    return (
        '<div style="margin:14px 0 22px;">'
        '<table style="border-collapse:collapse;table-layout:fixed;">'
        f'<thead><tr>{header_html}</tr></thead>'
        f'<tbody>{body_html}</tbody>'
        '</table></div>'
    )


CSS = """
:root {
  --bg: #ffffff; --surface: #f6f8fa; --border: #d0d7de;
  --text: #1f2328; --muted: #656d76; --accent: #0969da;
  --accent-dim: rgba(9,105,218,.08);
  --table-head: #f6f8fa; --row-alt: #f6f8fa; --code-bg: #f6f8fa;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 18px; }

#sidebar {
  position: fixed; top: 0; left: 0; width: 255px; height: 100vh;
  overflow-y: auto; background: var(--surface); border-right: 1px solid var(--border);
  padding: 24px 14px; font-size: 15px;
}
#sidebar .sidebar-title { font-size: 14px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 14px; padding: 0 8px; }
#sidebar a { display: block; padding: 6px 10px; color: var(--muted); text-decoration: none; border-radius: 4px; transition: all .15s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#sidebar a:hover { color: var(--accent); background: var(--accent-dim); }
#sidebar .lv2 { font-weight: 600; color: var(--text); margin-top: 6px; }
#sidebar .lv3 { padding-left: 22px; }

#main { margin-left: 255px; max-width: 900px; padding: 48px 40px; }

h1 { font-size: 30px; font-weight: 700; margin-bottom: 6px; }
.meta { color: var(--muted); font-size: 15px; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }

h2 {
  font-size: 20px; font-weight: 700; color: var(--text);
  margin: 52px 0 18px; padding: 10px 14px;
  background: var(--accent-dim);
  border-left: 4px solid var(--accent);
  border-radius: 0 6px 6px 0;
}
h3 {
  font-size: 17px; font-weight: 600; color: #0550ae;
  margin: 32px 0 10px;
}
h4 {
  font-size: 16px; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: .09em; margin: 22px 0 8px;
}

p { margin-bottom: 12px; font-size: 16px; }
ul, ol { font-size: 16px; margin: 6px 0 16px; padding-left: 22px; }
li { margin-bottom: 4px; line-height: 1.6; }
strong { color: var(--text); }

table { width: 100%; border-collapse: collapse; margin: 12px 0 22px; font-size: 16px; }
thead th { background: var(--table-head); color: var(--muted); font-size: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; padding: 10px 14px; border: 1px solid var(--border); text-align: left; }
tbody td { padding: 9px 14px; border: 1px solid var(--border); vertical-align: top; }
tbody tr:nth-child(even) { background: var(--row-alt); }
tbody tr:hover { background: rgba(9,105,218,.04); }

pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 6px; padding: 14px 18px; margin: 14px 0; font-size: 16px; overflow-x: auto; }
code { font-family: "SFMono-Regular", Consolas, monospace; font-size: 15px; background: var(--code-bg); padding: 2px 5px; border-radius: 3px; }
pre code { background: none; padding: 0; }

blockquote { border-left: 3px solid var(--border); padding: 8px 14px; margin: 14px 0; color: var(--muted); font-size: 16px; }
blockquote p { margin: 0; }
hr { border: none; border-top: 1px solid var(--border); margin: 36px 0; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

details { margin: 12px 0 22px; border: 1px solid var(--border); border-radius: 6px; width: 100%; }
details summary { padding: 10px 14px; cursor: pointer; color: var(--accent); font-weight: 600; user-select: none; list-style: none; }
details summary::-webkit-details-marker { display: none; }
details summary::before { content: '▶ '; font-size: 14px; }
details[open] summary::before { content: '▼ '; }
details summary:hover { background: var(--accent-dim); border-radius: 6px; }
details[open] summary { border-bottom: 1px solid var(--border); border-radius: 6px 6px 0 0; }
details > .mermaid { padding: 20px; background: var(--surface); border-radius: 0 0 6px 6px; overflow-x: auto; }
details > .mermaid svg { display: block; }
#sidebar .toc-row { display: flex; align-items: center; margin-top: 6px; }
#sidebar .toc-row a.lv2 { padding-left: 4px; margin-top: 0; flex: 1; }
#sidebar .toc-arrow { font-size: 10px; color: var(--muted); cursor: pointer; padding: 6px 2px 6px 10px; user-select: none; flex-shrink: 0; }
#sidebar .toc-arrow:hover { color: var(--accent); }
"""

JS = """
function slugify(text) {
  return text.trim().replace(/\\s+/g, '-').replace(/[<>"\\\\/?#[\\]{}|^`]/g, '');
}
const toc = document.getElementById('toc');
const headings = [...document.querySelectorAll('h2,h3')];
headings.forEach((el, i) => { el.id = slugify(el.textContent) || ('h' + i); });
let currentSubs = null;
headings.forEach((el, i) => {
  if (el.tagName === 'H2') {
    let hasSub = false;
    for (let j = i + 1; j < headings.length; j++) {
      if (headings[j].tagName === 'H2') break;
      if (headings[j].tagName === 'H3') { hasSub = true; break; }
    }
    const a = document.createElement('a');
    a.href = '#' + el.id;
    a.textContent = el.textContent;
    a.className = 'lv2';
    if (hasSub) {
      const row = document.createElement('div');
      row.className = 'toc-row';
      const arrow = document.createElement('span');
      arrow.textContent = '▶';
      arrow.className = 'toc-arrow';
      row.appendChild(arrow);
      row.appendChild(a);
      const subs = document.createElement('div');
      subs.style.display = 'none';
      toc.appendChild(row);
      toc.appendChild(subs);
      arrow.addEventListener('click', () => {
        const hidden = subs.style.display === 'none';
        subs.style.display = hidden ? '' : 'none';
        arrow.textContent = hidden ? '▼' : '▶';
      });
      currentSubs = subs;
    } else {
      toc.appendChild(a);
      currentSubs = null;
    }
  } else {
    const a = document.createElement('a');
    a.href = '#' + el.id;
    a.textContent = el.textContent;
    a.className = 'lv3';
    (currentSubs || toc).appendChild(a);
  }
});
const firstP = document.querySelector('h1 + p');
if (firstP) firstP.className = 'meta';
"""

def build(md_path: Path):
    html_path = md_path.with_suffix('.html')
    md_text = md_path.read_text(encoding='utf-8')
    body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'nl2br'])
    body = re.sub(
        r'<pre><code[^>]*class="(?:language-)?wf"[^>]*>(.*?)</code></pre>',
        lambda m: render_wf_block(m.group(1)),
        body, flags=re.DOTALL
    )
    body = re.sub(
        r'<pre><code[^>]*class="(?:language-)?board"[^>]*>(.*?)</code></pre>',
        lambda m: render_board_block(m.group(1)),
        body, flags=re.DOTALL
    )
    h1 = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = h1.group(1) if h1 else md_path.stem

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
<nav id="sidebar">
  <div class="sidebar-title">目錄</div>
  <div id="toc"></div>
</nav>
<main id="main">
  {body}
</main>
<script>{JS}</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false, theme:'default', useMaxWidth: true}});
const allDetails = [...document.querySelectorAll('details')];
allDetails.forEach(d => d.open = true);
void document.body.offsetHeight;
mermaid.run().then(() => {{
  document.querySelectorAll('.mermaid svg').forEach(svg => {{
    const vb = svg.getAttribute('viewBox');
    if (vb) {{
      const parts = vb.trim().split(/\s+/).map(parseFloat);
      svg.removeAttribute('width');
      svg.removeAttribute('height');
      svg.style.width = parts[2] + 'px';
      svg.style.height = parts[3] + 'px';
    }}
  }});
  allDetails.forEach(d => d.open = false);
}});
</script>
</body>
</html>"""

    html_path.write_text(html, encoding='utf-8')
    print(f'[更新] {html_path.name}')


class MDHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            build(Path(event.src_path))

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            build(Path(event.src_path))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(f'監聽中：{WATCH_DIR}')
    print('存檔 .md 後自動更新對應 .html，按 Ctrl+C 停止\n')

    observer = Observer()
    observer.schedule(MDHandler(), str(WATCH_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
