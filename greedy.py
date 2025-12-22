
from connection import get_connection
import sınıflar
from classification import Classification

class Greedy:
    def __init__(self):
       self.classification = Classification() 
      
    def yerlestir(self):
        conn = get_connection()
        cursor = conn.cursor()
        ogrenciler = self.classification.get_ogrenciler()
        firmalar = self.classification.get_firmalar()
        firma_dct= {firma.id:firma for firma in firmalar}
        for ogrenci in ogrenciler:
          for firma_id in ogrenci.tercihler_listesi:
            if firma_dct[firma_id].kalan_kontenjan>0 and ogrenci.ort>=firma_dct[firma_id].min_ort:
                ogrenci.yerlesen_firma_id=firma_id
                ogrenci.durum="Yerlestirildi"
                ogrenci.tercihler_listesi.remove(firma_id)
                tercihler_str= ",".join(map(str,ogrenci.tercihler_listesi))
                firma_dct[firma_id].kalan_kontenjan-=1
                cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, tercihler=?, durum=? WHERE id=?",(firma_id,tercihler_str,"Yerlestirildi",ogrenci.id))
                cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",(firma_dct[firma_id].kalan_kontenjan,firma_id))
                conn.commit()
                
                break
        conn.close()


       
       
             
            