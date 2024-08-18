# 1 sutuna ingilizce 2. sutuna turkce karsiliklarini excell dosyasinda yaz o dosya input_file olacak

import pandas as pd
import xml.etree.ElementTree as ET

def add_target_elements_from_excel(input_file_path, output_file_path):
    # Excel dosyasını oku
    df = pd.read_excel(input_file_path)
    
    # XML dosyasını aç
    tree = ET.parse(output_file_path)
    root = tree.getroot()

    # Excel dosyasındaki her bir kelime için trans-unit öğelerini kontrol et
    for _, row in df.iterrows():
        english_word = str(row[0])  # 1. sütun, İngilizce kelime
        turkish_translation = str(row[1])  # 2. sütun, Türkçe karşılık

        # Her bir "trans-unit" öğesini kontrol et
        for trans_unit in root.iter('trans-unit'):
            source_element = trans_unit.find('source')
            if source_element is not None and source_element.text == english_word:
                # İngilizce kelimeyi bulduğumuzda, karşılık gelen Türkçe karşılığı ekleyin
                target_element = trans_unit.find('target')
                if target_element is None:
                    target_element = ET.SubElement(trans_unit, 'target')
                    target_element.text = turkish_translation
                break
        else:
            # "trans-unit" içinde zaten "target" varsa atla
            continue

    # Güncellenmiş XML dosyasını kaydet
    tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

input_file_path = 'guncel2.xlsx'
output_file_path = 'messages.tr.unfinished.xlf'
add_target_elements_from_excel(input_file_path, output_file_path)
