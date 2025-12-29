from connection import get_connection
import pandas as pd
import os

class ImportService:
    # Excel, CSV ve JSON dosyalarını kontrol edip veritabanına aktarır
    
    def dosya_kontrol(self, dosya_yolu, tür):
        # Dosya formatını ve içeriğini doğrular
        try:
            uzanti = os.path.splitext(dosya_yolu)[1].lower()
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
            
            if tür == "firmalar":
                gerekli_kolonlar = ['id', 'firma_adi', 'kontenjan', 'min_ort']
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Firmalar dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                try:
                    pd.to_numeric(df['id'], errors='raise')
                    pd.to_numeric(df['kontenjan'], errors='raise')
                    pd.to_numeric(df['min_ort'], errors='raise')
                except ValueError as e:
                    return False, f"Firmalar dosyasında veri tipi hatası: {str(e)}"
                
                if (df['kontenjan'] < 0).any():
                    return False, "Kontenjan negatif olamaz!"
                if (df['min_ort'] < 0).any() or (df['min_ort'] > 4).any():
                    return False, "Minimum ortalama 0-4 arasında olmalı!"
                
            elif tür == "ogrenciler":
                gerekli_kolonlar = ['id', 'ogrenci_adi', 'ort', 'tercihler']
                for kolon in gerekli_kolonlar:
                    if kolon not in df.columns:
                        return False, f"Öğrenciler dosyasında '{kolon}' kolonu eksik!\nGerekli kolonlar: {', '.join(gerekli_kolonlar)}"
                
                for kolon in gerekli_kolonlar:
                    if df[kolon].isnull().any():
                        return False, f"'{kolon}' kolonunda boş değerler var!"
                
                try:
                    pd.to_numeric(df['id'], errors='raise')
                    pd.to_numeric(df['ort'], errors='raise')
                except ValueError as e:
                    return False, f"Öğrenciler dosyasında veri tipi hatası: {str(e)}"
                
                if (df['ort'] < 0).any() or (df['ort'] > 4).any():
                    return False, "Öğrenci ortalaması 0-4 arasında olmalı!"
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
                        if any(tercih <= 0 for tercih in tercih_listesi):
                            return False, f"Satır {index+2}'de geçersiz tercih ID'si (pozitif sayı olmalı)!"
                    except ValueError:
                        return False, f"Satır {index+2}'de tercihler formatı yanlış! Virgülle ayrılmış sayılar olmalı (örn: 1,2,3)"
                
                if df['id'].duplicated().any():
                    return False, "Öğrenci ID'lerinde tekrar var!"
            if df['id'].duplicated().any():
                return False, f"{tür.capitalize()} ID'lerinde tekrar var!"
                
            return True, f"Dosya başarıyla kontrol edildi. {len(df)} kayıt bulundu."
            
        except Exception as e:
            return False, f"Dosya okuma hatası: {str(e)}"
    
    def validate_firma_references(self, ogrenci_df, firma_df):
        firma_ids = set(firma_df['id'].tolist())
        
        for index, tercihler in ogrenci_df['tercihler'].items():
            tercih_listesi = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
            for tercih_id in tercih_listesi:
                if tercih_id not in firma_ids:
                    return False, f"Satır {index+2}'de geçersiz firma ID: {tercih_id} (Böyle bir firma yok!)"
        
        return True, "Tüm firma referansları geçerli."
    
    def import_data(self, dosya_yolu, tür):
        # Dosyayı kontrol edip veritabanına kaydeder
        basarili, mesaj = self.dosya_kontrol(dosya_yolu, tür)
        if not basarili:
            raise ValueError(mesaj)
        
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
        
        if tür == 'firmalar':
            df['kalan_kontenjan'] = df['kontenjan']
        elif tür == 'ogrenciler':
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