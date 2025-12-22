import tkinter as tk
from tkinter import filedialog, messagebox
import os 
import pandas as pd
from ImportService import ImportService
from simulation import Simulation

class Gui:
    def __init__(self):
        self.simulation = Simulation()
        self.import_service = ImportService()
        self.root = tk.Tk()
        self.root.title("Dosya Import Sistemi")
        self.root.geometry("600x500")
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Başlık
        title_label = tk.Label(main_frame, text="Dosya Import Sistemi", 
                             font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Firmalar butonu
        firma_buton = tk.Button(main_frame, text="Firmalar Dosyası Seç", 
                               command=lambda: self.dosya_sec("firmalar"),
                               bg="#4CAF50", fg="white", width=20, height=2)
        firma_buton.pack(pady=10)
        
        # Öğrenciler butonu
        ogrenci_buton = tk.Button(main_frame, text="Öğrenciler Dosyası Seç", 
                                 command=lambda: self.dosya_sec("ogrenciler"),
                                 bg="#2196F3", fg="white", width=20, height=2)
        ogrenci_buton.pack(pady=10)

        #simulationbutton
        simulation_buton = tk.Button(main_frame,text="Simulation Başlat",command=lambda:self.simulation_start(),bg="#FFA500",fg="white",width=20,height=2)
        simulation_buton.pack(pady=10)

        #min_ortalama arttırma
        minOrtalama_buton = tk.Button(main_frame,text="Minimum Ort Azalt",command=lambda:self.minOrtalama_increase(),bg="red",fg="white",width=20,height=2)
        minOrtalama_buton.pack(pady=10)

    def simulation_start(self):
        self.simulation.reject_simulation()
    def minOrtalama_increase(self):
        self.simulation.reduce_min_ort()
    

    def dosya_sec(self, tür):
        dosya_yolu = filedialog.askopenfilename(
            title=f"{tür.capitalize()} dosyası seçin",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"), 
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if dosya_yolu:
            uzanti = os.path.splitext(dosya_yolu)[1].lower()
            self.dosya_isle(dosya_yolu, uzanti, tür)

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
                return False, "Desteklenmeyen dosya formatı!"
            
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

    def dosya_isle(self, dosya_yolu, uzanti, tür):
        """Dosyayı kontrol eder ve işler"""
        try:
            # Önce dosya içeriğini kontrol et
            basarili, mesaj = self.dosya_kontrol(dosya_yolu, tür)
            
            if not basarili:
                messagebox.showerror("Hata", mesaj)
                return
            
            # Dosya geçerliyse işle
            if tür == "firmalar":
                if uzanti == ".xlsx":
                    self.import_service.import_excel_firmalar(dosya_yolu)
                elif uzanti == ".csv":
                    self.import_service.import_csv_firmalar(dosya_yolu)
                elif uzanti == ".json":
                    self.import_service.import_json_firmalar(dosya_yolu)
                    
            elif tür == "ogrenciler":
                if uzanti == ".xlsx":
                    self.import_service.import_excel_ogrenciler(dosya_yolu)
                elif uzanti == ".csv":
                    self.import_service.import_csv_ogrenciler(dosya_yolu)
                elif uzanti == ".json":
                    self.import_service.import_json_ogrenciler(dosya_yolu)
            
            messagebox.showinfo("Başarılı", f"{tür.capitalize()} dosyası başarıyla import edildi!")
            
        except Exception as e:
            messagebox.showerror("Import Hatası", f"Dosya import edilirken hata oluştu: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Gui()
    app.run()
