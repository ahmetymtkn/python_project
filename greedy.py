
from connection import get_connection
import siniflar
from classification import Classification
import time

class Greedy:
    # Öğrencileri tercih sırasına göre yerleştirir
    def __init__(self):
       self.classification = Classification()
       self.islem_sayisi = 0
       self.calisma_suresi = 0
      
    def yerlestir(self):
        # Öğrencileri not sırasına göre tercihlerine yerleştirir
        baslangic = time.time()
        self.islem_sayisi = 0
        
        conn = get_connection()
        cursor = conn.cursor()
        ogrenciler = self.classification.get_ogrenciler()
        firmalar = self.classification.get_firmalar()
        firma_dct= {firma.id:firma for firma in firmalar}
        
        yerlestirilen_sayisi = 0
        
        for ogrenci in ogrenciler:
          self.islem_sayisi += 1
          if ogrenci.yerlesen_firma_id is not None:
              continue
          if not ogrenci.tercihler_listesi or len(ogrenci.tercihler_listesi) == 0:
              continue
          for firma_id in ogrenci.tercihler_listesi:
            self.islem_sayisi += 1
            if firma_dct[firma_id].kalan_kontenjan>0 and ogrenci.ort>=firma_dct[firma_id].min_ort:
                ogrenci.yerlesen_firma_id=firma_id
                ogrenci.durum="Yerlestirildi"
                firma_dct[firma_id].kalan_kontenjan-=1
                cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",(firma_id,"Yerlestirildi",ogrenci.id))
                cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",(firma_dct[firma_id].kalan_kontenjan,firma_id))
                conn.commit()
                yerlestirilen_sayisi += 1
                break
        conn.close()
        
        self.calisma_suresi = time.time() - baslangic
        return yerlestirilen_sayisi


       
       
             
            