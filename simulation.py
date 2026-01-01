# Yerleştirme simülasyonu ve red işlemlerini yöneten modül
from connection import get_connection
import classification
import random

class Simulation:
    # Yerleştirme sonrası simülasyon işlemlerini yönetir
    def __init__(self):
        # Sınıflandırma işlemlerini yapmak için classification nesnesini oluştur
        self.classification = classification.Classification()

    def reject_simulation(self):
        # Her firmadan rastgele sayıda öğrenci reddeder ve reddedilenlerin listesini döndürür
        conn = get_connection()
        cursor = conn.cursor()
        firmalar = self.classification.get_firmalar()  # Tüm firmaları al
        reddedilenler = []  # Reddedilen öğrencilerin listesi
        
        for firma in firmalar:  
            ogrenciler = self.classification.get_firma_ogrenciler(firma.id)  # Firmadaki öğrenciler
            if(len(ogrenciler)==0):
                continue
            numrejects = random.randint(0,len(ogrenciler)-1)  # Kaç kişi reddedilecek
            for _ in range(numrejects):
                r=random.randint(0,len(ogrenciler)-1)
                ogrenci = ogrenciler[r]
                ogrenciler.pop(r)
                
                # Reddedilen öğrenciyi listeye ekle
                reddedilenler.append({
                    'id': ogrenci.id,
                    'ad': ogrenci.ogrenci_adi,
                    'firma': firma.firma_adi
                })
                
                ogrenci.yerlesen_firma_id = None
                ogrenci.durum = "Yerlesemedi"
                cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",
                               (ogrenci.yerlesen_firma_id, ogrenci.durum, ogrenci.id))
                firma.kalan_kontenjan += 1
                cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",
                               (firma.kalan_kontenjan, firma.id))
                
                conn.commit()
        conn.close()
        return reddedilenler

    def reduce_min_ort(self):
        # Tüm firmaların minimum ortalama şartını %10 düşürür
        conn = get_connection()
        cursor = conn.cursor()
        firmalar = self.classification.get_firmalar()
        for firma in firmalar:
            firma.min_ort = firma.min_ort*0.9
            cursor.execute("UPDATE firmalar SET min_ort=? WHERE id=?",
                           (firma.min_ort, firma.id))
        conn.commit()
        conn.close()
                        
                            

        