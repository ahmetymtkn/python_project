
from connection import get_connection

def veritabani_hazirla():
    conn = get_connection()
    cursor = conn.cursor()

    # Firmalar Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firmalar (
            id INTEGER PRIMARY KEY,
            firma_adi TEXT,
            kontenjan INTEGER,
            min_ort REAL,
            kalan_kontenjan INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ogrenciler (
            id INTEGER PRIMARY KEY,
            ogrenci_adi TEXT,
            ort REAL,
            tercihler TEXT, -- Virgülle ayrılmış ID'ler: "5,12,30,8,2"
            yerlesen_firma_id INTEGER DEFAULT NULL,
            durum TEXT DEFAULT 'Yerlesemedi'
        )
    ''')

    conn.commit()
    return conn

if __name__ == "__main__":
    veritabani_hazirla()
    print("Veritabanı oluşturuldu!")