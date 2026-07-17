"""
gen_map4.py - 海南师范大学桂林洋校区互动地图生成器 (v4)
使用模板 + replace 代替 f-string，避免花括号转义问题。
"""
import base64, os, io
from PIL import Image

UP = r"d:\桌面\glyMAP\uploads"
OUT = r"d:\桌面\glyMAP\index.html"

# ── 图片压缩工具 ──────────────────────────────────────────
def img_b64(path, max_w=800, quality=75):
    im = Image.open(path)
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    if im.width > max_w:
        ratio = max_w / im.width
        im = im.resize((max_w, int(im.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

# ── 地图底图 ──────────────────────────────────────────────
map_path = os.path.join(UP, "image_1784172028988_ftpvylb.jpg")
map_b64 = img_b64(map_path, max_w=1200, quality=80)
print(f"地图 base64: {len(map_b64)//1024}KB")

# ── 建筑数据 (坐标来自红圈检测 + 地图分析) ────────────────
BUILDINGS = [
    {
        "id":"nanmen", "name":"南门", "x":16.7, "y":89.5,
        "photos":["南门"], "nav":"110.377,20.041",
        "desc":"校园主入口，桂林洋校区南大门。学校大型活动、开学典礼、健康跑等多在此启动，是师生出入校园的重要门户。"
    },
    {
        "id":"tushuguan", "name":"图书馆", "x":32.7, "y":52.2,
        "photos":["图书馆","图书馆2","图书馆3","图书馆4"], "nav":"110.374,20.047",
        "desc":"功能属性：校园学术核心与文献中心\\n空间规模：分南北两楼，总建筑面积约3万平方米，阅览座位1980个\\n楼层分布：一楼为自习、休闲与展览区；二三层为中外图文库与主要自习区；四楼设海南文献中心；五楼为研修区与个人自习室\\n服务配套：人脸识别入馆、插座、台灯、打印机、自助查询系统、饮水机"
    },
    {
        "id":"wenxue", "name":"文学楼", "x":46.0, "y":50,
        "photos":["文学楼"], "nav":"110.376,20.048",
        "desc":"功能属性：文学院、教育学院（教育与心理学院）等教学科研楼\\n建筑特色：塔楼式建筑，周围椰林环绕，毗邻椰林广场\\n学科概况：文学院是海南师范大学传统人文强院，承担汉语言文学、汉语国际教育等人才培养；教育学院承担教育学、心理学等师范类专业教学"
    },
    {
        "id":"yijiao", "name":"一教", "x":40.0, "y":42.8,
        "photos":["一教_AI看图"], "nav":"110.377,20.047",
        "desc":"功能属性：第一公共教学楼（历史文化学院、法学院）\\n建筑规模：6层公共教学楼，总建筑面积约14908平方米\\n环境特色：楼后有人工湖景观，与椰林广场相连，是桂林洋校区公共教学的重要场所\\n使用学院：历史文化学院、法学院等文科专业主要在此上课"
    },
    {
        "id":"waiyu", "name":"外语楼", "x":48, "y":56,
        "photos":["外语楼"], "nav":"110.378,20.049",
        "desc":"功能属性：外国语学院、经济与管理学院教学科研楼\\n学科概况：外国语学院承担英语、日语、翻译等外语类专业教学；经济与管理学院承担经济学、管理学等应用型专业教学\\n建筑特色：塔楼外墙设醒目学院标识，是桂林洋校区早期投入使用的主教学楼之一"
    },
    {
        "id":"xinxi", "name":"信息楼", "x":53, "y":35.7,
        "photos":["信息楼"], "nav":"110.379,20.046",
        "desc":"功能属性：信息科学技术学院教学楼\\n学科概况：设有计算机科学与技术系、教育技术系、电子商务系和计算机公共教学部，承担计算机、教育技术、电子商务等专业教学\\n建筑特色：学院一楼设有曾宪云报告厅，可开展各类中小型讲座和学院基础活动"
    },
    {
        "id":"huagong", "name":"化工楼", "x":53.5, "y":25.7,
        "photos":["化工楼"], "nav":"110.380,20.050",
        "desc":"功能属性：化学与化工学院教学楼\\n学科概况：海南师范大学第一批设立的学院之一，海南省基础教育化学师资培养培训基地；设有化学、应用化学和制药工程三个系\\n建筑特色：2010年建成投入使用，承担化学、应用化学、制药工程等专业的教学与实验"
    },
    {
        "id":"meishu", "name":"美术楼", "x":42.9, "y":76.8,
        "photos":["美术楼","美术楼2"], "nav":"110.376,20.043",
        "desc":"功能属性：美术学院教学楼与美术馆\\n学科概况：承担美术学、书法学、视觉传达设计、环境设计、服装与服饰设计等艺术类专业教学\\n建筑特色：位于校区西南侧，是小白车全线终点区域之一，周边艺术氛围浓厚"
    },
    {
        "id":"tiyu", "name":"体育学院", "x":23.8, "y":74.3,
        "photos":["体育学院"], "nav":"110.373,20.043",
        "desc":"功能属性：体育学院教学楼\\n学科概况：承担体育教育、运动训练、社会体育指导与管理等体育类专业教学\\n建筑特色：靠近风雨操场与体育馆，周边分布室外网球场、篮球场、排球场等运动设施"
    },
    {
        "id":"zuozhe", "name":"作者|校园频道", "x":19.8, "y":23,
        "photos":["作者","校园频道"], "nav":"110.373,20.043",
        "desc":"校园内容创作与分享空间，记录海南师范大学桂林洋校区的校园生活、风景与故事。"
    },
    {
        "id":"ershi", "name":"20栋", "x":57, "y":50,
        "photos":["20栋","20栋 (1)","20栋 (2)","20栋 (3)","20栋 (4)"], "nav":"110.377,20.046",
        "desc":"楼栋属性：四期新建学生公寓（18-22栋片区）\\n住宿规格：床位大小：1.8*0.8 全楼栋统一4人间，上床下桌，配衣柜、空调、风扇、洗衣机、独立卫生间与独立阳台\\n收费标准：住宿费1450元/学年\\n生活配套：楼下设有门禁系统，可刷脸或刷校园卡进出；每层楼配备饮水机，楼栋内设有自动贩卖机"
    },
    {
        "id":"nanmen", "name":"东二门", "x":85, "y":30,
        "photos":["东二门"], "nav":"110.377,20.041",
        "desc":"桂林洋校区主要学生出入口，新生报到推荐从此门入校，出门直达校内小吃街，日常出行、觅食十分方便。"
    },
    {
        "id":"nanmen", "name":"拼多多驿站", "x":60, "y":0,
        "photos":["拼多多驿站"], "nav":"110.377,20.041",
        "desc":"在校外非常之远，没有小电驴会非常痛苦，承接圆通、申通快递"
    },
    {
        "id":"nanmen", "name":"菜鸟驿站", "x":60, "y":7,
        "photos":["菜鸟驿站"], "nav":"110.377,20.041",
        "desc":"在校内，中通、邮政、韵达、极兔、顺丰、京东快递均在此，还算方便。"
    },
    
]

# ── 加载照片 base64 ──────────────────────────────────────
photo_b64 = {}
for b in BUILDINGS:
    for pname in b["photos"]:
        if pname in photo_b64:
            continue
        ppath = os.path.join(UP, pname + ".png")
        if not os.path.exists(ppath):
            ppath = os.path.join(UP, pname + ".jpg")
        if os.path.exists(ppath):
            photo_b64[pname] = img_b64(ppath, max_w=600, quality=70)
            print(f"  照片 {pname}: {len(photo_b64[pname])//1024}KB")
        else:
            print(f"  ! 找不到照片: {pname}")
            photo_b64[pname] = ""

# 构建照片数据 JS 对象
photo_js_items = []
for name, b64 in photo_b64.items():
    photo_js_items.append('"' + name + '":"data:image/jpeg;base64,' + b64 + '"')
photo_js = "{" + ",\n".join(photo_js_items) + "}"

# 构建建筑数据 JS 数组
bld_js_items = []
for b in BUILDINGS:
    photos_arr = ",".join('"' + p + '"' for p in b["photos"])
    desc = b.get("desc", "").replace('"', '\\"').replace('\\n', '<br>')
    bld_js_items.append(
        '{id:"' + b["id"] + '",name:"' + b["name"] + '",x:' + str(b["x"]) + ',y:' + str(b["y"]) + ','
        'photos:[' + photos_arr + '],nav:"' + b["nav"] + '",desc:"' + desc + '"}'
    )
bld_js = "[\n" + ",\n".join(bld_js_items) + "\n]"

# ── HTML 模板 (用占位符，不用 f-string) ────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>海南师范大学桂林洋校区</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#1a1a2e;font-family:"Microsoft YaHei","PingFang SC",sans-serif}

#hd{position:absolute;top:0;left:0;right:0;height:44px;background:linear-gradient(135deg,#0d7a3e,#15944a);
  display:flex;align-items:center;justify-content:center;z-index:10;
  box-shadow:0 2px 8px rgba(0,0,0,.3)}
#hd h1{color:#fff;font-size:15px;font-weight:500;letter-spacing:1px}

#map{position:absolute;top:44px;left:0;right:0;bottom:0;
  overflow:hidden;background:#e8efe8}
#mapImg{display:block;width:100%;height:100%;object-fit:contain;user-select:none;-webkit-user-drag:none}

#loading{position:absolute;top:44px;left:0;right:0;bottom:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;background:#1a1a2e;z-index:20;transition:opacity .5s}
#loading.hide{opacity:0;pointer-events:none}
.spinner{width:36px;height:36px;border:3px solid rgba(255,255,255,.2);border-top-color:#15944a;
  border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#loading p{color:rgba(255,255,255,.7);margin-top:12px;font-size:13px}

.mk{position:absolute;transform:translate(-50%,-50%);cursor:pointer;z-index:5;transition:transform .15s}
.mk:hover{transform:translate(-50%,-50%) scale(1.2);z-index:6}
.mk-dot{width:28px;height:28px;border-radius:50%;background:#e74c3c;border:2.5px solid #fff;
  box-shadow:0 2px 8px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center}
.mk-dot svg{width:14px;height:14px;fill:#fff}
.mk-label{position:absolute;top:32px;left:50%;transform:translateX(-50%);white-space:nowrap;
  background:rgba(0,0,0,.72);color:#fff;font-size:11px;padding:2px 7px;border-radius:3px;
  pointer-events:none;letter-spacing:.5px}

#overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.55);z-index:50;
  display:none;align-items:center;justify-content:center;backdrop-filter:blur(3px)}
#overlay.show{display:flex}
#popup{background:#fff;border-radius:14px;max-width:380px;width:88%;overflow:hidden;
  box-shadow:0 12px 40px rgba(0,0,0,.45);animation:popIn .25s ease}
@keyframes popIn{from{transform:scale(.9);opacity:0}to{transform:scale(1);opacity:1}}
#popImg{width:100%;max-height:240px;object-fit:cover;display:block;background:#eee}
#popBody{padding:16px 18px}
#popTitle{font-size:17px;font-weight:600;color:#222;margin-bottom:8px}
#popDesc{font-size:12px;color:#555;line-height:1.6;margin-bottom:10px;max-height:180px;overflow-y:auto}
#popNav{display:inline-block;background:#15944a;color:#fff;padding:7px 18px;border-radius:8px;
  text-decoration:none;font-size:13px;margin-top:6px;transition:background .2s}
#popNav:hover{background:#0d7a3e}
#popClose{position:absolute;top:10px;right:12px;width:28px;height:28px;border-radius:50%;
  background:rgba(0,0,0,.5);border:none;color:#fff;font-size:18px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;line-height:1}
#popClose:hover{background:rgba(0,0,0,.7)}
#popPhotos{display:flex;gap:6px;margin-top:10px;overflow-x:auto}
#popPhotos img{width:72px;height:72px;object-fit:cover;border-radius:6px;cursor:pointer;
  border:2px solid transparent;transition:border-color .2s;flex-shrink:0}
