#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵感库 服务器（零依赖，Python 3 标准库即可运行）

功能：
  - 托管本文件夹的静态页面（灵感库.html 等）
  - 提供录入 API：GET/POST/DELETE /api/entries
  - 录入数据自动持久化到本文件夹的 linggan-entries.json
    （原子写入：先写 .tmp 再替换，避免写入中断损坏数据）

运行：
  python3 server.py            # 默认端口 8080
  PORT=9000 python3 server.py  # 自定义端口

部署到服务器后，浏览器打开 http://<服务器IP>:8080/ 即可，
新录入的灵感会自动 POST 到本服务并写入 linggan-entries.json，
下次访问仍然存在。
"""
import json
import os
import re
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "linggan-entries.json")
PORT = int(os.environ.get("PORT", "8080"))

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}


def load_entries():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def save_entries(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, DATA_FILE)


def new_id():
    return int(time.time() * 1000)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # 静默访问日志
        pass

    def _send(self, code, obj=None, ctype="application/json; charset=utf-8"):
        if isinstance(obj, (dict, list)):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        elif isinstance(obj, str):
            body = obj.encode("utf-8")
        elif isinstance(obj, bytes):
            body = obj
        else:
            body = b""
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/entries":
            self._send(200, load_entries())
            return
        if path == "/":
            path = "/灵感库.html"
        if re.search(r"[?#]", path):
            path = path.split("?")[0].split("#")[0]
        fp = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
        if not fp.startswith(ROOT) or not os.path.isfile(fp):
            self._send(404, "404 not found", "text/plain; charset=utf-8")
            return
        ctype = CONTENT_TYPES.get(os.path.splitext(fp)[1].lower(), "application/octet-stream")
        with open(fp, "rb") as f:
            self._send(200, f.read(), ctype)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path != "/api/entries":
            self._send(404, "404 not found", "text/plain; charset=utf-8")
            return
        try:
            n = int(self.headers.get("Content-Length", 0) or 0)
            obj = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            self._send(400, {"error": "请求体不是合法 JSON"})
            return
        t = str(obj.get("t") or "").strip()
        if not t:
            self._send(400, {"error": "内容不能为空"})
            return
        c = str(obj.get("c") or "发明灵感").strip()
        g = str(obj.get("g") or "").strip() or "其他发明"
        b = obj.get("b")
        if isinstance(b, list) and b:
            batch = str(b[0]).strip() or "手动录入"
        else:
            batch = str(b or "手动录入").strip() or "手动录入"
        entry = {
            "id": new_id(),
            "t": t,
            "c": c,
            "g": g,
            "s": ["手动录入"],
            "b": [batch],
            "ts": time.strftime("%Y-%m-%d %H:%M"),
        }
        data = load_entries()
        # 去重：内容完全相同则不重复入库
        if any(d.get("t") == t for d in data):
            self._send(200, {"duplicate": True, "entry": entry})
            return
        data.insert(0, entry)
        save_entries(data)
        self._send(200, entry)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/entries":
            self._send(404, "404 not found", "text/plain; charset=utf-8")
            return
        try:
            eid = int(urllib.parse.parse_qs(parsed.query).get("id", [""])[0])
        except Exception:
            self._send(400, {"error": "缺少合法的 id 参数"})
            return
        data = load_entries()
        rest = [d for d in data if d.get("id") != eid]
        if len(rest) == len(data):
            self._send(404, {"error": "条目不存在"})
            return
        save_entries(rest)
        self._send(200, {"ok": True})


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("=" * 56)
    print("  灵感库服务器已启动")
    print(f"  本机访问: http://127.0.0.1:{PORT}/")
    print(f"  局域网访问: http://<本机IP>:{PORT}/")
    print(f"  数据文件: {DATA_FILE}")
    print("  按 Ctrl+C 停止")
    print("=" * 56)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
