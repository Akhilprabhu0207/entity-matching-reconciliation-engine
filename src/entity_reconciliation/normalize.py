import re, unicodedata

def normalize_text(value: object) -> str:
    if value is None: return ''
    text=unicodedata.normalize('NFKD', str(value)).encode('ascii','ignore').decode().upper()
    text=re.sub(r'&',' AND ',text)
    text=re.sub(r'\b(THE|INCORPORATED|INC|CORP|CORPORATION|LTD|LIMITED|LLC|PLC|CO)\b',' ',text)
    text=re.sub(r'[^A-Z0-9]+',' ',text)
    return re.sub(r'\s+',' ',text).strip()

def normalize_id(value: object) -> str:
    if value is None: return ''
    return re.sub(r'[^A-Z0-9]','',str(value).upper())