#popPhotos img:hover,#popPhotos img.active{border-color:#15944a}

#zoom{position:absolute;bottom:16px;right:16px;display:flex;flex-direction:column;gap:6px;z-index:8}
#zoom button{width:36px;height:36px;border:none;border-radius:8px;background:rgba(255,255,255,.9);
  font-size:18px;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.25);color:#333;
  display:flex;align-items:center;justify-content:center;transition:background .2s}
#zoom button:hover{background:#fff}
</style>
</head>
<body>

<div id="hd"><h1>海南师范大学 · 桂林洋校区地图</h1></div>

<div id="loading"><div class="spinner"></div><p>加载地图中…</p></div>

<div id="map">
  <img id="mapImg" src="data:image/jpeg;base64,__MAP_B64__" alt="campus map">
</div>

<div id="zoom">
  <button onclick="zoomMap(1.3)" title="放大">+</button>
  <button onclick="zoomMap(1/1.3)" title="缩小">-</button>
  <button onclick="resetMap()" title="重置">&#8635;</button>
</div>

<div id="overlay" onclick="closePopup(event)">
  <div id="popup" style="position:relative">
    <button id="popClose" onclick="closePopup()">&times;</button>
    <img id="popImg" src="" alt="">
    <div id="popBody">
      <div id="popTitle"></div>
      <div id="popDesc"></div>
      <div id="popPhotos"></div>
      <a id="popNav" href="#" target="_blank">&#128205; 高德地图导航</a>
    </div>
  </div>
