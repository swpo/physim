"""Keep historical report generators out of the current documentation surface."""
from html import escape
from pathlib import Path
import os
import re

DOCS = Path(__file__).resolve().parents[3] / "docs"
ARCHIVE = DOCS / "archive"


def legacy_output(path):
    """Allow archive/external outputs, refusing writes to current public docs."""
    output = Path(path)
    resolved = output.resolve()
    if DOCS == resolved or (DOCS in resolved.parents and ARCHIVE not in resolved.parents):
        raise ValueError("Historical generators must write under docs/archive/ or outside docs/. "
                         "Build current documentation with scripts/build_docs.py.")
    return output


def archive_html(source, output, *, shared_assets=False):
    """Label regenerated historical reports and link back to current docs."""
    output = legacy_output(output)
    home = escape(os.path.relpath(DOCS / "index.html", output.resolve().parent), quote=True)
    source = source.replace("<html>", '<html lang="en">', 1)
    source = source.replace("</head>", '<meta name="viewport" content="width=device-width, initial-scale=1">'
                            '<meta name="robots" content="noindex"></head>', 1)
    banner = ('<aside style="padding:1rem;border:1px solid #ccd4de;margin-bottom:1.5rem;'
              'font-size:16px;background:#f6f8fa"><strong>Research archive.</strong> '
              f'Historical methods and results. <a href="{home}">Current Physim documentation</a>.</aside>')
    source = re.sub(r"(<body[^>]*>)", lambda m: m[1] + banner, source, count=1)
    if shared_assets:
        assets = os.path.relpath(DOCS / "assets", output.resolve().parent)
        source = source.replace('src="assets/', f'src="{assets}/')
    return source
