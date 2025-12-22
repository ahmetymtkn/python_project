from connection import get_connection
import sınıflar

class Classification:
    def get_ogrenciler(self):
        conn = get_connection()  
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ogrenciler ORDER BY ort DESC")
        ogrenciler = cursor.fetchall()
        conn.close()
        return [sınıflar.Ogrenciler(*row) for row in ogrenciler]

    def get_firmalar(self):  
        conn = get_connection()  
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM firmalar")
        firmalar = cursor.fetchall()
        conn.close()
        return [sınıflar.Firmalar(*row) for row in firmalar]
    
    def get_firma_ogrenciler(self, firma_id):
        conn = get_connection() 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ogrenciler WHERE yerlesen_firma_id=?", (firma_id,))
        firma_ogrenciler = cursor.fetchall()
        conn.close()
        return [sınıflar.Ogrenciler(*row) for row in firma_ogrenciler]