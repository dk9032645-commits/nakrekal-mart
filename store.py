
import os, base64, threading, urllib.request, json as _json

def _sync_github(filepath):
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token or not os.path.exists(filepath):
        return
    repo = "dk9032645-commits/nakrekal-mart"
    fname = os.path.basename(filepath)
    url = f"https://api.github.com/repos/{repo}/contents/{fname}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "NakrekalMart"
    }
    try:
        sha = None
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as res:
                sha = _json.loads(res.read().decode()).get("sha")
        except Exception:
            pass
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        payload = {"message": f"Auto-save {fname}", "content": b64}
        if sha:
            payload["sha"] = sha
        put_req = urllib.request.Request(url, data=_json.dumps(payload).encode(), headers=headers, method="PUT")
        urllib.request.urlopen(put_req)
    except Exception as e:
        print("GitHub Sync Error:", e)

_orig_json_dump = _json.dump
def _patched_json_dump(obj, fp, *args, **kwargs):
    res = _orig_json_dump(obj, fp, *args, **kwargs)
    try:
        fp.flush()
        name = getattr(fp, "name", "")
        if any(k in name for k in ("products.json", "categories.json", "banners.json")):
            threading.Thread(target=_sync_github, args=(name,), daemon=True).start()
    except Exception:
        pass
    return res
_json.dump = _patched_json_dump

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080
DATA_FILE = "products.json"
CAT_FILE = "categories.json"
BANNER_FILE = "banners.json"
WHATSAPP_NUMBER = "919032645123"
ADMIN_PIN = "9032"

