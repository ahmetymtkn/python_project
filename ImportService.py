#hazır verileri almak için modül
from connection import get_connection
import pandas as pd
import os

class ImportService:
    # Excel, CSV ve JSON dosyalarını kontrol edip veritabanına aktarır
    
    def dosya_kontrol(self, dosya_yolu, tür):
        # Dosya formatını ve içeriğini doğrular
        try:
            # Dosya uzantısını al ve küçük harfe çevir
            uzanti = os.path.splitext(dosya_yolu)[1].lower()
            # Desteklenen formatlara göre dosyayı oku
            if uzanti == ".xlsx":
                df = pd.read_excel(dosya_yolu)
            elif uzanti == ".csv":
                df = pd.read_csv(dosya_yolu)
            elif uzanti == ".json":
                df = pd.read_json(dosya_yolu)
            else:
                return False, "Desteklenmeyen dosya formati!"
            
            # Boş dosya kontrolü
            if df.empty:
                return False, "Dosya boş!"
            
            # Firmalar dosyası için gerekli kontroller
            if tür == "firmalar":
                # Zorunlu kolonları kontrol et
                gerekli_kolonlar = ['id', 'firma_adi', 'kontenjan', 'min_ort']
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Firmalar dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                # Boş değer kontrolü
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                # Sayısal değerler kontrolü
                try:
                    pd.to_numeric(df['id'], errors='raise')
                    pd.to_numeric(df['kontenjan'], errors='raise')
                    pd.to_numeric(df['min_ort'], errors='raise')
                except ValueError as e:
                    return False, f"Firmalar dosyasında veri tipi hatası: {str(e)}"
                
                # Mantıksal değer kontrolleri
                if (df['kontenjan'] < 0).any():
                    return False, "Kontenjan negatif olamaz!"
                if (df['min_ort'] < 0).any() or (df['min_ort'] > 4).any():
                    return False, "Minimum ortalama 0-4 arasında olmalı!"
            # Öğrenciler dosyası için gerekli kontroller    
            elif tür == "ogrenciler":
                # Zorunlu kolonları kontrol et
                gerekli_kolonlar = ['id', 'ogrenci_adi', 'ort', 'tercihler']
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Öğrenciler dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                # Boş değer kontrolü
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                # Sayısal değerler kontrolü
                try:
                    pd.to_numeric(df['id'], errors='raise')
                    pd.to_numeric(df['ort'], errors='raise')
                except ValueError as e:
                    return False, f"Öğrenciler dosyasında veri tipi hatası: {str(e)}"
                
                # Ortalama aralığı kontrolü
                if (df['ort'] < 0).any() or (df['ort'] > 4).any():
                    return False, "Öğrenci ortalaması 0-4 arasında olmalı!"
                
                # Tercihler format kontrolü (satır satır)
                for index, tercihler in df['tercihler'].items():
                    # Boş tercih kontrolü
                    if pd.isna(tercihler):
                        return False, f"Satır {index+2}'de tercihler boş!"
                    
                    # String olarak çevir ve boşluk kontrolü
                    tercihler_str = str(tercihler)
                    if not tercihler_str.strip():
                        return False, f"Satır {index+2}'de tercihler boş!"
                    
                    # Vergülle ayrılmış sayılar kontrolü
                    try:
                        tercih_listesi = tercihler_str.split(",")
                        # Boş elemanları temizle ve sayıya çevir
                        tercih_listesi = [int(t.strip()) for t in tercih_listesi if t.strip()]
                        # Hiç geçerli tercih yoksa hata
                        if len(tercih_listesi) == 0:
                            return False, f"Satır {index+2}'de geçerli tercih bulunamadı!"
                        # Negatif ID kontrolü
                        if any(tercih <= 0 for tercih in tercih_listesi):
                            return False, f"Satır {index+2}'de geçersiz tercih ID'si (pozitif sayı olmalı)!"
                    except ValueError:
                        return False, f"Satır {index+2}'de tercihler formatı yanlış! Virgülle ayrılmış sayılar olmalı (örn: 1,2,3)"
                
                # Öğrenci ID tekrar kontrolü
                if df['id'].duplicated().any():
                    return False, "Öğrenci ID'lerinde tekrar var!"
            
            # Genel ID tekrar kontrolü
            if df['id'].duplicated().any():
                return False, f"{tür.capitalize()} ID'lerinde tekrar var!"
                
            return True, f"Dosya başarıyla kontrol edildi. {len(df)} kayıt bulundu."
            
        except Exception as e:
            return False, f"Dosya okuma hatası: {str(e)}"
    
    def validate_firma_references(self, ogrenci_df, firma_df):
        # Öğrencilerin tercihlerindeki firma ID'lerinin var olup olmadığını kontrol eder
        # Mevcut firma ID'lerini set olarak al (hızlı arama için)
        firma_ids = set(firma_df['id'].tolist())
        
        # Her öğrencinin tercihlerini kontrol et
        for index, tercihler in ogrenci_df['tercihler'].items():
            # Tercih string'ini listeye çevir
            tercih_listesi = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
            # Her tercih ID'sinin firmalar tablosunda olup olmadığını kontrol et
            for tercih_id in tercih_listesi:
                if tercih_id not in firma_ids:
                    return False, f"Satır {index+2}'de geçersiz firma ID: {tercih_id} (Böyle bir firma yok!)"
        
        return True, "Tüm firma referansları geçerli."
    
    def import_data(self, dosya_yolu, tür):
        # Dosyayı kontrol edip veritabanına kaydeder
        # Önce dosya doğrulama yap
        basarili, mesaj = self.dosya_kontrol(dosya_yolu, tür)
        if not basarili:
            raise ValueError(mesaj)
        
        # Dosya uzantısını belirle
        uzanti = os.path.splitext(dosya_yolu)[1].lower()
        
        # Veritabanı bağlantısını aç
        conn = get_connection()
        
        # Dosyayı uygun formatıyla oku
        try:
            if uzanti == '.xlsx':
                df = pd.read_excel(dosya_yolu)
            elif uzanti == '.csv':
                df = pd.read_csv(dosya_yolu)
            elif uzanti == '.json':
                df = pd.read_json(dosya_yolu)
            else:
                raise ValueError(f"Desteklenmeyen format: {uzanti}")
        except Exception as e:
            conn.close()
            raise Exception(f"Veri okuma hatası: {e}")
        
        # Türe göre ek işlemler yap
        if tür == 'firmalar':
            # Kalan kontenjanı başlangıçta toplam kontenjana eşit yap
            df['kalan_kontenjan'] = df['kontenjan']
        elif tür == 'ogrenciler':
            # Önce firmaların var olup olmadığını kontrol et
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM firmalar")
            firma_rows = cursor.fetchall()
            
            # Eğer firmalar varsa tercih referanslarını kontrol et
            if firma_rows:  # Firmalar varsa kontrol et
                firma_df_temp = pd.DataFrame(firma_rows, columns=['id'])
                basarili, mesaj_ref = self.validate_firma_references(df, firma_df_temp)
                if not basarili:
                    conn.close()
                    raise ValueError(mesaj_ref)
            
            # Eksik kolonları ekle (yerleştirme bilgileri)
            df['yerlesen_firma_id'] = None  # Başlangıçta hiçbiri yerleşmemiş
            df['durum'] = 'Yerlesemedi'      # Varsayılan durum
        # Veritabanına kaydetme işlemi
        try:
            cursor = conn.cursor()
            # Önce mevcut verileri sil (yeni verilerle değiştir)
            cursor.execute(f"DELETE FROM {tür}")
            conn.commit()
            
            # Yeni verileri ekle
            df.to_sql(tür, conn, if_exists='append', index=False)
            conn.commit()
        except Exception as e:
            raise Exception(f"Veritabanına kaydetme hatası: {e}")
        finally:
            # Bağlantıyı mutlaka kapat
            conn.close()
        
        # Başarılı sonuç döndür
        return True, mesaj