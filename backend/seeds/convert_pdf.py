#!/usr/bin/env python3
"""
PDF → 静态 HTML 查看器转换脚本
将高考数学 PDF 转换为每页高质量 WebP 图片 + 带导航的精美 HTML 查看器
"""
import fitz
import os
import sys
import json
from pathlib import Path

def convert_pdf_to_html_viewer(
    pdf_path: str,
    output_dir: str,
    dpi: int = 180,
    quality: int = 85,
):
    """
    将 PDF 转换为分页 WebP 图片 + 自包含 HTML 查看器

    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        dpi: 渲染分辨率 (DPI)，180 适合高清屏幕阅读数学公式
        quality: WebP 质量 (1-100)，85 兼顾清晰度与文件大小
    """
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 渲染缩放因子: PDF 默认 72 DPI, 目标 DPI 需乘以此系数
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    print(f"PDF: {pdf_path}")
    print(f"总页数: {total_pages}")
    print(f"分辨率: {dpi} DPI")
    print(f"质量: {quality}")
    print(f"输出目录: {output_dir}")
    print()

    pages_meta = []
    for page_num in range(total_pages):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        img_name = f"page_{page_num + 1:04d}.png"
        img_path = output_path / img_name

        # 保存为 PNG (无损，确保数学公式清晰)
        pix.save(str(img_path))

        img_size = img_path.stat().st_size
        pages_meta.append({
            "num": page_num + 1,
            "img": img_name,
            "width": pix.width,
            "height": pix.height,
            "size": img_size,
        })

        if (page_num + 1) % 50 == 0 or page_num == total_pages - 1:
            total_mb = sum(p["size"] for p in pages_meta) / (1024 * 1024)
            print(f"  进度: {page_num + 1}/{total_pages} ({100*(page_num+1)/total_pages:.0f}%), 已生成 {total_mb:.1f}MB")

    doc.close()

    # 写入元数据
    meta_path = output_path / "pages.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(pages_meta, f, ensure_ascii=False, indent=2)

    # 生成 HTML 查看器
    html_path = output_path / "viewer.html"
    generate_viewer_html(html_path, total_pages)

    total_mb = sum(p["size"] for p in pages_meta) / (1024 * 1024)
    print(f"\n转换完成!")
    print(f"  页数: {total_pages}")
    print(f"  图片总大小: {total_mb:.1f}MB")
    print(f"  平均每页: {total_mb/total_pages:.2f}MB")
    print(f"  查看器: {html_path}")

    return pages_meta


