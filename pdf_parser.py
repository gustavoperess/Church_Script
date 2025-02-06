
import xml.etree.ElementTree as ET
import re
from babel.numbers import parse_decimal, NumberFormatError

xml_file = "pdf_structure.xml"
tree = ET.parse(xml_file)
root = tree.getroot()
date_pattern = re.compile(r"\d{2}/\d{2}")
saldo_pattern = re.compile(r'\bsaldo\b', re.IGNORECASE)
pix_receb_pattern = re.compile(r"PIX.*RECEB|RECEB.*PIX", re.IGNORECASE)
pix_emit_pattern = re.compile(r'\bPIX EMIT\b', re.IGNORECASE) 
depo_dinheiro_pattern = re.compile(r"\bDEP.\b", re.IGNORECASE)
comp_patern = re.compile(r"\bCOMP\b", re.IGNORECASE)
deb_pattern = re.compile(r"\b(DÉB|DEB|PGTO|DÉBITO|DB)\b", re.IGNORECASE)
currency_pattern = re.compile(r"^\d{1,3}(\.\d{3})*,\d{2}[CD]?$") 

hashMap = {}


for text_line in root.iter("LTTextLineHorizontal"):
    text = text_line.text.strip() if text_line.text else ""
    bbox = text_line.attrib.get("bbox", "").replace("[", "").replace("]", "").split(",")  
    bbox = [b.strip() for b in bbox]
    if len(text) > 1:
        if bbox[1] in hashMap:
            hashMap[bbox[1]].append(text)
        else:
            hashMap[bbox[1]] = [text]

 
for text_line in root.iter("LTTextBoxHorizontal"):
    text = text_line.text.strip() if text_line.text else ""
    bbox = text_line.attrib.get("bbox", "").replace("[", "").replace("]", "").split(",")  
    bbox = [b.strip() for b in bbox]
    if len(text) > 1:
        if bbox[1] in hashMap:
            hashMap[bbox[1]].append(text)
        else:
            hashMap[bbox[1]] = [text]
    

pix_recebidos = []
pix_emitidos = []
dep_dinheiros = []
compras = []
debitos = []

for key, value in hashMap.items():
    for k in value:
        if date_pattern.match(k):
            filtered_values = [k for k in value if not saldo_pattern.search(k)]
            if filtered_values:
                pix_recebido = [item for item in filtered_values if pix_receb_pattern.search(item)]
                pix_emitido = [item for item in filtered_values if pix_emit_pattern.search(item)]
                dep_dinheiro = [item for item in filtered_values if depo_dinheiro_pattern.search(item)]
                comp = [item for item in filtered_values if comp_patern.search(item)]
                deb = [item for item in filtered_values if deb_pattern.search(item)]
                if pix_recebido:
                    for i in filtered_values:
                        i = i.strip()  
                        i = i.rstrip("CD")
                        if currency_pattern.match(i):  
                            i = i.replace(".", "").replace(",", ".")  
                            try:
                                n = float(i) 
                                pix_recebidos.append(n)
                            except NumberFormatError:
                                pass  
                elif pix_emitido:
                    for i in filtered_values:
                        i = i.strip()  
                        i = i.rstrip("CD")
                        if currency_pattern.match(i):  
                            i = i.replace(".", "").replace(",", ".")  
                            try:
                                n = float(i) 
                                pix_emitidos.append(n)
                            except NumberFormatError:
                                pass
                elif dep_dinheiro:
                    for i in filtered_values:
                        i = i.strip()  
                        i = i.rstrip("CD")
                        if currency_pattern.match(i):  
                            i = i.replace(".", "").replace(",", ".")  
                            try:
                                n = float(i) 
                                dep_dinheiros.append(n)
                            except NumberFormatError:
                                pass
                elif comp:
                    for i in filtered_values:
                        i = i.strip()  
                        i = i.rstrip("CD")
                        if currency_pattern.match(i):  
                            i = i.replace(".", "").replace(",", ".")
                            try:
                                n = float(i) 
                                compras.append(n)
                            except NumberFormatError:
                                pass
                    
                elif deb:
                    for i in filtered_values:
                        i = i.strip()  
                        i = i.rstrip("CD")
                        if currency_pattern.match(i):  
                            i = i.replace(".", "").replace(",", ".")
                            try:
                                n = float(i) 
                                debitos.append(n)
                            except NumberFormatError:
                                pass
    



dinheiro_recebido = sum(pix_recebidos) + sum(dep_dinheiros) 
dinheiro_gastado = sum(pix_emitidos) + sum(debitos) + sum(compras)


print(f"PIX Recebidos: R$ {sum(pix_recebidos):,.2f}")
print(f"PIX Emitidos: R$ {sum(pix_emitidos):,.2f}")
print(f"Depósitos em Dinheiro: R$ {sum(dep_dinheiros):,.2f}")
print(f"Compras: R$ {sum(compras):,.2f}")
print(f"Débitos: R$ {sum(debitos):,.2f}")
print(f"Dinheiro recebido ${dinheiro_recebido}")
print(f"Dinheiro gastado ${dinheiro_gastado}")