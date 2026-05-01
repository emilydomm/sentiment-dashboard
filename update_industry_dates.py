import json, glob, os

dates = sorted([
    os.path.basename(f).replace('.json', '')
    for f in glob.glob('docs/data/industry/*.json')
    if not f.endswith('dates.json')
])
with open('docs/data/industry/dates.json', 'w', encoding='utf-8') as f:
    json.dump(dates, f, ensure_ascii=False)
print(f'updated {len(dates)} dates')
