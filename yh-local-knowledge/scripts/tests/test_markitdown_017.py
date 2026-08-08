from __future__ import annotations

import importlib.metadata
import tempfile
import unittest
import zipfile
from pathlib import Path


def make_docx(path: Path, *, omml: bool) -> None:
    math = '''<m:oMathPara><m:oMath><m:r><m:t>x</m:t></m:r><m:r><m:t>+</m:t></m:r><m:r><m:t>y</m:t></m:r><m:r><m:t>=</m:t></m:r><m:r><m:t>z</m:t></m:r></m:oMath></m:oMathPara>''' if omml else ""
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><w:body>
<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Formula Regression</w:t></w:r></w:p>
<w:p><w:r><w:t>Body paragraph survives conversion.</w:t></w:r></w:p>
<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Metric</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Value</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:p><w:r><w:t>Area</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>42</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
{math}<w:sectPr/></w:body></w:document>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    styles = '''<?xml version="1.0" encoding="UTF-8"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:qFormat/></w:style></w:styles>'''
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)
        archive.writestr("word/_rels/document.xml.rels", doc_rels)


@unittest.skipUnless(importlib.metadata.version("markitdown") == "0.1.7", "requires isolated MarkItDown 0.1.7")
class MarkItDown017RegressionTests(unittest.TestCase):
    def convert(self, omml: bool) -> str:
        from markitdown import MarkItDown
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ("omml.docx" if omml else "plain.docx")
            make_docx(path, omml=omml)
            result = MarkItDown().convert_local(str(path))
            return result.text_content

    def test_plain_docx_heading_table_body(self):
        text = self.convert(False)
        for value in ("Formula Regression", "Body paragraph", "Metric", "Value", "Area", "42"):
            self.assertIn(value, text)

    def test_omml_formula_heading_table_body(self):
        text = self.convert(True)
        for value in ("Formula Regression", "Body paragraph", "Metric", "Value", "Area", "42", "x", "y", "z"):
            self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
