# Ac gozlu algoritma ile öğrenci yerleştirme yapan modül

from connection import get_connection
import siniflar
from classification import Classification
import time

class Greedy:
    # Öğrencileri tercih sırasına göre yerleştirir
    def __init__(self):
       # Sınıflandırma işlemleri ve performans takibi için gerekli nesneler
       self.classification = Classification()
       self.islem_sayisi = 0
       self.calisma_suresi = 0
      
    def yerlestir(self):
        # Öğrencileri not sırasına göre tercihlerine yerleştirir
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
        firma_dct= {firma.id:firma for firma in firmalar}
        
        yerlestirilen_sayisi = 0  # Toplam yerleştirilen sayısı
        
        # Her öğrenci için yerleştirme dene
        for ogrenci in ogrenciler:
          self.islem_sayisi += 1
          # Zaten yerleştirilmişse atla
          if ogrenci.yerlesen_firma_id is not None:
              continue
          # Tercih listesi boşsa atla    
          if not ogrenci.tercihler_listesi or len(ogrenci.tercihler_listesi) == 0:
              continue
          # Tercihlerini sırayla dene
          for firma_id in ogrenci.tercihler_listesi:
            self.islem_sayisi += 1
            # Firmada yer var mı ve öğrenci koşulu sağlıyor mu kontrol et
            if firma_dct[firma_id].kalan_kontenjan>0 and ogrenci.ort>=firma_dct[firma_id].min_ort:
                # Öğrenciyi firmaya yerleştir
                ogrenci.yerlesen_firma_id=firma_id
                ogrenci.durum="Yerlestirildi"
                # Firma kontenjanını azalt
                firma_dct[firma_id].kalan_kontenjan-=1
                # Veritabanını güncelle
                cursor.execute("UPDATE ogrenciler SET yerlesen_firma_id=?, durum=? WHERE id=?",(firma_id,"Yerlestirildi",ogrenci.id))
                cursor.execute("UPDATE firmalar SET kalan_kontenjan=? WHERE id=?",(firma_dct[firma_id].kalan_kontenjan,firma_id))
                conn.commit()
                yerlestirilen_sayisi += 1
                break  # İlk uygun firmaya yerleştir, diğerlerine bakmaz
        conn.close()  # Bağlantıyı kapat
        
        # Toplam süreyi hesaplar
        self.calisma_suresi = time.time() - baslangic
        return yerlestirilen_sayisi


       
       
             
            