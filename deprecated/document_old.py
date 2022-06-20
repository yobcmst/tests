class HttpClient:
    def get(self, url: str="www.python.org"):
        import http.client
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", "/")
        r1 = conn.getresponse()
        assert r1.status == 200
        assert r1.reason == "OK"
        html = r1.read() # This will return entire content.
        return html

class Document:
    def __init__(self, url: str):
        self.client = HttpClient()
        self.html = self.client.get(url)

    def get_html(self):
        return self.html

    def get_client(self):
        return self.client # why we need client inside Document ????

class DocumentFactory:
    def build(self, url: str):
        return Document(url)


class Printer:
    def print(self, doc: Document):
        return doc.html
