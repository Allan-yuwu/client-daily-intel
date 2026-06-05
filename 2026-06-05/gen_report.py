#!/usr/bin/env python3
import json

# Load raw intel
with open('intel_raw.json', 'r', encoding='utf-8') as f:
    clients = json.load(f)

# ── Generate HTML report ──
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>客户每日情报 - 2026-06-05</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; color:#1a1a2e; line-height:1.6; margin:0; }
  .summary-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; margin-bottom:32px; }
  .summary-card { background:#fff; border-radius:10px; padding:16px 18px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,.06); }
  .summary-card .num { font-size:11px; color:#6b7280; margin-bottom:4px; }
  .summary-card .name { font-size:15px; font-weight:700; margin-bottom:6px; }
  .summary-card .brief { font-size:13px; color:#6b7280; line-height:1.5; }
  .summary-card .value { display:inline-block; margin-top:10px; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }
  .value.high { background:#ecfdf5; color:#059669; }
  .value.mid  { background:#fffbeb; color:#d97706; }
  .value.low  { background:#f3f4f6; color:#6b7280; }
  
  .detail { margin-bottom:28px; background:#fff; border-radius:10px; padding:20px 24px; border:1px solid #e5e7eb; }
  .detail h3 { font-size:16px; font-weight:700; margin:0 0 12px 0; padding-bottom:8px; border-bottom:2px solid #2563eb; display:flex; align-items:center; gap:8px; }
  .detail .val-badge { font-size:11px; padding:2px 10px; border-radius:12px; font-weight:600; }
  .val-badge.high { background:#ecfdf5; color:#059669; }
  .val-badge.mid  { background:#fffbeb; color:#d97706; }
  .val-badge.low  { background:#f3f4f6; color:#6b7280; }
  .detail .label { font-size:12px; font-weight:700; color:#6b7280; margin:10px 0 4px; letter-spacing:.5px; }
  .detail li { font-size:14px; padding:5px 0; border-bottom:1px solid #f3f4f6; }
  .detail li:last-child { border-bottom:none; }
  .detail ul { list-style:none; padding:0; margin:0; }
  .detail .src { font-size:12px; color:#2563eb; word-break:break-all; }
  .detail .src a { color:#2563eb; text-decoration:none; }
  .detail .src a:hover { text-decoration:underline; }
</style>
</head>
<body>

<!-- ════ 摘要卡片 ════ -->
<div class="summary-grid">
'''

for c in clients:
    html += f'''
<div class="summary-card">
  <div class="num">#{c['id']}</div>
  <div class="name">{c['short_name']}</div>
  <div class="brief">{c['card_brief']}</div>
  <span class="value {'high' if c['value']=='高' else 'mid' if c['value']=='中' else 'low'}">{c['value']}</span>
</div>
'''

html += '''
</div>

<!-- ════ 详细情报 ════ -->
'''

value_map = {'高': '高价值', '中': '中价值', '低': '低价值'}
for c in clients:
    v = c['value']
    html += f'''
<div class="detail">
  <h3>{c['id']}. {c['name']} <span class="val-badge {'high' if v=='高' else 'mid' if v=='中' else 'low'}">{value_map[v]}</span></h3>
  <div class="label">📰 最新动态</div>
  <ul>
'''
    for news in c['news']:
        html += f'    <li>{news}</li>\n'
    html += f'''  </ul>
  <div class="label">💼 招聘动态</div>
  <p style="font-size:14px;">{c['recruitment']}</p>
  <div class="label">🔗 信息来源</div>
  <p class="src"><a href="{c['source_url']}" target="_blank">{c['source_text']}</a></p>
</div>
'''

html += '''
</body>
</html>
'''

with open('客户每日情报.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ HTML report generated: 客户每日情报.html")

# ── Update index.html REPORTS array ──
import re

index_path = '../index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_array = 'var REPORTS = ["2026-06-04","2026-06-03","2026-06-02","2026-06-01","2026-05-29","2026-05-28","2026-05-27","2026-05-26","2026-05-25","2026-05-21","2026-05-20","2026-05-19","2026-05-18","2026-05-12","2026-05-11"];'
new_array = 'var REPORTS = ["2026-06-05","2026-06-04","2026-06-03","2026-06-02","2026-06-01","2026-05-29","2026-05-28","2026-05-27","2026-05-26","2026-05-25","2026-05-21","2026-05-20","2026-05-19","2026-05-18","2026-05-12","2026-05-11"];'

if old_array in content:
    content = content.replace(old_array, new_array)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ index.html REPORTS array updated")
else:
    print("⚠️ REPORTS array not found in index.html, trying regex...")
    pattern = r'var REPORTS = \[.*?\];'
    match = re.search(pattern, content)
    if match:
        content = content.replace(match.group(0), new_array)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ index.html REPORTS array updated via regex")
    else:
        print("❌ Could not update REPORTS array")

print("Done!")
