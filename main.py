# Ana program - veritabanını sıfırlar ve GUI'yi başlatır
import os
import sys
from databaseCreater import veritabani_hazirla
from gui import Gui

def main():
    try:
        # Eski veritabanını temizle
        if os.path.exists("db.db"):
            os.remove("db.db")
            print("Eski veritabanı silindi.")
        
        # Yeni boş veritabanı oluştur
        print("Veritabanı oluşturuluyor...")
        veritabani_hazirla()
        print("Veritabanı başarıyla oluşturuldu.")
        
        # Kullanıcı arayüzünü başlat
        print("GUI başlatılıyor...")
        app = Gui()
        app.root.mainloop()
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


