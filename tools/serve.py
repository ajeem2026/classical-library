"""Serve the player locally, with /media/ mapped to your music library.

Usage: python -I serve.py <web_dir> <library_dir> [port]
Supports HTTP Range requests so seeking works (Python's built-in server does not).
"""
import http.server, os, sys, urllib.parse

web, library = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        root, rel = (library, path[len("/media/"):]) if path.startswith("/media/") else (web, path.lstrip("/"))
        full = os.path.realpath(os.path.join(root, rel))
        return full if full.startswith(root) else os.path.join(web, "404")

    def send_head(self):
        path = self.translate_path(self.path)
        rng = self.headers.get("Range")
        if not rng or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        start, _, end = rng.replace("bytes=", "").partition("-")
        start = int(start) if start else size - int(end)
        end = int(end) if end and start < size else size - 1
        if start >= size:
            self.send_error(416)
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        try:
            while remaining > 0:
                chunk = source.read(min(1 << 16, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # browser cancelled the range request while seeking

    def end_headers(self):
        # Local preview: never let the browser serve a stale module after an edit.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


print(f"Player: http://localhost:{port}  (media from {library})")
http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
