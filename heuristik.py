from connection import get_connection
from classification import Classification
import time

class Heuristik:
    # Skor hesaplayarak en uygun eşleştirmeyi yapar
    def __init__(self):
        self.classification = Classification()
        self.islem_sayisi = 0
        self.calisma_suresi = 0

    def yerlestir(self):
        # Her öğrenci için skor hesaplar ve en uygun firmaya yerleştirir
        baslangic = time.time()
        self.islem_sayisi = 0
        
        conn = get_connection()
        cursor = conn.cursor()
        ogrenciler = self.classification.get_ogrenciler()
        firmalar = self.classification.get_firmalar()
        firma_dct = {firma.id: firma for firma in firmalar}
        
        yerlestirilen_sayisi = 0

        for ogrenci in ogrenciler:
            self.islem_sayisi += 1
            if ogrenci.yerlesen_firma_id is not None:
                continue
            if not ogrenci.tercihler_listesi or len(ogrenci.tercihler_listesi) == 0:
                continue
            
            tercih_skorlari = []
            for firma_id in ogrenci.tercihler_listesi:
                self.islem_sayisi += 1
                firma = firma_dct[firma_id]
                if firma.kalan_kontenjan > 0 and ogrenci.ort >= firma.min_ort:
                    skor = self.skor_hesapla(ogrenci, firma)
                    tercih_skorlari.append((firma_id, skor))

            tercih_skorlari.sort(key=lambda x: x[1], reverse=True)

            for firma_id, skor in tercih_skorlari:
                if firma_dct[firma_id].kalan_kontenjan > 0:
                    ogrenci.yerlesen_firma_id = firma_id
                    ogrenci.durum = "Yerlestirildi"
                    firma_dct[firma_id].kalan_kontenjan -= 1    
                    cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",
                                 (firma_id, "Yerlestirildi", ogrenci.id))
                    cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",
                                 (firma_dct[firma_id].kalan_kontenjan, firma_id))
                    conn.commit()
                    yerlestirilen_sayisi += 1
                    break
        conn.close()
        
        self.calisma_suresi = time.time() - baslangic
        return yerlestirilen_sayisi

    def skor_hesapla(self, ogrenci, firma):
        # Not, tercih sırası ve uygunluğa göre skor hesaplar
        self.islem_sayisi += 1
        k = ogrenci.tercihler_listesi.index(firma.id) + 1
        skor = ogrenci.ort * 25 + (60 - k * 10) - abs(firma.min_ort - ogrenci.ort) * 5
        return skor
        
        