#!/usr/bin/env python3
import json, glob, os

CLIENTS = []
for f in sorted(glob.glob("batch*.json")):
    with open(f) as fh:
        data = json.load(fh)
        for k, v in data.items():
            CLIENTS.append(v)

VALUE_MAP = {
    1: "高", 2: "高", 3: "中", 4: "高", 5: "高",
    6: "中", 7: "中", 8: "高", 9: "高", 10: "中",
    11: "中", 12: "低", 13: "中", 14: "高", 15: "中",
    16: "中", 17: "高"
}

SHORT_NAME = {
    "伊顿（中国）投资有限公司": "伊顿（中国）",
    "思爱普（中国）有限公司": "思爱普 SAP",
    "上海建科工程咨询有限公司": "上海建科工程咨询",
    "欧加隆（上海）医药科技有限公司": "欧加隆（上海）",
    "远景动力技术（江苏）有限公司": "远景动力",
    "益科德（上海）有限公司": "益科德 Exyte",
    "上海建科咨询集团股份有限公司": "上海建科咨询集团",
    "村田（中国）投资有限公司": "村田（中国）",
    "捷普科技（上海）有限公司": "捷普科技",
    "上海皓元医药股份有限公司": "皓元医药",
    "浙江天正电气股份有限公司": "天正电气",
    "上海朗阁教育科技股份有限公司": "朗阁教育",
    "上海罗莱生活科技有限公司": "罗莱生活",
    "3M中国有限公司": "3M中国",
    "仲利国际融资租赁有限公司": "仲利国际",
    "上海振华重工（集团）股份有限公司": "振华重工",
    "赛诺菲（中国）投资有限公司": "赛诺菲（新）",
}

def get_brief(news_list):
    if not news_list:
        return "暂无新动态"
    brief = news_list[0]
    if len(brief) > 50:
        brief = brief[:50] + "..."
    return brief

# ════ Summary cards ════
cards_html = ""
for i, c in enumerate(CLIENTS):
    idx = i + 1
    v = VALUE_MAP[idx]
    name = SHORT_NAME.get(c["name"], c["name"])
    brief = get_brief(c.get("news", []))
    cards_html += f"""<div class="summary-card">
  <div class="num">#{idx}</div>
  <div class="name">{name}</div>
  <div class="brief">{brief}</div>
  <span class="value {v}">{v}</span>
</div>
"""

# ════ Detail sections ════
detail_html = ""
for i, c in enumerate(CLIENTS):
    idx = i + 1
    v = VALUE_MAP[idx]
    vb_label = {"高": "高价值", "中": "中价值", "低": "低价值"}[v]
    
    news = c.get("news", [])
    hr = c.get("hr_info", "暂无")
    url = c.get("url", "")
    url_title = c.get("url_title", "")
    
    news_li = "\n".join([f"    <li>{n}</li>" for n in news]) if news else "    <li>暂无最新动态</li>"
    
    src_html = ""
    if url and url_title:
        src_html = f'<p class="src"><a href="{url}" target="_blank">{url_title}</a></p>'
    elif url:
        src_html = f'<p class="src"><a href="{url}" target="_blank">{url}</a></p>'
    
    detail_html += f"""<div class="detail">
  <h3>{idx}. {c["name"]} <span class="val-badge {v}">{vb_label}</span></h3>
  <div class="label">📰 最新动态</div>
  <ul>
{news_li}
  </ul>
  <div class="label">💼 招聘动态</div>
  <p style="font-size:14px;">{hr}</p>
  <div class="label">🔗 信息来源</div>
  {src_html if src_html else '<p style="font-size:12px;color:#9ca3af;">暂无可点来源</p>'}
</div>
"""

FULL_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>客户每日情报 - 2026-07-13</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; color:#1a1a2e; line-height:1.6; margin:0; }}
  .summary-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; margin-bottom:32px; }}
  .summary-card {{ background:#fff; border-radius:10px; padding:16px 18px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,.06); }}
  .summary-card .num {{ font-size:11px; color:#6b7280; margin-bottom:4px; }}
  .summary-card .name {{ font-size:15px; font-weight:700; margin-bottom:6px; }}
  .summary-card .brief {{ font-size:13px; color:#6b7280; line-height:1.5; }}
  .summary-card .value {{ display:inline-block; margin-top:10px; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
  .value.高 {{ background:#ecfdf5; color:#059669; }}
  .value.中  {{ background:#fffbeb; color:#d97706; }}
  .value.低  {{ background:#f3f4f6; color:#6b7280; }}
  
  .detail {{ margin-bottom:28px; background:#fff; border-radius:10px; padding:20px 24px; border:1px solid #e5e7eb; }}
  .detail h3 {{ font-size:16px; font-weight:700; margin:0 0 12px 0; padding-bottom:8px; border-bottom:2px solid #2563eb; display:flex; align-items:center; gap:8px; }}
  .detail .val-badge {{ font-size:11px; padding:2px 10px; border-radius:12px; font-weight:600; }}
  .val-badge.高 {{ background:#ecfdf5; color:#059669; }}
  .val-badge.中  {{ background:#fffbeb; color:#d97706; }}
  .val-badge.低  {{ background:#f3f4f6; color:#6b7280; }}
  .detail .label {{ font-size:12px; font-weight:700; color:#6b7280; margin:10px 0 4px; letter-spacing:.5px; }}
  .detail li {{ font-size:14px; padding:5px 0; border-bottom:1px solid #f3f4f6; }}
  .detail li:last-child {{ border-bottom:none; }}
  .detail ul {{ list-style:none; padding:0; margin:0; }}
  .detail .src {{ font-size:12px; color:#2563eb; word-break:break-all; }}
  .detail .src a {{ color:#2563eb; text-decoration:none; }}
  .detail .src a:hover {{ text-decoration:underline; }}
</style>
</head>
<body>

<!-- ════ 摘要卡片 ════ -->
<div class="summary-grid">
{cards_html}</div>

<!-- ════ 详细情报 ════ -->
{detail_html}
</body>
</html>
"""

with open("客户每日情报.html", "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated 客户每日情报.html ({len(FULL_HTML)} bytes, {len(CLIENTS)} clients)")
