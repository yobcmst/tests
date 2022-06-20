from document_old import Document, Printer


def test_Printer():
    url = "www.python.org"
    doc = Document(url)
    assert doc.client # we need to instantiate client as object field, why ??
    # we my wire object graphs through "Factory" ??
    printer = Printer()
    print_res = printer.print(doc)
    assert print_res == doc.html
