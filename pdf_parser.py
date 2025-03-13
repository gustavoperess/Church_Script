
# import xml.etree.ElementTree as ET
# import re
# from babel.numbers import parse_decimal, NumberFormatError

# #xml_file = "old_pdf_structure.xml"
# xml_file = "pdf_structure.xml"

# tree = ET.parse(xml_file)
# root = tree.getroot()
# date_pattern = re.compile(r"\d{2}/\d{2}")
# saldo_pattern = re.compile(r'\bsaldo\b', re.IGNORECASE)
# pix_receb_pattern = re.compile(r"PIX.*RECEB|RECEB.*PIX", re.IGNORECASE)
# pix_emit_pattern = re.compile(r'\bPIX EMIT[A-Z]*\b', re.IGNORECASE)
# depo_dinheiro_pattern = re.compile(r"\bDEP.\b", re.IGNORECASE)
# comp_patern = re.compile(r'\bCOMP[A-Za-z]*\b', re.IGNORECASE)
# deb_pattern = re.compile(r"\b(DÉB|DEB|PGTO|DÉBITO|DB)\b", re.IGNORECASE)
# currency_pattern = re.compile(r"^\d{1,3}(\.\d{3})*,\d{2}[CD]?$") 

# hashMap = {}


# for text_line in root.iter("LTTextLineHorizontal"):
#     text = text_line.text.strip() if text_line.text else ""
#     bbox = text_line.attrib.get("bbox", "").replace("[", "").replace("]", "").split(",")  
#     bbox = [b.strip() for b in bbox]
#     if len(text) > 1:
#         if bbox[1] in hashMap:
#             hashMap[bbox[1]].append(text)
#         else:
#             hashMap[bbox[1]] = [text]

 
# for text_line in root.iter("LTTextBoxHorizontal"):
#     text = text_line.text.strip() if text_line.text else ""
#     bbox = text_line.attrib.get("bbox", "").replace("[", "").replace("]", "").split(",")  
#     bbox = [b.strip() for b in bbox]
#     if len(text) > 1:
#         if bbox[1] in hashMap:
#             hashMap[bbox[1]].append(text)
#         else:
#             hashMap[bbox[1]] = [text]
    

# pix_recebidos = []
# pix_emitidos = []
# dep_dinheiros = []
# compras = []
# debitos = []

# for key, value in hashMap.items():
#     for k in value:
  
#         if date_pattern.match(k):
       
#             filtered_values = [k for k in value if not saldo_pattern.search(k)]
#             # print(filtered_values)
#             if filtered_values:
#                 # print(filtered_values)
#                 pix_recebido = [item for item in filtered_values if pix_receb_pattern.search(item)]
#                 pix_emitido = [item for item in filtered_values if pix_emit_pattern.search(item)]
#                 dep_dinheiro = [item for item in filtered_values if depo_dinheiro_pattern.search(item)]
#                 comp = [item for item in filtered_values if comp_patern.search(item)]
#                 deb = [item for item in filtered_values if deb_pattern.search(item)]
#                 if pix_recebido:
                
#                     for i in filtered_values:
#                         # print(pix_recebido, i)
#                         i = i.strip()  
#                         i = i.rstrip("CD")
#                         if currency_pattern.match(i):  
#                             i = i.replace(".", "").replace(",", ".")  
#                             try:
#                                 n = float(i) 
#                                 pix_recebidos.append(n)
#                             except NumberFormatError:
#                                 pass  
#                 elif pix_emitido:
#                     for i in filtered_values:
#                         i = i.strip()  
#                         i = i.rstrip("CD")
#                         if currency_pattern.match(i):  
#                             i = i.replace(".", "").replace(",", ".")  
#                             try:
#                                 n = float(i) 
#                                 pix_emitidos.append(n)
#                             except NumberFormatError:
#                                 pass
#                 elif dep_dinheiro:
#                     for i in filtered_values:
#                         i = i.strip()  
#                         i = i.rstrip("CD")
#                         if currency_pattern.match(i):  
#                             i = i.replace(".", "").replace(",", ".")  
#                             try:
#                                 n = float(i) 
#                                 dep_dinheiros.append(n)
#                             except NumberFormatError:
#                                 pass
#                 elif comp:
#                     for i in filtered_values:
#                         i = i.strip()  
#                         i = i.rstrip("CD")
#                         if currency_pattern.match(i):  
#                             i = i.replace(".", "").replace(",", ".")
#                             print(i, comp)
#                             try:
#                                 n = float(i) 
#                                 compras.append(n)
#                             except NumberFormatError:
#                                 pass
                    
