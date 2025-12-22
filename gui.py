import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from ImportService import ImportService
from simulation import Simulation
from ExportService import ExportService
import sys
from io import StringIO

class Gui:
    def __init__(self):
        self.simulation = Simulation()
        self.import_service = ImportService()
        self.export_service = ExportService()
        self.root = tk.Tk()
        self.root.title("Staj Eşleştirme Sistemi")
        self.root.geometry("900x600")
        
        # Dosya yükleme durumları
        self.firma_yuklendi = False
        self.ogrenci_yuklendi = False
        
        self.setup_dosya_yukleme()
    
    def setup_dosya_yukleme(self):
        """Adım 1: Dosya Yükleme Ekranı"""
        self.clear_screen()
        
        # Ana container
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(container, width=300, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Başlık
        tk.Label(left_frame, text="Dosya Yükleme", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Firmalar butonu
        self.firma_btn = tk.Button(left_frame, text="Firmalar Dosyası Seç", 
                                   command=lambda: self.dosya_sec("firmalar"),
                                   bg="#4CAF50", fg="white", width=25, height=2)
        self.firma_btn.pack(pady=10)
        
        # Öğrenciler butonu
        self.ogrenci_btn = tk.Button(left_frame, text="Öğrenciler Dosyası Seç", 
                                     command=lambda: self.dosya_sec("ogrenciler"),
                                     bg="#2196F3", fg="white", width=25, height=2)
        self.ogrenci_btn.pack(pady=10)
        
        # Simulation başlat butonu (başta gizli)
        self.sim_start_btn = tk.Button(left_frame, text="Simülasyon Başlat >", 
                                       command=self.setup_simulation,
                                       bg="#FFA500", fg="white", width=25, height=2)
        self.sim_start_btn.pack(pady=20)
        self.sim_start_btn.pack_forget()  # Gizle
        
        # Sağ panel - Log alanı
        self.setup_log_panel(container)
        
        self.log("Sistem hazır. Lütfen dosyaları yükleyin...")
    
    def setup_simulation(self):
        """Adım 2: Simülasyon Seçenekleri Ekranı"""
        self.clear_screen()
        
        # Ana container
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(container, width=300, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Başlık
        tk.Label(left_frame, text="Simülasyon Seçenekleri", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Greedy butonu
        tk.Button(left_frame, text="Greedy Algoritması", 
                 command=self.run_greedy,
                 bg="#4CAF50", fg="white", width=25, height=2).pack(pady=8)
        
        # Heuristik butonu
        tk.Button(left_frame, text="Heuristik Algoritması", 
                 command=self.run_heuristik,
                 bg="#2196F3", fg="white", width=25, height=2).pack(pady=8)
        
        # Reject Simulation butonu
        tk.Button(left_frame, text="Reject Simülasyonu", 
                 command=self.run_reject,
                 bg="#FF5722", fg="white", width=25, height=2).pack(pady=8)
        
        # Ort Düşür butonu
        tk.Button(left_frame, text="Min Ortalama Düşür (%10)", 
                 command=self.run_ort_dusur,
                 bg="#FF9800", fg="white", width=25, height=2).pack(pady=8)
        
        # Ayırıcı
        tk.Label(left_frame, text="").pack(pady=5)
        
        # Sonuçları Göster butonu
        tk.Button(left_frame, text=" Sonuçları Göster", 
                 command=self.show_results,
                 bg="#00BCD4", fg="white", width=25, height=2).pack(pady=8)
        
        # Export butonu
        tk.Button(left_frame, text="Export Et >", 
                 command=self.setup_export,
                 bg="#9C27B0", fg="white", width=25, height=2).pack(pady=20)
        
        # Sağ panel - Log alanı
        self.setup_log_panel(container)
        
        self.log("Simülasyon ekranı hazır. Algoritma seçin...")
    
    def setup_export(self):
        """Adım 3: Export Format Seçimi Ekranı"""
        self.clear_screen()
        
        # Ana container
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(container, width=300, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Başlık
        tk.Label(left_frame, text="Export Formatı Seçin", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Excel butonu
        tk.Button(left_frame, text="Excel (.xlsx)", 
                 command=lambda: self.export("excel"),
                 bg="#217346", fg="white", width=25, height=2).pack(pady=8)
        
        # CSV butonu
        tk.Button(left_frame, text="CSV (.csv)", 
                 command=lambda: self.export("csv"),
                 bg="#4CAF50", fg="white", width=25, height=2).pack(pady=8)
        
        # JSON butonu
        tk.Button(left_frame, text="JSON (.json)", 
                 command=lambda: self.export("json"),
                 bg="#FF9800", fg="white", width=25, height=2).pack(pady=8)
        
        # Geri dön butonu
        tk.Button(left_frame, text="← Geri Dön", 
                 command=self.setup_simulation,
                 bg="#757575", fg="white", width=25, height=2).pack(pady=20)
        
        # Sağ panel - Log alanı
        self.setup_log_panel(container)
        
        self.log("Export ekranı hazır. Format seçin...")
    
    def setup_log_panel(self, parent):
        """Sağ panel - Log/Konsol çıktısı alanı"""
        right_frame = tk.LabelFrame(parent, text="Log / Konsol Çıktısı", padx=10, pady=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(0,20), pady=20)
        
        # Log text alanı
        self.log_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                   font=("Courier New", 9), 
                                                   bg="#1e1e1e", fg="#00ff00",
                                                   height=30)
        self.log_text.pack(fill='both', expand=True)
    
    def log(self, message):
        """Log mesajı ekle"""
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.root.update()
        print(message)  # Konsola da yazdır
    
    def clear_screen(self):
        """Tüm widget'ları temizle"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def dosya_sec(self, tür):
        """Dosya seç ve yükle"""
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
            self.dosya_isle(dosya_yolu, tür)

    def dosya_isle(self, dosya_yolu, tür):
        """Dosyayı ImportService üzerinden işler"""
        try:
            self.log(f"\n{'='*50}")
            self.log(f"{tür.upper()} DOSYASI YÜKLENİYOR...")
            self.log(f"Dosya: {dosya_yolu}")
            
            self.import_service.import_data(dosya_yolu, tür)
            
            self.log(f"OK {tür.capitalize()} dosyası başarıyla yüklendi!")
            messagebox.showinfo("Başarılı", f"{tür.capitalize()} dosyası başarıyla yüklendi!")
            
            # Durumu güncelle
            if tür == "firmalar":
                self.firma_yuklendi = True
                self.firma_btn.config(text="OK Firmalar Yüklendi", bg="#2E7D32")
                self.log("Firmalar veritabanına kaydedildi.")
            elif tür == "ogrenciler":
                self.ogrenci_yuklendi = True
                self.ogrenci_btn.config(text="OK Öğrenciler Yüklendi", bg="#1565C0")
                self.log("Öğrenciler veritabanına kaydedildi.")
            
            # İkisi de yüklendiyse simülasyon butonunu göster
            if self.firma_yuklendi and self.ogrenci_yuklendi:
                self.sim_start_btn.pack(pady=20)
                self.log("\nOK Tüm dosyalar yüklendi! Simülasyon başlatabilirsiniz.")
                
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", str(e))
    
    def run_greedy(self):
        """Greedy algoritmasını çalıştır"""
        try:
            from greedy import Greedy
            
            self.log("\n" + "="*50)
            self.log("GREEDY ALGORİTMASI BAŞLADI")
            self.log("="*50)
            
            greedy = Greedy()
            greedy.yerlestir()
            
            # İstatistik göster
            stats = self.get_stats()
            self.log(f"\nOK Greedy algoritması tamamlandı!")
            self.log(f"  Yerleşen: {stats['yerlesen']}")
            self.log(f"  Yerleşemeyen: {stats['yerlesemeyen']}")
            self.log(f"  Başarı Oranı: %{stats['oran']:.1f}")
            
            messagebox.showinfo("Başarılı", 
                f"Greedy algoritması tamamlandı!\n\nYerleşen: {stats['yerlesen']}\nYerleşemeyen: {stats['yerlesemeyen']}\nOran: %{stats['oran']:.1f}")
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", f"Greedy hatası: {str(e)}")
    
    def run_heuristik(self):
        """Heuristik algoritmasını çalıştır"""
        try:
            from heuristik import Heuristik
            
            self.log("\n" + "="*50)
            self.log("HEURİSTİK ALGORİTMASI BAŞLADI")
            self.log("="*50)
            
            heuristik = Heuristik()
            heuristik.yerlestir()
            
            # İstatistik göster
            stats = self.get_stats()
            self.log(f"\nOK Heuristik algoritması tamamlandı!")
            self.log(f"  Yerleşen: {stats['yerlesen']}")
            self.log(f"  Yerleşemeyen: {stats['yerlesemeyen']}")
            self.log(f"  Başarı Oranı: %{stats['oran']:.1f}")
            
            messagebox.showinfo("Başarılı", 
                f"Heuristik algoritması tamamlandı!\n\nYerleşen: {stats['yerlesen']}\nYerleşemeyen: {stats['yerlesemeyen']}\nOran: %{stats['oran']:.1f}")
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", f"Heuristik hatası: {str(e)}")
    
    def run_reject(self):
        """Reject simülasyonunu çalıştır"""
        try:
            self.log("\n" + "="*50)
            self.log("REJECT SİMÜLASYONU BAŞLADI")
            self.log("="*50)
            
            stats_before = self.get_stats()
            self.log(f"Başlangıç: Yerleşen={stats_before['yerlesen']}")
            
            self.simulation.reject_simulation()
            
            stats_after = self.get_stats()
            rejected_count = stats_before['yerlesen'] - stats_after['yerlesen']
            self.log(f"OK {rejected_count} öğrenci reddedildi")
            self.log(f"Yeni durum: Yerleşen={stats_after['yerlesen']}, Yerleşemeyen={stats_after['yerlesemeyen']}")
            
            self.log("\nOK Reject simülasyonu tamamlandı!")
            messagebox.showinfo("Başarılı", 
                f"Reject simülasyonu tamamlandı!\n\n{rejected_count} öğrenci reddedildi")
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", f"Reject hatası: {str(e)}")
    
    def run_ort_dusur(self):
        """Minimum ortalama düşürme işlemi"""
        try:
            self.log("\n" + "="*50)
            self.log("MİNİMUM ORTALAMA AZALTMA BAŞLADI")
            self.log("="*50)
            
            self.simulation.reduce_min_ort()
            
            self.log("OK Tüm firmaların min_ort değeri %10 azaltıldı")
            messagebox.showinfo("Başarılı", "Tüm firmaların min_ort değeri %10 azaltıldı!")
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", f"Ort düşürme hatası: {str(e)}")
    
    def export(self, format_type):
        """Veriyi export et"""
        try:
            # Uzantı belirle
            if format_type == "excel":
                ext = ".xlsx"
                file_filter = ("Excel", "*.xlsx")
            elif format_type == "csv":
                ext = ".csv"
                file_filter = ("CSV", "*.csv")
            else:
                ext = ".json"
                file_filter = ("JSON", "*.json")
            
            dosya_yolu = filedialog.asksaveasfilename(
                title="Export dosyası kaydet",
                defaultextension=ext,
                filetypes=[file_filter]
            )
            
            if dosya_yolu:
                self.log(f"\n{'='*50}")
                self.log(f"EXPORT BAŞLADI ({format_type.upper()})")
                self.log(f"Dosya: {dosya_yolu}")
                
                # Yerleşenleri export et
                self.export_service.export_data_yerlesenler(dosya_yolu, format_type)
                
                self.log(f"OK Veriler {format_type.upper()} formatında export edildi!")
                messagebox.showinfo("Başarılı", f"Veriler {format_type.upper()} formatında export edildi!")
        except Exception as e:
            self.log(f"X Export hatası: {str(e)}")
            messagebox.showerror("Hata", f"Export hatası: {str(e)}")
    
    def get_stats(self):
        """Yerleşme istatistiklerini al"""
        from connection import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlestirildi'")
        yerlesen = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlesemedi'")
        yerlesemeyen = cursor.fetchone()[0]
        
        toplam = yerlesen + yerlesemeyen
        oran = (yerlesen / toplam * 100) if toplam > 0 else 0
        
        conn.close()
        
        return {
            'yerlesen': yerlesen,
            'yerlesemeyen': yerlesemeyen,
            'toplam': toplam,
            'oran': oran
        }
    
    def show_results(self):
        """Detaylı sonuçları göster"""
        try:
            from connection import get_connection
            
            self.log("\n" + "="*50)
            self.log("DETAYLI SONUÇLAR")
            self.log("="*50)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Genel istatistikler
            stats = self.get_stats()
            self.log(f"\n GENEL İSTATİSTİKLER:")
            self.log(f"  Toplam Öğrenci: {stats['toplam']}")
            self.log(f"  Yerleşen: {stats['yerlesen']} (%{stats['oran']:.1f})")
            self.log(f"  Yerleşemeyen: {stats['yerlesemeyen']} (%{100-stats['oran']:.1f})")
            
            # Firmalara göre yerleşme
            self.log(f"\n FİRMALARA GÖRE YERLEŞME:")
            cursor.execute("""
                SELECT f.firma_adi, f.kontenjan, f.kalan_kontenjan, 
                       (f.kontenjan - f.kalan_kontenjan) as dolu
                FROM firmalar f
                ORDER BY dolu DESC
            """)
            firmalar = cursor.fetchall()
            
            for firma_adi, kontenjan, kalan, dolu in firmalar:
                doluluk = (dolu / kontenjan * 100) if kontenjan > 0 else 0
                self.log(f"  {firma_adi:20} > {dolu}/{kontenjan} (%{doluluk:.0f}) [Kalan: {kalan}]")
            
            # En yüksek notta yerleşenler
            self.log(f"\n EN YÜKSEK NOTLU YERLEŞENLER (İlk 10):")
            cursor.execute("""
                SELECT o.ogrenci_adi, o.ort, f.firma_adi
                FROM ogrenciler o
                LEFT JOIN firmalar f ON o.yerlesen_firma_id = f.id
                WHERE o.durum = 'Yerlestirildi'
                ORDER BY o.ort DESC
                LIMIT 10
            """)
            yerlesenler = cursor.fetchall()
            
            for i, (ad, ort, firma) in enumerate(yerlesenler, 1):
                self.log(f"  {i:2}. {ad:20} (GPA: {ort:.2f}) > {firma}")
            
            # Yerleşemeyenler
            self.log(f"\n YERLEŞEMEYENLER (İlk 10):")
            cursor.execute("""
                SELECT o.ogrenci_adi, o.ort, o.tercihler
                FROM ogrenciler o
                WHERE o.durum = 'Yerlesemedi'
                ORDER BY o.ort DESC
                LIMIT 10
            """)
            yerlesemeyenler = cursor.fetchall()
            
            for i, (ad, ort, tercihler) in enumerate(yerlesemeyenler, 1):
                self.log(f"  {i:2}. {ad:20} (GPA: {ort:.2f}) - Tercihler: {tercihler}")
            
            conn.close()
            
            messagebox.showinfo("Sonuçlar", 
                f"Detaylı sonuçlar log panelinde gösteriliyor.\n\n"
                f"Toplam: {stats['toplam']}\n"
                f"Yerleşen: {stats['yerlesen']} (%{stats['oran']:.1f})\n"
                f"Yerleşemeyen: {stats['yerlesemeyen']}")
                
        except Exception as e:
            self.log(f"X HATA: {str(e)}")
            messagebox.showerror("Hata", f"Sonuç gösterme hatası: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Gui()
    app.run()
