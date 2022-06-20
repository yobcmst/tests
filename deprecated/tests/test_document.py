import pytest

from document import DocumnetFactory, Documnet, HttpClient, Printer

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

class FakeHttpClient:
    def get(self, url: str):
        return f"<!doctype html>"

def test_HttpClient():
    url = "www.python.org"
    http_client = HttpClient()
    html = http_client.get(url)

def test_Documnet():
    url = "www.python.org"
    http_client = HttpClient()
    html_1 = http_client.get(url)
    doc_factory = DocumnetFactory(http_client)
    doc = doc_factory.build(url)
    assert doc.html == html_1

def test_Documnet_from_fake_client():
    fake_url = ""
    http_client = FakeHttpClient()
    fake_html = http_client.get(fake_url)
    doc_factory = DocumnetFactory(http_client)
    doc = doc_factory.build(fake_url)
    assert doc.html == fake_html

def test_Printer():
    html = "hey we are going to test printer"
    fake_doc = Documnet(html)
    printer = Printer()
    print_res = printer.print(fake_doc)
    print(print_res)
    assert print_res == f"document html: {html}"