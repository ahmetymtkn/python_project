# Veritabanı verilerini sınıf nesnelerine dönüştüren modül
from connection import get_connection
import siniflar

class Classification:
    # Veritabanından veri çeker ve nesnelere dönüştürür
    
    def get_ogrenciler(self):
        # Tüm öğrencileri nota göre sıralı getirir
        try:
            conn = get_connection()  
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ogrenciler ORDER BY ort DESC")
            ogrenciler = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving students: {e}")
            ogrenciler = []
        finally:
            conn.close()
        return [siniflar.Ogrenciler(*row) for row in ogrenciler]

    def get_firmalar(self):
        # Tüm firmaları getirir
        try:  
            conn = get_connection()  
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM firmalar")
            firmalar = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving firms: {e}")
            firmalar = []
        finally:
            conn.close()
        return [siniflar.Firmalar(*row) for row in firmalar]
    
    def get_firma_ogrenciler(self, firma_id):
        # Belirli bir firmaya yerleşen öğrencileri getirir
        try:
            conn = get_connection() 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ogrenciler WHERE yerlesen_firma_id=?", (firma_id,)) 
            firma_ogrenciler = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving students for firm ID {firma_id}: {e}")
            firma_ogrenciler = []
        finally:
            conn.close()
        return [siniflar.Ogrenciler(*row) for row in firma_ogrenciler]