"""README.md from README.md.in, reports/table.md and reports/summary.json (results block and remaining items)."""
import json
from pathlib import Path

B = Path("/home/user/evalwork/bundles")
s = json.loads((B / "reports" / "summary.json").read_text())
text = (B / "README.md.in").read_text()
text = text.replace("{{TABLE}}", (B / "reports" / "table.md").read_text().strip())
text = text.replace("{{RESULTS}}", (B / "reports" / "results.md").read_text().strip())
text = text.replace("{{REMAINING}}", (B / "reports" / "remaining.md").read_text().strip())
(B / "README.md").write_text(text)
print(len(text.split()), "words")
