# Sezgisel algoritma ile öğrenci yerleştirme yapan modül
from connection import get_connection
from classification import Classification
import time

class Heuristik:
    # Skor hesaplayarak en uygun eşleştirmeyi yapar
    def __init__(self):
        # Sınıflandırma işlemleri ve performans takibi için gerekli nesneler
        self.classification = Classification()
        self.islem_sayisi = 0
        self.calisma_suresi = 0

    def yerlestir(self):
        # Her öğrenci için skor hesaplar ve en uygun firmaya yerleştirir
        baslangic = time.time()  # Başlangıç zamanını kaydet
        self.islem_sayisi = 0    # İşlem sayacını sıfırla
        
        # Veritabanı bağlantısını aç
        conn = get_connection()
        cursor = conn.cursor()
        
        # Öğrencileri nota göre sıralı al
        ogrenciler = self.classification.get_ogrenciler()
        # Tüm firmaları al
        firmalar = self.classification.get_firmalar()
        # Firma ID'lerine hızlı erişim için dictionary oluştur
        firma_dct = {firma.id: firma for firma in firmalar}
        
        yerlestirilen_sayisi = 0  # Toplam yerleştirilen sayısı

        # Her öğrenci için en iyi eşleşmeyi bul
        for ogrenci in ogrenciler:
            self.islem_sayisi += 1
            # Zaten yerleştirilmişse atla
            if ogrenci.yerlesen_firma_id is not None:
                continue
            # Tercih listesi boşsa atla
            if not ogrenci.tercihler_listesi or len(ogrenci.tercihler_listesi) == 0:
                continue
            
            # İlgili firmalar için skor hesapla
            tercih_skorlari = []
            for firma_id in ogrenci.tercihler_listesi:
                self.islem_sayisi += 1
                firma = firma_dct[firma_id]
                # Firma uygun mu kontrol et (yer var mı, not yeterli mi)
                if firma.kalan_kontenjan > 0 and ogrenci.ort >= firma.min_ort:
                    # Uygunluk skoru hesapla
                    skor = self.skor_hesapla(ogrenci, firma)
                    tercih_skorlari.append((firma_id, skor))

            # Skorlara göre büyükten küçüğe sırala
            tercih_skorlari.sort(key=lambda x: x[1], reverse=True)

            # En yüksek skorlu uygun firmaya yerleştir
            for firma_id, skor in tercih_skorlari:
                # Son kontrol: hala yer var mı?
                if firma_dct[firma_id].kalan_kontenjan > 0:
                    # Öğrenciyi firmaya yerleştir
                    ogrenci.yerlesen_firma_id = firma_id
                    ogrenci.durum = "Yerlestirildi"
                    # Firma kontenjanını azalt
                    firma_dct[firma_id].kalan_kontenjan -= 1    
                    # Veritabanını güncelle
                    cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",
                                 (firma_id, "Yerlestirildi", ogrenci.id))
                    cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",
                                 (firma_dct[firma_id].kalan_kontenjan, firma_id))
                    conn.commit()
                    yerlestirilen_sayisi += 1
                    break  # Yerleştirince diğer firmaları deneme
        conn.close()  # Bağlantıyı kapat
        
        # Toplam süreyi hesapla
        self.calisma_suresi = time.time() - baslangic
        return yerlestirilen_sayisi

    def skor_hesapla(self, ogrenci, firma):
        # Not, tercih sırası ve uygunluğa göre skor hesaplar
        self.islem_sayisi += 1
        # Öğrencinin bu firmayı kaçıncı sırada tercih ettiğini bul
        k = ogrenci.tercihler_listesi.index(firma.id) + 1
        # Skor formülü: (not*25) + (tercih bonusu) - (not farkı cezası)
        # Yüksek not = +25 puana kadar bonus
        # İlk tercih = 50 bonus, ikinci = 40, vs.
        # Not farkı = her 0.1 fark için -0.5 ceza
        skor = ogrenci.ort * 25 + (60 - k * 10) - abs(firma.min_ort - ogrenci.ort) * 5
        return skor
        
        