def generate_viewer_html(html_path: Path, total_pages: int):
    """生成自包含的 HTML 文档查看器"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<base href="pages/">
<title>高考数学试题查看器</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;background:#1a1a2e;color:#e0e0e0;overflow:hidden;height:100vh;display:flex}}
.sidebar{{width:220px;background:#12122a;display:flex;flex-direction:column;flex-shrink:0;border-right:1px solid #2a2a4a}}
.sidebar-header{{padding:14px 16px;border-bottom:1px solid #2a2a4a}}
.sidebar-header h1{{font-size:15px;font-weight:600;font-family:'Songti SC','STSong','SimSun',serif}}
.sidebar-header p{{font-size:10px;color:#888;margin-top:3px}}
.page-jump{{padding:10px 16px;border-bottom:1px solid #2a2a4a;display:flex;gap:6px}}
.page-jump input{{flex:1;background:#1a1a2e;border:1px solid #3a3a5a;color:#e0e0e0;padding:5px 8px;border-radius:4px;font-size:12px;outline:none;min-width:0}}
.page-jump input:focus{{border-color:#8b4513}}
.page-jump button{{background:#8b4513;color:#fff;border:0;padding:5px 12px;border-radius:4px;cursor:pointer;font-size:12px;white-space:nowrap;flex-shrink:0}}
.page-jump button:hover{{background:#5c2d0a}}
.info-row{{padding:6px 16px;font-size:10px;color:#666;display:flex;justify-content:space-between}}
.page-list{{flex:1;overflow-y:auto;overflow-x:hidden;padding:4px 8px;contain:strict}}
.page-list::-webkit-scrollbar{{width:3px}}
.page-list::-webkit-scrollbar-track{{background:transparent}}
.page-list::-webkit-scrollbar-thumb{{background:#3a3a5a;border-radius:2px}}
.page-item{{padding:5px 10px;border-radius:3px;cursor:pointer;font-size:12px;display:flex;align-items:center;gap:8px;transition:background .12s;margin-bottom:1px;font-variant-numeric:tabular-nums;white-space:nowrap}}
.page-item:hover{{background:#1e1e3a}}
.page-item.active{{background:#8b4513;color:#fff;font-weight:600}}
.page-num{{min-width:34px;text-align:right;font-weight:500}}
.page-range{{font-size:9px;color:#555;overflow:hidden;text-overflow:ellipsis}}
.page-item.active .page-range{{color:#d4a574}}
.main{{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}}
.toolbar{{display:flex;align-items:center;gap:8px;padding:8px 16px;background:#12122a;border-bottom:1px solid #2a2a4a;flex-shrink:0;flex-wrap:wrap}}
.toolbar button{{background:#2a2a4a;color:#ccc;border:0;padding:6px 12px;border-radius:4px;cursor:pointer;font-size:12px;transition:background .15s;white-space:nowrap}}
.toolbar button:hover{{background:#3a3a5a}}
.toolbar button:disabled{{opacity:.3;cursor:default}}
.zoom-info{{font-size:11px;color:#888;margin-left:auto}}
.viewport{{flex:1;overflow:auto;display:flex;align-items:flex-start;justify-content:center;padding:16px;background:#222240}}
.viewport::-webkit-scrollbar{{width:8px;height:8px}}
.viewport::-webkit-scrollbar-track{{background:#1a1a2e}}
.viewport::-webkit-scrollbar-thumb{{background:#4a4a6a;border-radius:4px}}
.page-img-wrapper{{transition:transform .12s;transform-origin:top center}}
.page-img-wrapper img{{display:block;max-width:none;box-shadow:0 4px 30px rgba(0,0,0,.5);border-radius:2px}}
.page-label{{text-align:center;color:#666;font-size:11px;margin-top:8px;margin-bottom:24px}}
.kb-hint{{padding:6px 16px;background:#0a0a1a;font-size:10px;color:#555;text-align:center;flex-shrink:0;border-top:1px solid #1a1a3a}}
@media(max-width:768px){{
  .sidebar{{display:none;position:fixed;z-index:100;left:0;top:0;bottom:0;width:280px}}
  .sidebar.open{{display:flex}}
}}
</style>
</head>
<body>

<div class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <h1>高考数学试题档案馆</h1>
    <p>1977—2025 真题全编</p>
  </div>
  <div class="page-jump">
    <input type="number" id="jumpInput" min="1" max="{total_pages}" placeholder="跳转页码" onkeydown="if(event.key==='Enter')jumpTo()">
    <button onclick="jumpTo()">Go</button>
  </div>
  <div class="info-row"><span>总页数</span><span id="pageCounter">{total_pages}</span></div>
  <div class="page-list" id="pageList"></div>
</div>

<div class="main">
  <div class="toolbar">
    <button onclick="prevPage()" id="btnPrev" title="上一页 (←)">◀ 上一页</button>
    <button onclick="nextPage()" id="btnNext" title="下一页 (→)">下一页 ▶</button>
    <span style="color:#444;margin:0 4px">|</span>
    <button onclick="zoomOut()" title="缩小">🔍−</button>
    <span id="zoomLabel" class="zoom-info">100%</span>
    <button onclick="zoomIn()" title="放大">🔍+</button>
    <button onclick="zoomFit()" title="适合宽度">⊡ 适合</button>
    <span style="flex:1"></span>
    <span id="pageInfo" style="font-size:12px;color:#888">第 1 / {total_pages} 页</span>
    <button onclick="toggleSidebar()" style="margin-left:8px" id="sidebarToggle">☰</button>
  </div>
  <div class="viewport" id="viewport">
    <div>
      <div class="page-img-wrapper" id="pageWrapper">
        <img id="pageImage" src="" alt="页面" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22300%22><rect fill=%22%2312122a%22 width=%22400%22 height=%22300%22/><text fill=%22%23666%22 x=%22200%22 y=%22150%22 text-anchor=%22middle%22 font-size=%2214%22>加载失败</text></svg>'">
      </div>
      <div class="page-label" id="pageLabel">第 1 / {total_pages} 页</div>
    </div>
  </div>
  <div class="kb-hint">
    ← → 翻页 &nbsp;|&nbsp; Home/End 首尾页 &nbsp;|&nbsp; +/- 缩放 &nbsp;|&nbsp; 鼠标滚轮翻页
  </div>
</div>

<script>
const TOTAL = {total_pages}
let current = 1
let zoomLevel = 1.0
const ZOOM_MIN = 0.3, ZOOM_MAX = 5.0, ZOOM_STEP = 0.25

function getSrc(n){{ return 'page_' + String(n).padStart(4,'0') + '.png' }}

function loadPage(n) {{
  current = Math.max(1, Math.min(TOTAL, n))
  var img = document.getElementById('pageImage')
  img.style.opacity = '0.3'
  img.src = getSrc(current)
  img.onload = function() {{ img.style.opacity = '1' }}
  applyZoom()
  document.getElementById('pageLabel').textContent = '第 ' + current + ' / ' + TOTAL + ' 页'
  document.getElementById('pageInfo').textContent = '第 ' + current + ' / ' + TOTAL + ' 页'
  document.getElementById('btnPrev').disabled = current <= 1
  document.getElementById('btnNext').disabled = current >= TOTAL
  updateActive()
}}

function prevPage() {{ if(current>1) loadPage(current-1) }}
function nextPage() {{ if(current<TOTAL) loadPage(current+1) }}
function jumpTo() {{
  var v = parseInt(document.getElementById('jumpInput').value)
  if(v >= 1 && v <= TOTAL) {{ loadPage(v); scrollToPage(v) }}
  document.getElementById('jumpInput').value = ''
}}

function zoomIn() {{ zoomLevel = Math.min(ZOOM_MAX, zoomLevel + ZOOM_STEP); applyZoom() }}
function zoomOut() {{ zoomLevel = Math.max(ZOOM_MIN, zoomLevel - ZOOM_STEP); applyZoom() }}
function zoomFit() {{
  var vw = document.getElementById('viewport').clientWidth - 40
  var img = document.getElementById('pageImage')
  if(img.naturalWidth) {{ zoomLevel = vw / img.naturalWidth; applyZoom() }}
}}
function applyZoom() {{
  var img = document.getElementById('pageImage')
  img.style.transform = 'scale(' + zoomLevel + ')'
  document.getElementById('zoomLabel').textContent = Math.round(zoomLevel * 100) + '%'
}}

function toggleSidebar() {{
  document.getElementById('sidebar').classList.toggle('open')
}}

// Build page list with virtual scrolling for performance
var ITEM_HEIGHT = 28
var BUFFER = 40
var pageList = document.getElementById('pageList')
var pageItems = []
var visibleRange = [0, 0]

function createPageItem(n) {{
  var div = document.createElement('div')
  div.className = 'page-item'
  div.style.position = 'absolute'
  div.style.top = ((n-1) * ITEM_HEIGHT) + 'px'
  div.style.left = '0'
  div.style.right = '0'
  div.style.height = ITEM_HEIGHT + 'px'
  div.setAttribute('data-page', n)
  div.innerHTML = '<span class="page-num">' + n + '</span>'
  div.onclick = function(){{ loadPage(n) }}
  return div
}}

function updateVisible() {{
  var st = pageList.scrollTop
  var h = pageList.clientHeight
  var start = Math.max(1, Math.floor(st / ITEM_HEIGHT) - BUFFER)
  var end = Math.min(TOTAL, Math.ceil((st + h) / ITEM_HEIGHT) + BUFFER)

  if(start === visibleRange[0] && end === visibleRange[1]) return
  visibleRange = [start, end]

  // Remove items outside range
  var children = pageList.children
  for(var i = children.length - 1; i >= 0; i--) {{
    var p = parseInt(children[i].getAttribute('data-page'))
    if(p < start || p > end) pageList.removeChild(children[i])
  }}

  // Add items in range
  var existing = {{}}
  for(var i = 0; i < pageList.children.length; i++) {{
    existing[pageList.children[i].getAttribute('data-page')] = true
  }}
  for(var n = start; n <= end; n++) {{
    if(!existing[n]) {{
      var item = createPageItem(n)
      if(n === current) item.classList.add('active')
      pageList.appendChild(item)
    }}
  }}
}}

// Set list height
pageList.style.position = 'relative'
var spacer = document.createElement('div')
spacer.style.height = (TOTAL * ITEM_HEIGHT) + 'px'
spacer.style.width = '1px'
pageList.appendChild(spacer)

// Initial render
updateVisible()
pageList.addEventListener('scroll', updateVisible)

function scrollToPage(n) {{
  pageList.scrollTop = (n - 1) * ITEM_HEIGHT - pageList.clientHeight / 2
}}

function updateActive() {{
  for(var i = 0; i < pageList.children.length; i++) {{
    var item = pageList.children[i]
    if(item.getAttribute('data-page')) {{
      item.classList.toggle('active', parseInt(item.getAttribute('data-page')) === current)
    }}
  }}
}}

// Keyboard
document.addEventListener('keydown', function(e) {{
  if(e.target.tagName === 'INPUT') return
  switch(e.key) {{
    case 'ArrowLeft': e.preventDefault(); prevPage(); break
    case 'ArrowRight': e.preventDefault(); nextPage(); break
    case 'Home': e.preventDefault(); loadPage(1); break
    case 'End': e.preventDefault(); loadPage(TOTAL); break
    case '=': case '+': e.preventDefault(); zoomIn(); break
    case '-': case '_': e.preventDefault(); zoomOut(); break
    case '0': e.preventDefault(); zoomFit(); break
  }}
}})

// Mouse wheel on viewport scrolls pages when at edges
var vp = document.getElementById('viewport')
vp.addEventListener('wheel', function(e) {{
  if(e.ctrlKey || e.metaKey) {{
    e.preventDefault()
    if(e.deltaY < 0) zoomIn()
    else zoomOut()
    return
  }}
  var atTop = vp.scrollTop <= 1
  var atBottom = vp.scrollTop + vp.clientHeight >= vp.scrollHeight - 2
  if(atTop && e.deltaY < 0) {{ e.preventDefault(); prevPage() }}
  else if(atBottom && e.deltaY > 0) {{ e.preventDefault(); nextPage() }}
}}, {{passive:false}})

loadPage(1)
</script>
</body>
</html>'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 convert_pdf.py <PDF路径> [输出目录] [DPI] [质量]")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(pdf)[0] + "_html"
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 180
    quality = int(sys.argv[4]) if len(sys.argv) > 4 else 85

    os.makedirs(out, exist_ok=True)
    convert_pdf_to_html_viewer(pdf, out, dpi, quality)
