from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LAParams
import xml.etree.ElementTree as ET

pdf_file = "pdfReader2.pdf"  
xml_output = "output.xml"  

root = ET.Element("PDFContent")

# Extract content from the PDF
for page_layout in extract_pages(pdf_file, laparams=LAParams()):
  
    page_element = ET.SubElement(root, "LTPage", {
        "y0": str(page_layout.y0),
        "y1": str(page_layout.y1),
        "x0": str(page_layout.x0),
        "x1": str(page_layout.x1),
        "width": str(page_layout.width),
        "height": str(page_layout.height),
        "bbox": f"[{page_layout.x0}, {page_layout.y0}, {page_layout.x1}, {page_layout.y1}]",
        "pageid": str(page_layout.pageid)
    })
    
  
    for element in page_layout:
        if isinstance(element, LTTextBoxHorizontal):
            for text_line in element:
                if isinstance(text_line, LTTextLineHorizontal):
                    text_element = ET.SubElement(page_element, "LTTextLineHorizontal", {
                        "y0": str(text_line.y0),
                        "y1": str(text_line.y1),
                        "x0": str(text_line.x0),
                        "x1": str(text_line.x1),
                        "width": str(text_line.width),
                        "height": str(text_line.height),
                        "bbox": f"[{text_line.x0}, {text_line.y0}, {text_line.x1}, {text_line.y1}]",
                        "word_margin": str(text_line.word_margin)
                    })
                    text_element.text = text_line.get_text().strip()


tree = ET.ElementTree(root)
tree.write(xml_output, encoding="utf-8", xml_declaration=True)

print(f"PDF successfully converted to {xml_output}")


from pdfquery import PDFQuery

pdf_file = "pdfReader2.pdf"
output_xml = "pdf_structure.xml"


pdf = PDFQuery(pdf_file)
pdf.load()


pdf.tree.write(output_xml, pretty_print=True)

print(f"XML saved as {output_xml}")