#                 elif deb:
#                     for i in filtered_values:
#                         i = i.strip()  
#                         i = i.rstrip("CD")
#                         if currency_pattern.match(i):  
#                             i = i.replace(".", "").replace(",", ".")
#                             try:
#                                 n = float(i) 
#                                 debitos.append(n)
#                             except NumberFormatError:
#                                 pass
#                 else:
#                     # print(filtered_values, key, value)
#                     pass
                  




# dinheiro_recebido = sum(pix_recebidos) + sum(dep_dinheiros) 
# dinheiro_gastado = sum(pix_emitidos) + sum(debitos) + sum(compras)


# print(f"PIX Recebidos: R$ {sum(pix_recebidos):,.2f}")
# print(f"PIX Emitidos: R$ {sum(pix_emitidos):,.2f}")
# print(f"Depósitos em Dinheiro: R$ {sum(dep_dinheiros):,.2f}")
# print(f"Compras: R$ {sum(compras):,.2f}")
# print(f"Débitos: R$ {sum(debitos):,.2f}")
# print(f"Dinheiro recebido ${dinheiro_recebido}")
# print(f"Dinheiro gastado ${dinheiro_gastado}")



import pdfplumber
import pandas as pd
import re
import locale
locale.setlocale(locale.LC_NUMERIC, "pt_BR.UTF-8") 

# Path to your PDF file
pdf_path = "pdfReader2.pdf"

def extract_transactions(pdf_path):
    pix_recebidos = 0
    pix_emitido = 0
    compra = 0
    deposito = 0
    saldo = 0
    debito = 0
    date_pattern = re.compile(r"\d{2}/\d{2}")
    saldo_pattern = re.compile(r'\bsaldo\b', re.IGNORECASE)
    pix_receb_pattern = re.compile(r"PIX.*RECEB|RECEB.*PIX", re.IGNORECASE)
    pix_emit_pattern = re.compile(r'\bPIX EMIT[A-Z]*\b', re.IGNORECASE)
    depo_dinheiro_pattern = re.compile(r"\bDEP.\b", re.IGNORECASE)
    comp_patern = re.compile(r'\bCOMP[A-Za-z]*\b', re.IGNORECASE)
    deb_pattern = re.compile(r"\b(DÉB|DEB|PGTO|DÉBITO|DB)\b", re.IGNORECASE)
    currency_pattern = re.compile(r"\d{1,3}(\.\d{3})*,\d{2}C?")
 
    
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    if date_pattern.match(line):
                        if pix_receb_pattern.search(line):
                                match = currency_pattern.search(line)
                                if match:
                                    x = (match.group())
                                    x = x.strip()
                                    i = x.rstrip("CD")
                                    n = float(locale.atof(i))
                                    pix_recebidos += n
                        elif pix_emit_pattern.search(line):
                            match = currency_pattern.search(line)
                            if match:
                                x = (match.group())
                                x = x.strip()
                                i = x.rstrip("CD")
                                n = float(locale.atof(i))
                                pix_emitido += n
                        elif comp_patern.search(line):
                            match = currency_pattern.search(line)
                            if match:
                                x = (match.group())
                                x = x.strip()
                                i = x.rstrip("CD")
                                n = float(locale.atof(i))
                                compra += n
                        elif depo_dinheiro_pattern.search(line):
                            match = currency_pattern.search(line)
                            if match:
                                x = (match.group())
                                x = x.strip()
                                i = x.rstrip("CD")
                                n = float(locale.atof(i))
                                deposito += n
                        elif saldo_pattern.search(line):
                            match = currency_pattern.search(line)
                            if match:
                                x = (match.group())
                                x = x.strip()
                                i = x.rstrip("CD")
                                n = float(locale.atof(i))
                                saldo += n
                        else:
                            print(line, "CHECK THIS TO SEE ")
                            match = currency_pattern.search(line)
                            if match:
                                x = (match.group())
                                x = x.strip()
                                i = x.rstrip("CD")
                                n = float(locale.atof(i))
                                debito += n
                        
                                    
                                  
                                    
    print(f"PIX Recebidos: R$ {round(pix_recebidos, 2):,.2f}")               
    print(f"PIX Emitidos: R$ {round(pix_emitido, 2):,.2f}")   
    print(f"Compras: R$ {round(compra, 2):,.2f}")   
    print(f"Deposito: R$ {round(deposito, 2):,.2f}")   
    print(f"Debito: R$ {round(debito, 2):,.2f}")
                   


data = extract_transactions(pdf_path)

# Create DataFrame
# df = pd.DataFrame(data, columns=["Date", "Document", "Description", "Value"])

# # Save to CSV
# df.to_csv("transactions.csv", index=False)
