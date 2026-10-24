import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f) for f in files]
W = max(i.width for i in ims); H = sum(i.height for i in ims)
c = Image.new('RGB', (W, H)); y = 0
for i in ims:
    c.paste(i, (0, y)); y += i.height
c.save(out)
