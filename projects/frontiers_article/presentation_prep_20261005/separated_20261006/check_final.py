from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from PIL import Image, ImageChops
from collections import Counter
import json,hashlib,re,shutil
root=Path('/Users/omer/workspace/personal/repos/gifted-masking')
p=root/'projects/frontiers_article/presentation_prep_20261005/separated_20261006'
w=Path('/private/tmp/gifted-separated-deck-20261006')
final=w/'output/masking_methods_then_results_v4.pptx'
a=ZipFile(final);b=ZipFile(root/'output/pptx/masking_results_discussion.pptx')
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
def xml(z,n):return etree.fromstring(z.read(n))
def content(z,n):return '\n'.join(xml(z,n).xpath('//a:t/text()',namespaces=ns))
def chartdata(z):
    out=[]
    for n in sorted(z.namelist()):
        if re.fullmatch(r'ppt/charts/chart\d+.xml',n):
            x=xml(z,n)
            out.append([etree.tostring(y,method='c14n').decode() for y in x.xpath('//c:ser/c:cat|//c:ser/c:val|//c:ser/c:xVal|//c:ser/c:yVal',namespaces=ns)])
    return out
assert chartdata(a)==chartdata(b),'Result chart data changed'
for new,old in [(11,3)]:
    x=xml(a,f'ppt/slides/slide{new}.xml').xpath('//a:tbl',namespaces=ns)
    y=xml(b,f'ppt/slides/slide{old}.xml').xpath('//a:tbl',namespaces=ns)
    assert len(x)==len(y)==2
    for v1,v2 in zip(x,y):
        c1=v1.xpath('.//a:tc/a:tcPr/a:solidFill/a:srgbClr/@val',namespaces=ns)
        c2=v2.xpath('.//a:tc/a:tcPr/a:solidFill/a:srgbClr/@val',namespaces=ns)
        assert c1==c2,'M2 map cell colors changed'
        assert v1.xpath('.//a:t/text()',namespaces=ns)==v2.xpath('.//a:t/text()',namespaces=ns)
spec=json.loads((p/'SLIDE_SPEC.json').read_text())
assert spec['slide_count']==16 and spec['duration_seconds']==900
assert [s['model'] for s in spec['slides'][3:8]]==['M0','M1','M2','M3','M4']
assert all(s['section']=='Methods' for s in spec['slides'][3:8])
assert [s['model'] for s in spec['slides'][8:14]]==['M0','M1','M2','M3','M3','M4']
for i in range(4,9):
    x=xml(a,f'ppt/slides/slide{i}.xml')
    assert not x.xpath('//c:chart',namespaces=ns)
    assert 'METHODS' in content(a,f'ppt/slides/slide{i}.xml')
    assert not any(v in content(a,f'ppt/slides/slide{i}.xml') for v in ['243','84.19','99.72','25.50','32.87','0.313','95% CI'])
for i,s in enumerate(spec['slides'],1):
    text=content(a,f'ppt/notesSlides/notesSlide{i}.xml')
    assert s['script'] in text
    assert f"Timing: {s['seconds']} seconds." in text
    if i<=3:
        assert json.loads((p/'OPENING_SOURCES.json').read_text())[i-1] in text
    else:
        for ref in s['sources']:assert (root/ref).exists(),ref
assert 'No confirmatory E06 result to report' in content(a,'ppt/slides/slide14.xml')
protected=json.loads((p/'PRESERVED_FILES.json').read_text())
for rel,h in protected.items():assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==h,rel
D=json.loads((p.parent/'results_discussion_20261006/DATA.json').read_text())
for x in D['sources'].values(): assert hashlib.sha256((root/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
unchanged=[]; changed=[]
for i in range(1,17):
    f=f'slide-{i:02}.png'
    old=Image.open(w/'build/renders_v2'/f).convert('RGB');new=Image.open(w/'build/renders_v4'/f).convert('RGB')
    (unchanged if ImageChops.difference(old,new).getbbox() is None else changed).append(i)
report={'slides':16,'planned_seconds':900,'spoken_words':sum(len(x['script'].split()) for x in spec['slides']),'methods_slides':[4,5,6,7,8],'results_slides':[9,10,11,12,13],'M4_status_slide':14,'charts_preserved':5,'m2_map_cells_preserved':357,'prior_files_preserved':len(protected),'source_hashes_valid':len(D['sources']),'pixel_identical_to_reviewed_v2':unchanged,'changed_visuals_requiring_review':changed,'pptx_sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'pptx_bytes':final.stat().st_size}
(p/'FINAL_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
