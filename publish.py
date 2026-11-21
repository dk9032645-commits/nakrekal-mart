import urllib.request

print("Dillu Mart పూర్తి డేటాను index.html లోకి ప్యాక్ చేస్తున్నాము...")
try:
    html = urllib.request.urlopen("http://localhost:8080").read().decode("utf-8")
    prods = urllib.request.urlopen("http://localhost:8080/api/products").read().decode("utf-8")
    cats = urllib.request.urlopen("http://localhost:8080/api/categories").read().decode("utf-8")
    bans = urllib.request.urlopen("http://localhost:8080/api/banners").read().decode("utf-8")

    patch = f"""<script>
    window._STATIC_DATA = {{
        '/api/products': {prods},
        '/api/categories': {cats},
        '/api/banners': {bans}
    }};
    const _origFetch = window.fetch;
    window.fetch = function(url, opts) {{
        if (typeof url === 'string' && window._STATIC_DATA[url]) {{
            return Promise.resolve(new Response(JSON.stringify(window._STATIC_DATA[url]), {{
                status: 200,
                headers: {{ 'Content-Type': 'application/json' }}
            }}));
        }}
        return _origFetch.apply(this, arguments);
    }};
    </script>"""

    html = html.replace("<head>", "<head>\n" + patch, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Success! పూర్తి డేటాతో index.html రెడీ అయింది.")
except Exception as e:
    print("Error:", e)