</div>

<script>
var PHOTOS = __PHOTO_JS__;
var BLDS = __BLD_JS__;

var mapEl = document.getElementById("map");
var imgEl = document.getElementById("mapImg");
var scale = 1, tx = 0, ty = 0;
var dragging = false, startX, startY, lastTx, lastTy;
var markersReady = false;
var markerEls = [];

function init() {
  if (markersReady) return;
  var cw = mapEl.clientWidth, ch = mapEl.clientHeight;
  if (!cw || !ch) return;
  markersReady = true;
  createMarkers();
  document.getElementById("loading").classList.add("hide");
}

imgEl.onload = function() { init(); };
if (imgEl.complete) init();
window.addEventListener("resize", function() {
  if (markersReady) repositionMarkers();
});
document.addEventListener("visibilitychange", function() {
  if (!document.hidden) init();
});

function createMarkers() {
  for (var i = 0; i < BLDS.length; i++) {
    var b = BLDS[i];
    var mk = document.createElement("div");
    mk.className = "mk";
    mk.setAttribute("data-idx", i);
    mk.innerHTML = '<div class="mk-dot"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg></div>'
      + '<div class="mk-label">' + b.name + '</div>';
    mk.addEventListener("click", function(e) {
      e.stopPropagation();
      openPopup(parseInt(this.getAttribute("data-idx")));
    });
    mapEl.appendChild(mk);
    markerEls.push(mk);
  }
  repositionMarkers();
}

