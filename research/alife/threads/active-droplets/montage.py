import sys
from PIL import Image
fs=sys.argv[2:]
ims=[Image.open(f) for f in fs]
w=max(i.width for i in ims); h=sum(i.height for i in ims)+5*len(ims)
o=Image.new('L',(w,h),128); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height+5
o.save(sys.argv[1])
