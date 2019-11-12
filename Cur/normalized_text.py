import re
def normalize_text(text):
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    # Pad punctuation with spaces on both sides
    norm_text = norm_text.strip()
    # try find digits and DATES (new)
    norm_text = re.sub(r"\d\d\.\d\d\.\d\d\d\d", "ДАТА", norm_text)
    
    norm_text = re.sub(r"приложени[еюи]\s\d+", " ПРИЛОЖЕНИЕ", norm_text)
    
    norm_text = re.sub(r"\s[nN№]\s?\d+", " НОМЕР", norm_text)
    norm_text = re.sub(r"\s\d+(\s)?", " ЦИФРЫ ", norm_text)
    
    norm_text = re.sub(r"\w\.\w\.(\s)?\w+(\s)?", " ФИО ", norm_text)
    
    ## clearing under_ROW
    norm_text = re.sub('[_]+', 'ГОР_ЧЕРТА', norm_text)
    norm_text = re.sub('[|]+', 'ВЕР_ЧЕРТА', norm_text) 
    norm_text = re.sub('[│]+', 'ВЕР_ЧЕРТА', norm_text)
    norm_text = re.sub('│', 'ВЕР_ЧЕРТА', norm_text)
    norm_text = re.sub(r"(\<\*\>)", 'КАВЫЧ_ЗВЕЗД', norm_text)
    # clearing start numeration
    norm_text = re.sub(r"([\"«»])", "", norm_text)
    norm_text = re.sub(r"(^\d+\.\d+(\.)?(\d+\.)?\s?)", "", norm_text)
    norm_text = re.sub(r"(^\d+\)\s)", "", norm_text)
    norm_text = re.sub(r"(^\d+\.\s+)", "", norm_text)
    norm_text = re.sub(r"(^\w\)\s)", "", norm_text)
    norm_text = re.sub(r"(^\-\s?)", "", norm_text)
    
    
    
    norm_text = re.sub(r"([\.\[\]\"\,\,\%\(\)!\?;:])", "", norm_text)
    
    norm_text = re.sub('\/\s', ' ', norm_text)  
    norm_text = re.sub('\s№\s', ' ', norm_text)    
    norm_text = re.sub('\s[nN]\s', ' ', norm_text)
    #norm_text = re.sub('[_]+', '', norm_text)
    
    norm_text = re.sub('[\s+]', ' ', norm_text)
    norm_text = norm_text.strip()
    return norm_text