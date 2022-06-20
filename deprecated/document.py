class HttpClient:
    def get(self, url: str):
        import http.client
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", "/")
        r1 = conn.getresponse()
        assert r1.status == 200
        assert r1.reason == "OK"
        html = r1.read() # This will return entire content.
        return html

class Documnet:
    def __init__(self, html: str):
        self.html = html

class DocumnetFactory:
    def __init__(self, client: HttpClient):
        self.client = client

    def build(self, url: str):
        return Documnet(self.client.get(url))

class Printer:
    def print(self, doc: Documnet):
        return f"document html: {doc.html}"