function repositionMarkers() {
  var rect = imgEl.getBoundingClientRect();
  var mapRect = mapEl.getBoundingClientRect();
  var imgW = imgEl.naturalWidth, imgH = imgEl.naturalHeight;
  var contW = rect.width, contH = rect.height;
  var fitScale = Math.min(contW / imgW, contH / imgH);
  var dispW = imgW * fitScale, dispH = imgH * fitScale;
  var offX = rect.left - mapRect.left + (contW - dispW) / 2;
  var offY = rect.top - mapRect.top + (contH - dispH) / 2;
  for (var i = 0; i < BLDS.length; i++) {
    var b = BLDS[i];
    var px = offX + dispW * b.x / 100;
    var py = offY + dispH * b.y / 100;
    markerEls[i].style.left = px + "px";
    markerEls[i].style.top = py + "px";
  }
}

function openPopup(idx) {
  var b = BLDS[idx];
  var ov = document.getElementById("overlay");
  var pImg = document.getElementById("popImg");
  var pTitle = document.getElementById("popTitle");
  var pDesc = document.getElementById("popDesc");
  var pPhotos = document.getElementById("popPhotos");
  var pNav = document.getElementById("popNav");
  pTitle.textContent = b.name;
  pDesc.innerHTML = b.desc || "";
  pNav.href = "https://uri.amap.com/marker?position=" + b.nav + "&name=" + encodeURIComponent(b.name) + "&callnative=1";
  pPhotos.innerHTML = "";
  if (b.photos.length > 0) {
    pImg.src = PHOTOS[b.photos[0]] || "";
    for (var i = 0; i < b.photos.length; i++) {
      var thumb = document.createElement("img");
      thumb.src = PHOTOS[b.photos[i]] || "";
      thumb.setAttribute("data-key", b.photos[i]);
      if (i === 0) thumb.classList.add("active");
      thumb.addEventListener("click", function() {
        pImg.src = PHOTOS[this.getAttribute("data-key")] || "";
        var imgs = pPhotos.querySelectorAll("img");
        for (var j = 0; j < imgs.length; j++) imgs[j].classList.remove("active");
        this.classList.add("active");
      });
      pPhotos.appendChild(thumb);
    }
  } else {
    pImg.src = "";
  }
  ov.classList.add("show");
}

