from connection import get_connection
import classification
import random

class Simulation:
    # Yerleştirme sonrası simülasyon işlemlerini yönetir
    def __init__(self):
        self.classification = classification.Classification()

    def reject_simulation(self):
        # Her firmadan rastgele sayıda öğrenci reddeder
        conn = get_connection()
        cursor = conn.cursor()
        firmalar = self.classification.get_firmalar()
        for firma in firmalar:  
            ogrenciler = self.classification.get_firma_ogrenciler(firma.id)
            if(len(ogrenciler)==0):
                continue
            numrejects = random.randint(0,len(ogrenciler)-1)
            for _ in range(numrejects):
                r=random.randint(0,len(ogrenciler)-1)
                ogrenci = ogrenciler[r]
                ogrenciler.pop(r)
                ogrenci.yerlesen_firma_id = None
                ogrenci.durum = "Yerlesemedi"
                cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",
                               (ogrenci.yerlesen_firma_id, ogrenci.durum, ogrenci.id))
                firma.kalan_kontenjan += 1
                cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",
                               (firma.kalan_kontenjan, firma.id))
                
                conn.commit()
        conn.close()

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
                        
                            

        