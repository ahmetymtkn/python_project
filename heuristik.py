from connection import get_connection
from classification import Classification

class Heuristik:
    def __init__(self):
        self.classification = Classification()

    def yerlestir(self):
        conn = get_connection()
        cursor = conn.cursor()
        ogrenciler = self.classification.get_ogrenciler()
        firmalar = self.classification.get_firmalar()
        firma_dct = {firma.id: firma for firma in firmalar}

        for ogrenci in ogrenciler:
           # Öğrencinin tercih ettiği firmalardaki skorlarını hesapla
            tercih_skorlari = []
            for firma_id in ogrenci.tercihler_listesi:
                firma = firma_dct[firma_id]
                if firma.kalan_kontenjan > 0 and ogrenci.ort >= firma.min_ort:
                    skor = self.skor_hesapla(ogrenci, firma)
                    tercih_skorlari.append((firma_id, skor))

           # Skorlara göre sırala (en yüksek skor = en iyi)
            tercih_skorlari.sort(key=lambda x: x[1], reverse=True)

           # En yüksek skorlu uygun firmaya yerleştir
            for firma_id, skor in tercih_skorlari:
                if firma_dct[firma_id].kalan_kontenjan > 0:
                    ogrenci.yerlesen_firma_id = firma_id
                    ogrenci.durum = "Yerlestirildi"
                    ogrenci.tercihler_listesi.remove(firma_id)
                    tercihler_str = ",".join(map(str, ogrenci.tercihler_listesi))
                    firma_dct[firma_id].kalan_kontenjan -= 1    
                    cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, tercihler=?, durum=? WHERE id=?",
                                 (firma_id, tercihler_str, "Yerlestirildi", ogrenci.id))
                    cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",
                                 (firma_dct[firma_id].kalan_kontenjan, firma_id))
                    conn.commit()
                    break
        conn.close()

    def skor_hesapla(self, ogrenci, firma):
        # Tercih sırası (1-5) 
        k = ogrenci.tercihler_listesi.index(firma.id) + 1
        # Skor = (yüksek ortalama) + (düşük tercih sırası) + (firmaya uygunluk)
        skor = ogrenci.ort * 25 + (60 - k * 10) - abs(firma.min_ort - ogrenci.ort) * 5
        return skor
        
        