function closePopup(e) {
  if (e && e.target !== document.getElementById("overlay")) return;
  document.getElementById("overlay").classList.remove("show");
}

function zoomMap(factor) {
  scale *= factor;
  scale = Math.max(0.5, Math.min(3, scale));
  applyTransform();
}
function resetMap() {
  scale = 1; tx = 0; ty = 0;
  applyTransform();
}
function applyTransform() {
  imgEl.style.transform = "scale(" + scale + ") translate(" + tx + "px," + ty + "px)";
  repositionMarkers();
}

mapEl.addEventListener("mousedown", function(e) {
  dragging = true; startX = e.clientX; startY = e.clientY;
  lastTx = tx; lastTy = ty;
  mapEl.style.cursor = "grabbing";
});
document.addEventListener("mousemove", function(e) {
  if (!dragging) return;
  tx = lastTx + (e.clientX - startX) / scale;
  ty = lastTy + (e.clientY - startY) / scale;
  applyTransform();
});
document.addEventListener("mouseup", function() {
  dragging = false;
  mapEl.style.cursor = "";
});

mapEl.addEventListener("wheel", function(e) {
  e.preventDefault();
  zoomMap(e.deltaY < 0 ? 1.15 : 1/1.15);
}, {passive: false});

var touchDist = 0;
mapEl.addEventListener("touchstart", function(e) {
  if (e.touches.length === 1) {
    dragging = true;
    startX = e.touches[0].clientX; startY = e.touches[0].clientY;
    lastTx = tx; lastTy = ty;
  } else if (e.touches.length === 2) {
    dragging = false;
    var dx = e.touches[1].clientX - e.touches[0].clientX;
    var dy = e.touches[1].clientY - e.touches[0].clientY;
    touchDist = Math.sqrt(dx*dx + dy*dy);
  }
}, {passive: true});
mapEl.addEventListener("touchmove", function(e) {
  if (e.touches.length === 1 && dragging) {
    tx = lastTx + (e.touches[0].clientX - startX) / scale;
    ty = lastTy + (e.touches[0].clientY - startY) / scale;
    applyTransform();
  } else if (e.touches.length === 2) {
    var dx = e.touches[1].clientX - e.touches[0].clientX;
    var dy = e.touches[1].clientY - e.touches[0].clientY;
    var d = Math.sqrt(dx*dx + dy*dy);
    if (touchDist > 0) {
      scale *= d / touchDist;
      scale = Math.max(0.5, Math.min(3, scale));
      applyTransform();
    }
    touchDist = d;
  }
}, {passive: true});
mapEl.addEventListener("touchend", function() { dragging = false; touchDist = 0; });
</script>
</body>
</html>"""

# ── 替换占位符 ──
html = HTML_TEMPLATE
html = html.replace("__MAP_B64__", map_b64)
html = html.replace("__PHOTO_JS__", photo_js)
html = html.replace("__BLD_JS__", bld_js)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n已生成: {OUT}")
print(f"文件大小: {os.path.getsize(OUT)//1024}KB")