DEFAULT_CATS = [
    {"id": "All", "name": "For You", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z'/><line x1='3' y1='6' x2='21' y2='6'/><path d='M16 10a4 4 0 0 1-8 0'/></svg>", "img": ""},
    {"id": "Fashion", "name": "Fashion", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M20.38 3.46L16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z'/></svg>", "img": ""},
    {"id": "DTH & Remotes", "name": "DTH & TV", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><rect x='2' y='7' width='20' height='15' rx='2' ry='2'/><polyline points='17 2 12 7 7 2'/></svg>", "img": ""},
    {"id": "Mobile", "name": "Mobiles", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><rect x='5' y='2' width='14' height='20' rx='2' ry='2'/><line x1='12' y1='18' x2='12.01' y2='18'/></svg>", "img": ""},
    {"id": "Footwear", "name": "Footwear", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M3 18h18v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2zm1-2l2-7 4 2 3-4 4 3 3 6H4z'/></svg>", "img": ""},
    {"id": "General", "name": "More", "icon": "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><rect x='3' y='3' width='7' height='7'/><rect x='14' y='3' width='7' height='7'/><rect x='14' y='14' width='7' height='7'/><rect x='3' y='14' width='7' height='7'/></svg>", "img": ""}
]

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

if not os.path.exists(CAT_FILE):
    with open(CAT_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CATS, f, ensure_ascii=False, indent=2)

if not os.path.exists(BANNER_FILE):
    with open(BANNER_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="te">
<head>
    <meta name="google-site-verification" content="5c7j3MHN0RujpM5SKj89e1xbwogDgYVOq6lGbHtXU5A" />
    <title>Nakrekal Mart - Online Shopping Store | Free Home Delivery Nakrekal</title>
    <meta name="description" content="Nakrekal Mart online store - ESSA Banian, ESSA Underwear, and daily essentials with Free Home Delivery in Nakrekal town. Order on WhatsApp.">
    <meta name="keywords" content="Nakrekal Mart, Nakrekal online shopping, Nakrekal home delivery, ESSA banian Nakrekal">
    <title>Nakrekal Mart - Online Shopping Store | Free Home Delivery Nakrekal</title>
    <meta name="description" content="Nakrekal Mart online store - ESSA Banian, ESSA Underwear, and daily essentials with Free Home Delivery in Nakrekal town. Order on WhatsApp.">
    <meta name="keywords" content="Nakrekal Mart, Nakrekal online shopping, Nakrekal home delivery, ESSA banian Nakrekal">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nakrekal Mart - Nakrekal Free Home Delivery</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
  body { background: #f1f3f6; color: #212121; padding-bottom: 75px; }
  
  /* Header */
  .header { background: #141414; color: white; padding: 12px 15px 8px 15px; position: sticky; top: 0; z-index: 100; }
  .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .logo { font-size: 20px; font-weight: 800; display: flex; align-items: center; gap: 6px; color: #fff; }
  .badge { background: #ffe500; color: #141414; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 800; }
  .header-btns { display: flex; gap: 8px; align-items: center; }
  .admin-btn { display: none; background: #2a2a2a; color: #fff; border: 1px solid #444; padding: 5px 10px; border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: bold; }
  .add-btn { display: none; background: #ff9f00; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 13px; cursor: pointer; }
  .search-box { width: 100%; padding: 10px 14px; border-radius: 8px; border: none; font-size: 14px; outline: none; background: #fff; color: #212121; }

  /* Flipkart Sleek Dark Categories */
  .categories { display: flex; overflow-x: auto; background: #141414; color: #aaa; padding: 6px 8px 0 8px; gap: 14px; scrollbar-width: none; }
  .categories::-webkit-scrollbar { display: none; }
  .cat-item { position: relative; display: flex; flex-direction: column; align-items: center; min-width: 66px; cursor: pointer; padding: 4px 4px 8px 4px; border-bottom: 3px solid transparent; transition: 0.2s; }
  .cat-item.active { color: #ffffff; border-bottom: 3px solid #ffffff; font-weight: bold; }
  .cat-icon { height: 28px; width: 28px; display: flex; align-items: center; justify-content: center; margin-bottom: 4px; }
  .cat-img { width: 28px; height: 28px; object-fit: cover; border-radius: 50%; margin-bottom: 4px; border: 1px solid #555; }
  .cat-name { font-size: 11px; text-align: center; white-space: nowrap; }
  .cat-del { display: none; position: absolute; top: 0; left: 2px; background: #ff3f6c; color: #fff; font-size: 9px; width: 15px; height: 15px; border-radius: 50%; align-items: center; justify-content: center; }
  .cat-edit { display: none; position: absolute; top: 0; right: 2px; background: #ff9f00; color: #fff; font-size: 9px; width: 15px; height: 15px; border-radius: 50%; align-items: center; justify-content: center; }

  /* Auto Sliding Photo Banners */
  .slider-wrap { position: relative; margin: 10px; overflow: hidden; border-radius: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.15); background: #1a237e; }
  .slides { display: flex; transition: transform 0.5s ease-in-out; }
  .slide { min-width: 100%; padding: 18px 16px; color: white; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #1a237e, #2874f0); }
  .slide-img { min-width: 100%; height: 155px; object-fit: cover; display: block; }
  .slide h3 { font-size: 16px; margin-bottom: 4px; color: #ffe500; }
  .slide p { font-size: 12px; opacity: 0.95; }
  .banner-edit-btn { display: none; position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.75); color: #ffe500; border: 1px solid #ffe500; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; z-index: 10; }
  .dots { position: absolute; bottom: 6px; left: 0; right: 0; display: flex; justify-content: center; gap: 5px; }
  .dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.4); }
  .dot.active { width: 16px; border-radius: 4px; background: #fff; }

  /* Product Grid */
  .section-title { padding: 8px 14px; font-size: 15px; font-weight: bold; color: #212121; display: flex; justify-content: space-between; align-items: center; }
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; padding: 0 8px; }
  .card { background: #fff; border-radius: 10px; padding: 10px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 4px rgba(0,0,0,0.08); position: relative; }
  .card img { width: 100%; height: 135px; object-fit: contain; border-radius: 6px; background: #fafafa; margin-bottom: 8px; }
  .no-img { width: 100%; height: 135px; display: flex; align-items: center; justify-content: center; background: #f0f2f5; color: #888; font-size: 32px; border-radius: 6px; margin-bottom: 8px; }
  .p-cat { font-size: 10px; color: #2874f0; font-weight: bold; text-transform: uppercase; }
  .p-name { font-size: 13px; font-weight: 600; margin: 4px 0; line-height: 1.3; min-height: 34px; color: #212121; }
  
  /* Price & Discount */
  .price-row { display: flex; align-items: baseline; gap: 6px; margin-bottom: 6px; flex-wrap: wrap; }
  .p-price { font-size: 16px; font-weight: 800; color: #212121; }
  .p-mrp { font-size: 12px; color: #878787; text-decoration: line-through; }
  .p-off { font-size: 11px; color: #388e3c; font-weight: bold; }

  /* Size Chips */
  .size-box { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }
  .size-chip { border: 1px solid #ccc; background: #fff; color: #333; font-size: 11px; padding: 3px 7px; border-radius: 4px; cursor: pointer; font-weight: 600; }
  .size-chip.selected { background: #2874f0; color: #fff; border-color: #2874f0; }

  .free-del { font-size: 11px; color: #388e3c; font-weight: bold; margin-bottom: 8px; }
  .btn-row { display: flex; gap: 5px; width: 100%; }
  .btn-cart { background: #ff9f00; color: white; border: none; padding: 8px 4px; border-radius: 5px; font-weight: bold; font-size: 12px; cursor: pointer; flex: 1; }
  .btn-buy { background: #fb641b; color: white; border: none; padding: 8px 4px; border-radius: 5px; font-weight: bold; font-size: 12px; cursor: pointer; flex: 1; }
  .btn-del { display: none; position: absolute; top: 6px; right: 6px; background: #ffebee; color: #d32f2f; border: 1px solid #ffcdd2; border-radius: 50%; width: 26px; height: 26px; font-size: 13px; font-weight: bold; cursor: pointer; }

  /* Bottom Bar */
  .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #ddd; z-index: 100; }
  .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: #555; cursor: pointer; position: relative; }
  .nav-item.active { color: #2874f0; font-weight: bold; }
  .cart-badge { position: absolute; top: -5px; right: -10px; background: #ff3f6c; color: white; font-size: 10px; padding: 2px 6px; border-radius: 10px; font-weight: bold; }

  /* Modals */
  .modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.65); z-index: 200; align-items: center; justify-content: center; padding: 15px; }
  .modal-content { background: #fff; width: 100%; max-width: 400px; border-radius: 12px; padding: 18px; max-height: 88vh; overflow-y: auto; }
  .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
  .form-group { margin-bottom: 10px; }
  .form-group label { display: block; font-size: 12px; margin-bottom: 4px; font-weight: bold; color: #444; }
  .form-group input, .form-group select { width: 100%; padding: 9px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }
  .btn-submit { background: #2874f0; color: white; border: none; padding: 11px; width: 100%; border-radius: 6px; font-weight: bold; font-size: 15px; cursor: pointer; margin-top: 8px; }
  .btn-wa { background: #25D366; color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; margin-top: 10px; }
  .cart-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; font-size: 13px; }
  .qty-ctrl { display: flex; align-items: center; gap: 8px; margin-top: 4px; }
  .qty-btn { background: #e3f2fd; color: #2874f0; border: none; width: 24px; height: 24px; border-radius: 4px; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>

  <!-- Top Header -->
  <div class="header">
    <div class="header-top">
      <div class="logo" onclick="secretTap()">🛒 Nakrekal Mart <span class="badge">NAKREKAL</span></div>
      <div class="header-btns">
        <button class="add-btn" id="topAddBtn" onclick="openModal('addModal')">+ Add Item</button>
        <button class="admin-btn" id="adminLockBtn" onclick="toggleAdmin()">🔒 Admin</button>
      </div>
    </div>
    <input type="text" class="search-box" id="searchInput" placeholder="వస్తువు పేరుతో వెతకండి... (Search items)" oninput="renderProducts()">
  </div>

  <!-- Sleek Dark Categories -->
  <div class="categories" id="catBar"></div>
  <input type="file" id="catIconInput" accept="image/*" style="display:none;" onchange="uploadCatIcon(event)">

  <!-- Auto Sliding Photo Banners -->
  <div class="slider-wrap">
    <button class="banner-edit-btn" id="bannerEditBtn" onclick="openBannerModal()">🖼️ Banners</button>
    <div class="slides" id="bannerSlides"></div>
    <div class="dots" id="bannerDots"></div>
  </div>

  <div class="section-title">
    <span id="secTitle">All Available Items</span>
    <span style="font-size:11px; color:#388e3c;">⚡ Same Day Delivery</span>
  </div>
  <div class="grid" id="productGrid"></div>

  <!-- Bottom Navigation -->
  <div class="bottom-nav">
    <div class="nav-item active" onclick="selectCat('All')">🏠<span>Home</span></div>
    <div class="nav-item" onclick="openCart()">🛒<span>My Cart</span><span class="cart-badge" id="cartCount">0</span></div>
    <div class="nav-item" onclick="window.open('https://wa.me/__WA_NUM__', '_blank')">💬<span>Help / Call</span></div>
  </div>

  <!-- Banner Manager Modal -->
  <div class="modal" id="bannerModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>ఆఫర్ బ్యానర్లు (Manage Banners)</h3>
        <span style="cursor:pointer;font-size:22px;" onclick="closeModal('bannerModal')">&times;</span>
      </div>
      <div class="form-group">
        <label>కొత్త బ్యానర్ పోస్టర్ అప్‌లోడ్ చేయండి (16:9 / Wide Photo)</label>
        <input type="file" id="newBannerImg" accept="image/*">
        <button class="btn-submit" onclick="uploadBanner()">+ Upload Banner</button>
      </div>
      <div id="bannerList" style="margin-top:12px;"></div>
    </div>
  </div>

  <!-- Add Product Modal -->
  <div class="modal" id="addModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>కొత్త ఐటమ్ యాడ్ చేయండి</h3>
        <span style="cursor:pointer;font-size:22px;" onclick="closeModal('addModal')">&times;</span>
      </div>
      <div class="form-group">
        <label>వస్తువు పేరు (Item Name)</label>
        <input type="text" id="pName" placeholder="ఉదా: ESSA UNDERWEAR">
      </div>
      <div style="display:flex; gap:8px;">
        <div class="form-group" style="flex:1;">
          <label>అమ్మే ధర (Selling Price ₹)</label>
          <input type="number" id="pPrice" placeholder="110">
        </div>
        <div class="form-group" style="flex:1;">
          <label>అసలు ధర (MRP ₹ - Optional)</label>
          <input type="number" id="pMrp" placeholder="150">
        </div>
      </div>
      <div class="form-group">
        <label>కేటగిరీ (Category)</label>
        <select id="pCat">
          <option value="Fashion">Fashion</option>
          <option value="DTH & Remotes">DTH & TV</option>
          <option value="Mobile">Mobiles</option>
          <option value="Footwear">Footwear</option>
          <option value="General">More / General</option>
        </select>
      </div>
      <div class="form-group">
        <label>సైజులు (Sizes - Optional, కామాతో రాయండి)</label>
        <input type="text" id="pSizes" placeholder="ఉదా: 80cm, 85cm, 90cm, 95cm">
      </div>
      <div class="form-group">
        <label>ఫోటో ఎంచుకోండి (Photo)</label>
        <input type="file" id="pImg" accept="image/*">
      </div>
      <button class="btn-submit" onclick="saveProduct()">Save Product</button>
    </div>
  </div>

  <!-- Cart & Checkout Modal -->
  <div class="modal" id="cartModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>మీ కార్ట్ / ఆర్డర్ (Checkout)</h3>
        <span style="cursor:pointer;font-size:22px;" onclick="closeModal('cartModal')">&times;</span>
      </div>
      <div id="cartItems"></div>
      <div style="margin-top:12px; font-weight:bold; font-size:16px; text-align:right; color:#212121;" id="cartTotal">Total: ₹0</div>
      
      <div style="margin-top:12px; border-top:1px solid #eee; padding-top:10px;">
        <div class="form-group">
          <label>మీ పేరు (Your Name)</label>
          <input type="text" id="custName" placeholder="పేరు రాయండి">
        </div>
        <div class="form-group">
          <label>ఫోన్ నంబర్ (Mobile Number)</label>
          <input type="tel" id="custPhone" placeholder="10 అంకెల మొబైల్ నంబర్">
        </div>
        <div class="form-group">
          <label>నకిరేకల్ అడ్రస్ / కాలనీ (Delivery Address)</label>
          <input type="text" id="custAddr" placeholder="ఉదా: Main Road, Near Bus Stand, Nakrekal">
        </div>
        <button class="btn-wa" onclick="orderWhatsApp()">📲 💵 Cash on Delivery (Order on WhatsApp)</button>

<div id="upi-pay-box" style="margin-top:10px;">
  <button type="button" onclick="payViaUpi()" style="width:100%;padding:13px;background:#5f259f;color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:bold;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 3px 8px rgba(95,37,159,0.3);">
    <span>🟣 Pay via PhonePe / UPI</span>
  </button>
  <div style="text-align:center;font-size:12px;color:#555;margin-top:5px;">UPI ID: <b>9032645123-4@ybl</b> (Gundu Dilip Kumar)</div>
</div>
<script>
function payViaUpi() {
  var totalEl = document.body.innerText.match(/Total:\s*₹?(\d+)/i);
  var amt = totalEl ? totalEl[1] : "";
  var upiUrl = "upi://pay?pa=9032645123-4@ybl&pn=Nakrekal%20Mart&cu=INR" + (amt ? "&am=" + amt : "");
  window.location.href = upiUrl;
}
</script>

      </div>
    </div>
  </div>

<script>
const p = new URLSearchParams(window.location.search);
if (p.get("wa")) {
    const wm = `✅ నమస్కారం ${p.get("n") || ""} గారు! మీ Nakrekal Mart ఆర్డర్ (₹${p.get("t") || ""}) కన్ఫర్మ్ అయింది. ఈరోజే నకిరేకల్ లోపల మీ అడ్రస్‌కు ఉచిత హోమ్ డెలివరీ (Free Home Delivery) పంపిస్తున్నాము. 🚚`;
    window.location.href = "https://wa.me/91" + p.get("wa") + "?text=" + encodeURIComponent(wm);
}
if (p.get("sms")) {
    const m = `Namaskaram ${p.get("n") || ""}! Mee Nakrekal Mart order (Rs.${p.get("t") || ""}) confirm ayindi. Eeroje Nakrekal lo mee address ku Free Home Delivery pampistunnamu.`;
    const smsHref = "sms:+91" + p.get("sms") + "?body=" + encodeURIComponent(m);
    document.addEventListener("DOMContentLoaded", () => {
        document.body.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;background:#111827;color:#fff;font-family:sans-serif;padding:20px;text-align:center;">
            <h2>📩 Send Confirmation SMS</h2>
            <p style="font-size:18px;color:#FACC15;">Customer: +91 ${p.get("sms")}</p>
            <p style="background:#1F2937;padding:15px;border-radius:10px;max-width:400px;">${m}</p>
            <a href="${smsHref}" onclick="setTimeout(() => { window.location.replace(window.location.pathname); }, 1500)" style="margin-top:20px;background:#16A34A;color:#fff;padding:18px 36px;border-radius:12px;font-size:20px;font-weight:bold;text-decoration:none;">✅ Open Messages & Send</a>
            <a href="index.html" style="margin-top:16px;color:#9CA3AF;font-size:15px;text-decoration:underline;">🏠 Back to Nakrekal Mart</a>
        </div>`;
    });
}

  let products = [];
  let categoriesList = [];
  let customBanners = [];
  let cart = [];
  let selectedSizes = {};
  let currentCat = 'All';
  let isAdmin = false;
  let editingCatId = '';
  let newCatName = '';
  let slideIdx = 0;
  let totalSlides = 1;

  const WA_NUM = "__WA_NUM__";
  const CORRECT_PIN = "__ADMIN_PIN__";

  let tapCount = 0;
  function secretTap() {
    tapCount++;
    if (tapCount >= 5) {
      tapCount = 0;
      document.getElementById("adminLockBtn").style.display = "inline-block";
      toggleAdmin();
    }
    setTimeout(() => { tapCount = 0; }, 3000);
  }
  function toggleAdmin() {
    if (isAdmin) {
      isAdmin = false;
      document.getElementById('adminLockBtn').innerText = '🔒 Admin';
      document.getElementById('topAddBtn').style.display = 'none';
      document.getElementById('bannerEditBtn').style.display = 'none';
      renderCategories();
      renderProducts();
      return;
    }
    const pin = prompt("Admin PIN ఎంటర్ చేయండి:");
    if (pin === CORRECT_PIN) {
      isAdmin = true;
      document.getElementById('adminLockBtn').innerText = '🔓 Exit Admin';
      document.getElementById('topAddBtn').style.display = 'inline-block';
      document.getElementById('bannerEditBtn').style.display = 'block';
      renderCategories();
      renderProducts();
    } else if (pin !== null) {
      alert("తప్పు PIN!");
    }
  }

  async function initApp() {
    try {
      const [cRes, bRes, pRes] = await Promise.all([
        fetch('/api/categories'),
        fetch('/api/banners'),
        fetch('/api/products')
      ]);
      categoriesList = await cRes.json();
      customBanners = await bRes.json();
      products = await pRes.json();
      renderCategories();
      renderBanners();
      renderProducts();
    } catch (err) {
      console.error("Load error:", err);
    }
  }

  function renderCategories() {
    const bar = document.getElementById('catBar');
    bar.innerHTML = '';
    const editStyle = isAdmin ? 'display:flex;' : 'display:none;';
    categoriesList.forEach(c => {
      const iconHtml = c.img ? `<img src="${c.img}" class="cat-img">` : `<span class="cat-icon">${c.icon}</span>`;
      const activeClass = currentCat === c.id ? 'active' : '';
      const delBtn = (c.id !== 'All') ? `<span class="cat-del" style="${editStyle}" onclick="event.stopPropagation(); deleteCategory('${c.id}')">✕</span>` : '';
      bar.innerHTML += `
        <div class="cat-item ${activeClass}" onclick="selectCat('${c.id}')">
          ${delBtn}
          <span class="cat-edit" style="${editStyle}" onclick="event.stopPropagation(); triggerCatEdit('${c.id}')">✎</span>
          ${iconHtml}
          <span class="cat-name">${c.name}</span>
        </div>
      `;
    });
    if (isAdmin) {
      bar.innerHTML += `
        <div class="cat-item" onclick="addNewCategory()">
          <span class="cat-icon" style="color:#ffe500;font-size:20px;">➕</span>
          <span class="cat-name" style="color:#ffe500;">Add Cat</span>
        </div>
      `;
    }
    const sel = document.getElementById('pCat');
    if (sel) {
      sel.innerHTML = categoriesList.filter(c => c.id !== 'All').map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    }
  }

  async function deleteCategory(catId) {
    if (!confirm("ఈ కేటగిరీ లోగో డిలీట్ చేయాలా?")) return;
    await fetch('/api/cat_del', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: catId })
    });
    if (currentCat === catId) currentCat = 'All';
    initApp();
  }

  async function addNewCategory() {
    const cname = prompt("కొత్త కేటగిరీ పేరు రాయండి (ఉదా: Innerwear):");
    if (!cname || !cname.trim()) return;
    await fetch('/api/cat_add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: cname.trim() })
    });
    initApp();
  }

  async function triggerCatEdit(catId) {
    editingCatId = catId;
    const catObj = categoriesList.find(c => c.id === catId);
    const entered = prompt("కేటగిరీ పేరు మార్చండి:", catObj ? catObj.name : "");
    if (entered === null) return;
    newCatName = entered.trim() || (catObj ? catObj.name : "");
    
    if (confirm("ఐకాన్ ఫోటో కూడా మార్చాలా? (OK = ఫోటో ఎంచుకోండి, Cancel = పేరు మాత్రమే సేవ్ అవుతుంది)")) {
      document.getElementById('catIconInput').click();
    } else {
      await fetch('/api/cat_icon', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: editingCatId, name: newCatName })
      });
      initApp();
    }
  }

  async function uploadCatIcon(e) {
    if (!e.target.files.length) return;
    const base64 = await toBase64(e.target.files[0]);
    await fetch('/api/cat_icon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: editingCatId, name: newCatName, img: base64 })
    });
    e.target.value = '';
    initApp();
  }

  function renderBanners() {
    const slidesEl = document.getElementById('bannerSlides');
    if (customBanners.length > 0) {
      totalSlides = customBanners.length;
      slidesEl.innerHTML = customBanners.map(b => `<img src="${b.img}" class="slide-img">`).join('');
    } else {
      totalSlides = 2;
      slidesEl.innerHTML = `
        <div class="slide"><div><h3>🚚 FREE HOME DELIVERY</h3><p>నకిరేకల్ టౌన్ లోపల ఏ వస్తువు అయినా ఉచిత హోమ్ డెలివరీ!</p></div><div style="font-size:34px;">🎁</div></div>
        <div class="slide" style="background:linear-gradient(135deg, #b71c1c, #f57c00);"><div><h3>🔥 SPECIAL TOWN OFFERS</h3><p>ఫ్యాషన్ & నిత్యావసర వస్తువులు తక్కువ ధరలకే!</p></div><div style="font-size:34px;">🏷️</div></div>
      `;
    }
    slideIdx = 0;
    updateDots();
  }

  function updateDots() {
    const dotsEl = document.getElementById('bannerDots');
    let html = '';
    for (let i = 0; i < totalSlides; i++) {
      html += `<span class="dot ${i === slideIdx ? 'active' : ''}"></span>`;
    }
    dotsEl.innerHTML = html;
  }

  setInterval(() => {
    if (totalSlides <= 1) return;
    slideIdx = (slideIdx + 1) % totalSlides;
    document.getElementById('bannerSlides').style.transform = `translateX(-${slideIdx * 100}%)`;
    updateDots();
  }, 3500);

  function openBannerModal() {
    const list = document.getElementById('bannerList');
    if (customBanners.length === 0) {
      list.innerHTML = '<p style="font-size:12px;color:#777;">ఇంకా బ్యానర్ ఫోటోలు అప్‌లోడ్ చేయలేదు.</p>';
    } else {
      list.innerHTML = customBanners.map(b => `
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;border:1px solid #eee;padding:5px;border-radius:6px;">
          <img src="${b.img}" style="height:45px;width:90px;object-fit:cover;border-radius:4px;">
          <button onclick="deleteBanner(${b.id})" style="background:#ffebee;color:red;border:none;padding:5px 10px;border-radius:4px;font-weight:bold;">Delete</button>
        </div>
      `).join('');
    }
    openModal('bannerModal');
  }

  async function uploadBanner() {
    const inp = document.getElementById('newBannerImg');
    if (!inp.files.length) return alert("ముందుగా ఫోటో ఎంచుకోండి!");
    const base64 = await toBase64(inp.files[0]);
    await fetch('/api/banners_add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ img: base64 })
    });
    inp.value = '';
    await initApp();
    openBannerModal();
  }

  async function deleteBanner(id) {
    await fetch('/api/banners_del', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    await initApp();
    openBannerModal();
  }

  function selectCat(cat) {
    currentCat = cat;
    renderCategories();
    const catObj = categoriesList.find(c => c.id === cat);
    document.getElementById('secTitle').innerText = cat === 'All' ? 'All Available Items' : (catObj ? catObj.name : cat);
    renderProducts();
  }

  function chooseSize(prodId, size) {
    selectedSizes[prodId] = size;
    renderProducts();
  }

  function renderProducts() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    const grid = document.getElementById('productGrid');
    grid.innerHTML = '';
    
    const filtered = products.filter(p => {
      const matchCat = currentCat === 'All' || p.category === currentCat;
      const matchSearch = p.name.toLowerCase().includes(q);
      return matchCat && matchSearch;
    });

    filtered.forEach(p => {
      const imgHtml = p.image ? `<img src="${p.image}">` : `<div class="no-img">📦</div>`;
      
      let priceHtml = `<div class="price-row"><span class="p-price">₹${p.price}</span>`;
      if (p.mrp && p.mrp > p.price) {
        const off = Math.round(((p.mrp - p.price) / p.mrp) * 100);
        priceHtml += `<span class="p-mrp">₹${p.mrp}</span><span class="p-off">${off}% off</span>`;
      }
      priceHtml += `</div>`;

      let sizeHtml = '';
      if (p.sizes && p.sizes.length > 0) {
        if (!selectedSizes[p.id]) selectedSizes[p.id] = p.sizes[0];
        sizeHtml = '<div class="size-box">' + p.sizes.map(s => 
          `<span class="size-chip ${selectedSizes[p.id] === s ? 'selected' : ''}" onclick="chooseSize(${p.id}, '${s}')">${s}</span>`
        ).join('') + '</div>';
      }

      const delStyle = isAdmin ? 'display:block;' : 'display:none;';

      grid.innerHTML += `
        <div class="card">
          <button class="btn-del" style="${delStyle}" onclick="deleteProduct(${p.id})" title="Delete">✕</button>
          ${imgHtml}
          <div class="p-cat">${p.category}</div>
          <div class="p-name">${p.name}</div>
          ${priceHtml}
          ${sizeHtml}
          <div class="free-del">✓ Free Delivery in Nakrekal</div>
          <div class="btn-row">
            <button class="btn-cart" onclick="addToCart(${p.id})">🛒 Cart</button>
            <button class="btn-buy" onclick="buyNow(${p.id})">⚡ Buy Now</button>
          </div>
        </div>
      `;
    });
  }

  function buyNow(id) {
    const prod = products.find(p => p.id === id);
    const chosenSize = (prod.sizes && prod.sizes.length > 0) ? (selectedSizes[id] || prod.sizes[0]) : '';
    const cartKey = id + '_' + chosenSize;
    const existing = cart.find(c => c.cartKey === cartKey);
    if (!existing) cart.push({ ...prod, chosenSize, cartKey, qty: 1 });
    updateCartBadge();
    openCart();
  }

  function addToCart(id) {
    const prod = products.find(p => p.id === id);
    const chosenSize = (prod.sizes && prod.sizes.length > 0) ? (selectedSizes[id] || prod.sizes[0]) : '';
    const cartKey = id + '_' + chosenSize;
    const existing = cart.find(c => c.cartKey === cartKey);
    if (existing) existing.qty += 1;
    else cart.push({ ...prod, chosenSize, cartKey, qty: 1 });
    updateCartBadge();
    alert(prod.name + (chosenSize ? ` (Size: ${chosenSize})` : '') + " కార్ట్‌లో యాడ్ అయింది!");
  }

  function updateCartBadge() {
    const count = cart.reduce((sum, item) => sum + item.qty, 0);
    document.getElementById('cartCount').innerText = count;
  }

  function openCart() {
    const container = document.getElementById('cartItems');
    container.innerHTML = '';
    let total = 0;
    if (cart.length === 0) {
      container.innerHTML = '<p style="color:#777; text-align:center; padding:15px;">మీ కార్ట్ ఖాళీగా ఉంది</p>';
    } else {
      cart.forEach((item, idx) => {
        const sub = item.price * item.qty;
        total += sub;
        const sizeLabel = item.chosenSize ? ` <span style="background:#e3f2fd;color:#2874f0;padding:1px 5px;border-radius:3px;font-size:11px;">Size: ${item.chosenSize}</span>` : '';
        container.innerHTML += `
          <div class="cart-row">
            <div>
              <b>${item.name}</b>${sizeLabel}
              <div class="qty-ctrl">
                <button class="qty-btn" onclick="changeQty(${idx}, -1)">-</button>
                <span><b>${item.qty}</b></span>
                <button class="qty-btn" onclick="changeQty(${idx}, 1)">+</button>
                <small style="color:#666;">(₹${item.price} each)</small>
              </div>
            </div>
            <div>
              <b>₹${sub}</b>
              <button onclick="removeCart(${idx})" style="margin-left:10px; color:red; border:none; background:none; font-weight:bold; cursor:pointer;">✕</button>
            </div>
          </div>
        `;
      });
    }
    document.getElementById('cartTotal').innerText = "Total: ₹" + total + " (Free Delivery)";
    openModal('cartModal');
  }

  function changeQty(idx, delta) {
    cart[idx].qty += delta;
    if (cart[idx].qty <= 0) cart.splice(idx, 1);
    updateCartBadge();
    openCart();
  }

  function removeCart(idx) {
    cart.splice(idx, 1);
    updateCartBadge();
    openCart();
  }

  function orderWhatsApp() {
    if (cart.length === 0) return alert("ముందుగా ఐటమ్స్ సెలెక్ట్ చేయండి!");
    const name = document.getElementById('custName').value.trim();
    const phone = document.getElementById('custPhone').value.trim();
    const addr = document.getElementById('custAddr').value.trim();
    if (!name || !phone || !addr) return alert("దయచేసి పేరు, ఫోన్ నంబర్ మరియు అడ్రస్ రాయండి!");
            if (phone.replace(/\D/g, "").slice(-10).length !== 10) return alert("దయచేసి సరైన 10 అంకెల మొబైల్ నంబర్ ఎంటర్ చేయండి!");

    let msg = `🛍️ *NEW ORDER - Nakrekal Mart (NAKREKAL)*\n━━━━━━━━━━━━━━━━━━\n`;
    msg += `👤 *Name:* ${name}\n📞 *Phone:* ${phone}\n📍 *Address:* ${addr}\n\n📦 *Items:*\n`;
    let total = 0;
    cart.forEach(item => {
      const sub = item.price * item.qty;
      total += sub;
      const sText = item.chosenSize ? ` [Size: ${item.chosenSize}]` : '';
      msg += `• ${item.name}${sText} (${item.qty} x ₹${item.price}) = ₹${sub}\n`;
    });
    msg += `━━━━━━━━━━━━━━━━━━\n🚚 *Delivery:* FREE\n💰 *TOTAL BILL: ₹${total}*`;

    const cPhone = phone.replace(/\D/g, "").slice(-10);
            const cReply = encodeURIComponent(`✅ నమస్కారం ${name} గారు! మీ Nakrekal Mart ఆర్డర్ (₹${total}) కన్ఫర్మ్ అయింది. ఈరోజే నకిరేకల్ లోపల మీ అడ్రస్‌కు ఉచిత హోమ్ డెలివరీ (Free Home Delivery) పంపిస్తున్నాము. 🚚`);
            const smsUrl = `https://dk9032645-commits.github.io/nakrekal-mart/?sms=${cPhone}&n=${encodeURIComponent(name)}&t=${total}`;
            msg += `\n\n👇 *WhatsApp లో కన్ఫర్మ్ చేయడానికి:*\nhttps://dk9032645-commits.github.io/nakrekal-mart/?wa=${cPhone}&n=${encodeURIComponent(name)}&t=${total}\n\n📩 *SMS (Text) పంపడానికి:*\n${smsUrl}`;
            const url = `https://wa.me/${WA_NUM}?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
  }

  async function saveProduct() {
    const name = document.getElementById('pName').value.trim();
    const price = document.getElementById('pPrice').value;
    const mrp = document.getElementById('pMrp').value;
    const category = document.getElementById('pCat').value;
    const sizesRaw = document.getElementById('pSizes').value.trim();
    const fileInput = document.getElementById('pImg');

    if (!name || !price) return alert("పేరు మరియు ధర తప్పనిసరి!");

    const sizes = sizesRaw ? sizesRaw.split(',').map(s => s.trim()).filter(s => s) : [];
    let base64Img = "";
    if (fileInput.files.length > 0) {
      base64Img = await toBase64(fileInput.files[0]);
    }

    await fetch('/api/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, price: Number(price), mrp: mrp ? Number(mrp) : 0, category, sizes, image: base64Img })
    });

    document.getElementById('pName').value = '';
    document.getElementById('pPrice').value = '';
    document.getElementById('pMrp').value = '';
    document.getElementById('pSizes').value = '';
    fileInput.value = '';
    closeModal('addModal');
    initApp();
  }

  async function deleteProduct(id) {
    if (!confirm("ఈ ఐటమ్ డిలీట్ చేయాలా?")) return;
    await fetch('/api/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    initApp();
  }

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  function openModal(id) { document.getElementById(id).style.display = 'flex'; }
  function closeModal(id) { document.getElementById(id).style.display = 'none'; }

  initApp();
</script>

<style>
#search-suggestions {
    position: absolute; top: 100%; left: 0; right: 0;
    background: #fff; border-radius: 0 0 14px 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    z-index: 9999; max-height: 280px; overflow-y: auto;
    display: none; border: 1px solid #e2e8f0; border-top: none;
}
.sug-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-bottom: 1px solid #f1f5f9;
    cursor: pointer; color: #1e293b; text-align: left;
}
.sug-item:hover, .sug-item:active { background: #f8fafc; }
.sug-item img { width: 38px; height: 38px; object-fit: cover; border-radius: 6px; }
.sug-info { flex: 1; }
.sug-name { font-weight: 600; font-size: 14px; }
.sug-price { font-size: 12px; color: #16a34a; font-weight: 700; }
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
    const inp = document.querySelector("input[placeholder*=\"Search\"], input[placeholder*=\"వస్తువు\"]");
    if (!inp) return;
    inp.parentElement.style.position = "relative";
    const box = document.createElement("div");
    box.id = "search-suggestions";
    inp.parentElement.appendChild(box);

    inp.addEventListener("input", function() {
        const q = this.value.trim().toLowerCase();
        box.innerHTML = "";
        if (!q) { box.style.display = "none"; return; }
        const cards = document.querySelectorAll(".product-card, .card, [data-name]");
        let matches = [];
        cards.forEach(c => {
            const titleEl = c.querySelector("h3, h4, .title, .product-title, b, strong") || c;
            const name = (c.getAttribute("data-name") || titleEl.innerText || "").split("\n")[0].trim();
            const imgEl = c.querySelector("img");
            const priceMatch = c.innerText.match(/₹\s*\d+/);
            if (name.toLowerCase().includes(q) && name.length > 1) {
                matches.push({ name, img: imgEl ? imgEl.src : "", price: priceMatch ? priceMatch[0] : "", card: c });
            }
        });
        if (matches.length === 0) {
            box.innerHTML = "<div class=\"sug-item\" style=\"color:#64748b\">🔍 \"" + this.value + "\" పేరుతో వస్తువు దొరకలేదు</div>";
        } else {
            matches.slice(0, 8).forEach(m => {
                const div = document.createElement("div");
                div.className = "sug-item";
                div.innerHTML = (m.img ? "<img src=\"" + m.img + "\">" : "🔍") +
                    "<div class=\"sug-info\"><div class=\"sug-name\">" + m.name + "</div>" +
                    "<div class=\"sug-price\">" + m.price + "</div></div>";
                div.onclick = () => {
                    inp.value = m.name;
                    inp.dispatchEvent(new Event("input"));
                    box.style.display = "none";
                    m.card.scrollIntoView({ behavior: "smooth", block: "center" });
                };
                box.appendChild(div);
            });
        }
        box.style.display = "block";
    });
    document.addEventListener("click", e => { if (!inp.parentElement.contains(e.target)) box.style.display = "none"; });
});
</script>

<style>
#upi-pay-bar {
    position: fixed; bottom: 62px; left: 10px; right: 10px;
    background: linear-gradient(135deg, #5f259f, #7c3aed);
    color: #fff; padding: 12px 16px; border-radius: 14px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 6px 20px rgba(95,37,159,0.35); z-index: 9998;
    font-family: sans-serif;
}
#upi-pay-btn {
    background: #fff; color: #5f259f; border: none;
    padding: 8px 14px; border-radius: 10px; font-weight: 800;
    font-size: 13px; cursor: pointer;
}
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
    const upiId = "9032645123-4@ybl";
    const payeeName = "Nakrekal Mart";

    function openPhonePe(amount, itemName) {
        const cleanAmt = parseFloat(String(amount).replace(/[^0-9.]/g, "")) || 0;
        const note = encodeURIComponent("Order: " + (itemName || "Nakrekal Mart"));
        const upiUrl = `upi://pay?pa=${upiId}&pn=${encodeURIComponent(payeeName)}&am=${cleanAmt > 0 ? cleanAmt : ""}&cu=INR&tn=${note}`;
        window.location.href = upiUrl;
    }

    // Add PhonePe button inside Checkout / Cart modal or Buy Now clicks
    document.body.addEventListener("click", function(e) {
        const btn = e.target.closest("button, a");
        if (!btn) return;
        const txt = (btn.innerText || "").toLowerCase();
        if (txt.includes("buy now") || txt.includes("checkout") || txt.includes("order")) {
            setTimeout(() => {
                const modals = document.querySelectorAll(".modal, #checkoutModal, #cartModal, [role=\"dialog\"]");
                modals.forEach(m => {
                    if (m.offsetParent !== null && !m.querySelector("#modal-upi-btn")) {
                        const totalMatch = m.innerText.match(/(?:Total|₹)\s*:?\s*₹?\s*(\d+)/i);
                        const amt = totalMatch ? totalMatch[1] : "";
                        const payBtn = document.createElement("button");
                        payBtn.id = "modal-upi-btn";
                        payBtn.type = "button";
                        payBtn.innerHTML = "💜 Pay via PhonePe / UPI " + (amt ? "(₹" + amt + ")" : "");
                        payBtn.style.cssText = "width:100%;margin-top:10px;padding:12px;background:#5f259f;color:#fff;border:none;border-radius:10px;font-weight:bold;font-size:15px;cursor:pointer;";
                        payBtn.onclick = () => openPhonePe(amt, "Nakrekal Mart Order");
                        m.appendChild(payBtn);
                    }
                });
            }, 300);
        }
    });

    // Floating quick PhonePe button above bottom nav
    const bar = document.createElement("div");
    bar.id = "upi-pay-bar";
    bar.innerHTML = `<div><div style="font-size:13px;font-weight:700;">💜 PhonePe / UPI Payment</div><div style="font-size:11px;opacity:0.9;">UPI: ${upiId}</div></div><button id="upi-pay-btn">Pay Now</button>`;
    document.body.appendChild(bar);
    document.getElementById("upi-pay-btn").onclick = () => {
        const cartBadge = document.querySelector(".badge, #cart-count, [id*=\"cart\"]");
        const amt = prompt("పేమెంట్ చేయాల్సిన మొత్తం (₹) ఎంటర్ చేయండి:", "");
        if (amt !== null) openPhonePe(amt, "Nakrekal Mart");
    };
});
</script>
</body>


</html>
"""

class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            page = HTML_TEMPLATE.replace("__WA_NUM__", WHATSAPP_NUMBER).replace("__ADMIN_PIN__", ADMIN_PIN)
            self.wfile.write(page.encode("utf-8"))
        elif self.path == "/api/products":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        elif self.path == "/api/categories":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            with open(CAT_FILE, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        elif self.path == "/api/banners":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            with open(BANNER_FILE, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        data = json.loads(body)

        if self.path == "/api/add":
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                products = json.load(f)
            new_id = max([p["id"] for p in products], default=0) + 1
            products.insert(0, {
                "id": new_id,
                "name": data["name"],
                "price": data["price"],
                "mrp": data.get("mrp", 0),
                "category": data["category"],
                "sizes": data.get("sizes", []),
                "image": data.get("image", "")
            })
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

        elif self.path == "/api/delete":
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                products = json.load(f)
            products = [p for p in products if p["id"] != data["id"]]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

        elif self.path == "/api/cat_del":
            with open(CAT_FILE, "r", encoding="utf-8") as f:
                cats = json.load(f)
            cats = [c for c in cats if c["id"] != data["id"]]
            with open(CAT_FILE, "w", encoding="utf-8") as f:
                json.dump(cats, f, ensure_ascii=False, indent=2)

        elif self.path == "/api/cat_add":
            with open(CAT_FILE, "r", encoding="utf-8") as f:
                cats = json.load(f)
            cid = data["name"]
            default_svg = "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><rect x='3' y='3' width='7' height='7'/><rect x='14' y='3' width='7' height='7'/><rect x='14' y='14' width='7' height='7'/><rect x='3' y='14' width='7' height='7'/></svg>"
            cats.append({"id": cid, "name": cid, "icon": default_svg, "img": ""})
            with open(CAT_FILE, "w", encoding="utf-8") as f:
                json.dump(cats, f, ensure_ascii=False, indent=2)

        elif self.path == "/api/cat_icon":
            with open(CAT_FILE, "r", encoding="utf-8") as f:
                cats = json.load(f)
            for c in cats:
                if c["id"] == data["id"]:
                    if "name" in data and data["name"]:
                        c["name"] = data["name"]
                    if "img" in data and data["img"]:
                        c["img"] = data["img"]
            with open(CAT_FILE, "w", encoding="utf-8") as f:
                json.dump(cats, f, ensure_ascii=False, indent=2)

        elif self.path == "/api/banners_add":
            with open(BANNER_FILE, "r", encoding="utf-8") as f:
                b_list = json.load(f)
            new_bid = max([b["id"] for b in b_list], default=0) + 1
            b_list.append({"id": new_bid, "img": data["img"]})
            with open(BANNER_FILE, "w", encoding="utf-8") as f:
                json.dump(b_list, f)

        elif self.path == "/api/banners_del":
            with open(BANNER_FILE, "r", encoding="utf-8") as f:
                b_list = json.load(f)
            b_list = [b for b in b_list if b["id"] != data["id"]]
            with open(BANNER_FILE, "w", encoding="utf-8") as f:
                json.dump(b_list, f)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

print(f"🚀 Nakrekal Mart Final Pro Running at http://localhost:{PORT}")
HTTPServer(("0.0.0.0", PORT), StoreHandler).serve_forever()

