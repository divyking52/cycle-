from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
footer_css = (root / "assets" / "site-footer.css").read_text(encoding="utf-8")
footer_html = (root / "assets" / "site-footer.html").read_text(encoding="utf-8").strip()

support = r"""
/* Shared footer support (token/layout fallbacks) */
.container { width: min(100% - 2.5rem, var(--max, 1240px)); margin-inline: auto; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
.topo { background-image: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 60c20-30 40-30 60 0s40 30 60 0' fill='none' stroke='%23899B81' stroke-opacity='0.18' stroke-width='1'/%3E%3C/svg%3E"); }
.logo { font-family: var(--font-display); font-weight: 700; font-size: 1.15rem; display: inline-flex; align-items: center; gap: 0.55rem; text-decoration: none; }
.logo-mark { width: 1.55rem; height: 1.55rem; border-radius: 50%; background: conic-gradient(from 210deg, var(--orange), var(--sage, #899B81), var(--forest), var(--orange)); position: relative; display: inline-block; }
.logo-mark::after { content: ""; position: absolute; inset: 4px; border-radius: 50%; background: var(--cream, #F5F1E8); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.55rem; padding: 0.95rem 1.45rem; border-radius: var(--radius-sm, 4px); border: 1.5px solid transparent; font-weight: 600; font-size: 0.92rem; cursor: pointer; font-family: inherit; text-decoration: none; }
.btn-primary { background: var(--orange); color: #fff; }
"""

if "Shared footer support" not in footer_css:
    footer_css = support + "\n" + footer_css
    (root / "assets" / "site-footer.css").write_text(footer_css, encoding="utf-8")

boot_js = """
<script>
(function(){
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
  const news = document.getElementById('newsletterForm');
  if (news && !news.dataset.bound) {
    news.dataset.bound = '1';
    news.addEventListener('submit', function(e){
      e.preventDefault();
      alert('Thanks for joining the Wildspoke list. Hook this up to your newsletter provider when ready.');
      news.reset();
    });
  }
})();
</script>
"""

style_block = '<link rel="stylesheet" href="assets/site-footer.css" />\n'
pages = [p for p in root.glob("*.html") if p.name != "index.html"]
updated = []

for page in pages:
    text = page.read_text(encoding="utf-8")
    if "assets/site-footer.css" not in text:
        if "</head>" not in text:
            print("NO HEAD", page.name)
            continue
        text = text.replace("</head>", style_block + "</head>", 1)

    new_text, n = re.subn(r"<footer\b[\s\S]*?</footer>", footer_html, text, count=1, flags=re.I)
    if n == 0:
        if "</body>" not in text:
            print("NO FOOTER/BODY", page.name)
            continue
        new_text = text.replace("</body>", footer_html + "\n" + boot_js + "\n</body>", 1)
    elif "Hook this up to your newsletter provider when ready" not in new_text:
        new_text = new_text.replace("</body>", boot_js + "\n</body>", 1)

    page.write_text(new_text, encoding="utf-8")
    updated.append(page.name)

print("updated", len(updated))
print("\n".join(updated))
