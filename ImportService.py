from connection import get_connection
import pandas as pd
import os

class ImportService:
    
    def dosya_kontrol(self, dosya_yolu, tür):
        """Dosya içeriğini kontrol eder"""
        try:
            uzanti = os.path.splitext(dosya_yolu)[1].lower()
            
            # Dosyayı okuma
            if uzanti == ".xlsx":
                df = pd.read_excel(dosya_yolu)
            elif uzanti == ".csv":
                df = pd.read_csv(dosya_yolu)
            elif uzanti == ".json":
                df = pd.read_json(dosya_yolu)
            else:
                return False, "Desteklenmeyen dosya formati!"
            
            if df.empty:
                return False, "Dosya boş!"
            
            # İçerik kontrolü
            if tür == "firmalar":
                # Firmalar için zorunlu kolonlar
                gerekli_kolonlar = ['id', 'firma_adi', 'kontenjan', 'min_ort']
                
                # Kolon varlığı kontrolü
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Firmalar dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                # Boş değer kontrolü
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                # Veri tipi kontrolü
                try:
                    # id sayısal olmalı
                    pd.to_numeric(df['id'], errors='raise')
                    # kontenjan sayısal olmalı
                    pd.to_numeric(df['kontenjan'], errors='raise')
                    # min_ort sayısal olmalı
                    pd.to_numeric(df['min_ort'], errors='raise')
                except ValueError as e:
                    return False, f"Firmalar dosyasında veri tipi hatası: {str(e)}"
                
                # Negatif değer kontrolü
                if (df['kontenjan'] < 0).any():
                    return False, "Kontenjan negatif olamaz!"
                if (df['min_ort'] < 0).any() or (df['min_ort'] > 4).any():
                    return False, "Minimum ortalama 0-4 arasında olmalı!"
                
            elif tür == "ogrenciler":
                # Öğrenciler için zorunlu kolonlar
                gerekli_kolonlar = ['id', 'ogrenci_adi', 'ort', 'tercihler']
                
                # Kolon varlığı kontrolü
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Öğrenciler dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                # Boş değer kontrolü
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                # Veri tipi kontrolü
                try:
                    # id sayısal olmalı
                    pd.to_numeric(df['id'], errors='raise')
                    # ort sayısal olmalı
                    pd.to_numeric(df['ort'], errors='raise')
                except ValueError as e:
                    return False, f"Öğrenciler dosyasında veri tipi hatası: {str(e)}"
                
                # Ortalama değer kontrolü
                if (df['ort'] < 0).any() or (df['ort'] > 4).any():
                    return False, "Öğrenci ortalaması 0-4 arasında olmalı!"
                
                # Tercihler format kontrolü
                for index, tercihler in df['tercihler'].items():
                    if pd.isna(tercihler):
                        return False, f"Satır {index+2}'de tercihler boş!"
                    
                    tercihler_str = str(tercihler)
                    if not tercihler_str.strip():
                        return False, f"Satır {index+2}'de tercihler boş!"
                    
                    # Virgülle ayrılmış sayılar kontrolü
                    try:
                        tercih_listesi = tercihler_str.split(",")
                        tercih_listesi = [int(t.strip()) for t in tercih_listesi if t.strip()]
                        if len(tercih_listesi) == 0:
                            return False, f"Satır {index+2}'de geçerli tercih bulunamadı!"
                        # Negatif tercih kontrolü
                        if any(tercih <= 0 for tercih in tercih_listesi):
                            return False, f"Satır {index+2}'de geçersiz tercih ID'si (pozitif sayı olmalı)!"
                    except ValueError:
                        return False, f"Satır {index+2}'de tercihler formatı yanlış! Virgülle ayrılmış sayılar olmalı (örn: 1,2,3)"
                
                # ID tekrarı kontrolü
                if df['id'].duplicated().any():
                    return False, "Öğrenci ID'lerinde tekrar var!"
            
            # ID tekrarı kontrolü (her iki dosya için)
            if df['id'].duplicated().any():
                return False, f"{tür.capitalize()} ID'lerinde tekrar var!"
                
            return True, f"Dosya başarıyla kontrol edildi. {len(df)} kayıt bulundu."
            
        except Exception as e:
            return False, f"Dosya okuma hatası: {str(e)}"
    
    def validate_firma_references(self, ogrenci_df, firma_df):
        """Öğrenci tercihlerindeki firma ID'lerini doğrula"""
        firma_ids = set(firma_df['id'].tolist())
        
        for index, tercihler in ogrenci_df['tercihler'].items():
            tercih_listesi = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
            for tercih_id in tercih_listesi:
                if tercih_id not in firma_ids:
                    return False, f"Satır {index+2}'de geçersiz firma ID: {tercih_id} (Böyle bir firma yok!)"
        
        return True, "Tüm firma referansları geçerli."
    
    def import_data(self, dosya_yolu, tür):
        """Dosyayı kontrol edip veritabanına import eder"""
        # Önce dosya kontrolü yap
        basarili, mesaj = self.dosya_kontrol(dosya_yolu, tür)
        if not basarili:
            raise ValueError(mesaj)
        
        # Dosya formatını belirle
        uzanti = os.path.splitext(dosya_yolu)[1].lower()
        
        conn = get_connection()
        
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
        
        # Eğer firmalar tablosuysa kalan_kontenjan ekle
        if tür == 'firmalar':
            df['kalan_kontenjan'] = df['kontenjan']
        elif tür == 'ogrenciler':
            # Öğrenciler için firma ID validasyonu
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM firmalar")
            firma_rows = cursor.fetchall()
            
            if firma_rows:  # Firmalar varsa kontrol et
                firma_df_temp = pd.DataFrame(firma_rows, columns=['id'])
                basarili, mesaj_ref = self.validate_firma_references(df, firma_df_temp)
                if not basarili:
                    conn.close()
                    raise ValueError(mesaj_ref)
            
            # Eksik kolonları ekle
            df['yerlesen_firma_id'] = None
            df['durum'] = 'Yerlesemedi'
        
        # Veritabanına kaydet - Önce tabloyu temizle, sonra insert et
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tür}")
            conn.commit()
            
            df.to_sql(tür, conn, if_exists='append', index=False)
            conn.commit()
        except Exception as e:
            raise Exception(f"Veritabanına kaydetme hatası: {e}")
        finally:
            conn.close()
        
        return True, mesaj