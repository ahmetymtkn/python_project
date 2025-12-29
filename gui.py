import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, simpledialog
from ImportService import ImportService
from simulation import Simulation
from ExportService import ExportService
from RandomDataGenerator import RandomDataGenerator
from connection import get_connection
import sys
from io import StringIO

class Gui:
    # Staj eşleştirme sisteminin arayüzünü yönetir
    def __init__(self):
        self.simulation = Simulation()
        self.import_service = ImportService()
        self.export_service = ExportService()
        self.random_generator = RandomDataGenerator()
        self.root = tk.Tk()
        self.root.title("Staj Eşleştirme Sistemi")
        self.root.geometry("1100x700")
        
        # Dosya yükleme durumları
        self.firma_yuklendi = False
        self.ogrenci_yuklendi = False
        
        self.setup_dosya_yukleme()
    
    def setup_dosya_yukleme(self):
        """Adım 1: Veri Yükleme Ekranı - Geliştirilmiş"""
        self.clear_screen()
        
        # Ana container
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(container, width=350, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Başlık
        tk.Label(left_frame, text="Veri Yükleme", font=("Arial", 16, "bold")).pack(pady=15)
        
        # Bölüm 1: Dosyadan Import
        tk.Label(left_frame, text="━━━ Dosyadan İçe Aktar ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,5))
        
        # Firmalar butonu
        self.firma_btn = tk.Button(left_frame, text="📁 Firmalar Dosyası Seç", 
                                   command=lambda: self.dosya_sec("firmalar"),
                                   bg="#4CAF50", fg="white", width=28, height=2)
        self.firma_btn.pack(pady=5)
        
        # Öğrenciler butonu
        self.ogrenci_btn = tk.Button(left_frame, text="📁 Öğrenciler Dosyası Seç", 
                                     command=lambda: self.dosya_sec("ogrenciler"),
                                     bg="#2196F3", fg="white", width=28, height=2)
        self.ogrenci_btn.pack(pady=5)
        
        # Bölüm 2: Random Veri Oluştur
        tk.Label(left_frame, text="━━━ Rastgele Veri Oluştur ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(20,5))
        
        # Random veri oluştur butonu
        tk.Button(left_frame, text="🎲 Random Veri Oluştur", 
                 command=self.show_random_data_dialog,
                 bg="#9C27B0", fg="white", width=28, height=2).pack(pady=5)
        
        # Ayırıcı
        tk.Label(left_frame, text="━━━━━━━━━━━━━━━━━━━━", 
                font=("Arial", 10), fg="#ccc").pack(pady=(20,5))
        
        # Veritabanını Temizle
        tk.Button(left_frame, text="🗑️ Veritabanını Temizle", 
                 command=self.clear_database,
                 bg="#F44336", fg="white", width=28, height=2).pack(pady=5)
        
        # Simulation başlat butonu (başta gizli)
        self.sim_start_btn = tk.Button(left_frame, text="▶ Simülasyon Başlat", 
                                       command=self.setup_simulation,
                                       bg="#FFA500", fg="white", width=28, height=2,
                                       font=("Arial", 10, "bold"))
        
        # Eğer veriler yüklüyse butonu göster
        if self.firma_yuklendi and self.ogrenci_yuklendi:
            self.sim_start_btn.pack(pady=(20,10))
        else:
            self.sim_start_btn.pack(pady=(20,10))
            self.sim_start_btn.pack_forget()  # Gizle
        
        # Sağ panel - Bilgi paneli
        self.setup_info_panel(container)
        
        self.update_info_panel()
    
    def setup_simulation(self):
        # Simülasyon ve algoritma seçenekleri ekranını oluşturur
        self.clear_screen()
        
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        left_frame = tk.Frame(container, width=350, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="Simülasyon Seçenekleri", font=("Arial", 16, "bold")).pack(pady=15)
        
        tk.Label(left_frame, text="Yerleştirme Algoritmaları", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,5))
        
        tk.Button(left_frame, text="Greedy Algoritması", 
                 command=self.run_greedy,
                 bg="#4CAF50", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Button(left_frame, text="Heuristik Algoritması", 
                 command=self.run_heuristik,
                 bg="#2196F3", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Label(left_frame, text="Simülasyon İşlemleri", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(15,5))
        
        tk.Button(left_frame, text="Reject Simülasyonu", 
                 command=self.run_reject,
                 bg="#FF5722", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Button(left_frame, text="Min Ortalama Düşür (%10)", 
                 command=self.run_ort_dusur,
                 bg="#FF9800", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Label(left_frame, text="Sonuçlar ve Raporlar", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(15,5))
        
        tk.Button(left_frame, text="Export Et", 
                 command=self.setup_export,
                 bg="#9C27B0", fg="white", width=28, height=2,
                 font=("Arial", 10, "bold")).pack(pady=(15,5))
        
        tk.Button(left_frame, text="Geri Dön", 
                 command=self.setup_dosya_yukleme,
                 bg="#757575", fg="white", width=28, height=2).pack(pady=(10,5))
        
        # Sağ panel - Bilgi paneli
        self.setup_info_panel(container)
        
        self.update_info_panel()
    
    def setup_export(self):
        # Export format seçim ekranını oluşturur
        self.clear_screen()
        
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        left_frame = tk.Frame(container, width=350, padx=20, pady=20)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="Export Seçenekleri", font=("Arial", 16, "bold")).pack(pady=15)
        
        tk.Label(left_frame, text="Format Seçin", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,5))
        
        tk.Button(left_frame, text="Excel (.xlsx)", 
                 command=lambda: self.show_export_options("excel"),
                 bg="#217346", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Button(left_frame, text="CSV (.csv)", 
                 command=lambda: self.show_export_options("csv"),
                 bg="#4CAF50", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Button(left_frame, text="JSON (.json)", 
                 command=lambda: self.show_export_options("json"),
                 bg="#FF9800", fg="white", width=28, height=2).pack(pady=5)
        
        tk.Button(left_frame, text="Geri Dön", 
                 command=self.setup_simulation,
                 bg="#757575", fg="white", width=28, height=2).pack(pady=(20,5))
        
        # Sağ panel - Veritabanı Bilgisi
        self.setup_database_info_panel(container)
        
        self.update_database_info()
    
    def setup_info_panel(self, parent):
        # Veritabanı bilgi panelini oluşturur
        right_frame = tk.LabelFrame(parent, text="Veritabanı Bilgisi", padx=10, pady=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(0,20), pady=20)
        
        self.info_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                   font=("Consolas", 10), 
                                                   bg="#f5f5f5", fg="#333",
                                                   height=30)
        self.info_text.pack(fill='both', expand=True)
    
    def setup_database_info_panel(self, parent):
        # Veritabanı detay panelini oluşturur
        right_frame = tk.LabelFrame(parent, text="Veritabanı Detayları", padx=10, pady=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(0,20), pady=20)
        self.db_info_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                   font=("Consolas", 9), 
                                                   bg="#f5f5f5", fg="#333",
                                                   height=30)
        self.db_info_text.pack(fill='both', expand=True)
    
    def update_info_panel(self):
        # Veritabanı bilgilerini günceller ve gösterir
        if not hasattr(self, 'info_text'):
            return
            
        self.info_text.delete(1.0, tk.END)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Genel bilgiler
            cursor.execute("SELECT COUNT(*), SUM(kontenjan), SUM(kalan_kontenjan) FROM firmalar")
            firma_count, toplam_kontenjan, kalan_kontenjan = cursor.fetchone()
            toplam_kontenjan = toplam_kontenjan or 0
            kalan_kontenjan = kalan_kontenjan or 0
            
            cursor.execute("SELECT COUNT(*) FROM ogrenciler")
            ogrenci_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlestirildi'")
            yerlesen_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlesemedi'")
            yerlesemeyen_count = cursor.fetchone()[0]
            
            # Başlık
            info = "VERİTABANI DURUMU\n" + "="*70 + "\n\n"
            
            info += f"FİRMALAR: {firma_count} | KONTENJAN: {toplam_kontenjan} | KALAN: {kalan_kontenjan}\n"
            info += f"ÖĞRENCİLER: {ogrenci_count} | YERLEŞEN: {yerlesen_count} | YERLEŞEMEYEN: {yerlesemeyen_count}\n"
            
            if ogrenci_count > 0:
                oran = (yerlesen_count / ogrenci_count) * 100
                info += f"YERLEŞME ORANI: %{oran:.1f}\n"
            
            info += "\n" + "-"*70 + "\n"
            
            # Firma detayları
            cursor.execute("""
                SELECT f.id, f.firma_adi, f.kontenjan, f.kalan_kontenjan, 
                       (f.kontenjan - f.kalan_kontenjan) as dolu, f.min_ort
                FROM firmalar f
                ORDER BY f.id
            """)
            firmalar = cursor.fetchall()
            
            if firmalar:
                info += "\nFİRMA BİLGİLERİ:\n" + "-"*70 + "\n"
                for firma_id, firma_adi, kontenjan, kalan, dolu, min_ort in firmalar:
                    info += f"[{firma_id}] {firma_adi}: {dolu}/{kontenjan}  Min GPA: {min_ort:.2f}\n"
                info += "\n" + "-"*70 + "\n"
            
            # Yerleşenler listesi
            if yerlesen_count > 0:
                info += f"\nYERLEŞENLER ({yerlesen_count}):\n" + "-"*70 + "\n"
                cursor.execute("""
                    SELECT o.ogrenci_adi, o.ort, f.firma_adi, o.tercihler, o.yerlesen_firma_id
                    FROM ogrenciler o
                    LEFT JOIN firmalar f ON o.yerlesen_firma_id = f.id
                    WHERE o.durum = 'Yerlestirildi'
                    ORDER BY o.ort DESC
                """)
                
                for i, (ad, ort, firma, tercihler, firma_id) in enumerate(cursor.fetchall(), 1):
                    tercih_info = ""
                    if tercihler and firma_id:
                        try:
                            tercih_list = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
                            tercih_str = ",".join(map(str, tercih_list))
                            if firma_id in tercih_list:
                                sira = tercih_list.index(firma_id) + 1
                                tercih_info = f" Tercihler:({tercih_str}) [{sira}. tercih]"
                            else:
                                tercih_info = f" Tercihler:({tercih_str})"
                        except:
                            pass
                    info += f"{i:3}. {ad:25} (GPA: {ort:.2f}){tercih_info} -> {firma}\n"
            
            # Yerleşemeyenler listesi
            if yerlesemeyen_count > 0:
                info += f"\nYERLEŞEMEYENLER ({yerlesemeyen_count}):\n" + "-"*70 + "\n"
                cursor.execute("""
                    SELECT o.ogrenci_adi, o.ort, o.tercihler
                    FROM ogrenciler o
                    WHERE o.durum = 'Yerlesemedi'
                    ORDER BY o.ort DESC
                """)
                
                for i, (ad, ort, tercihler) in enumerate(cursor.fetchall(), 1):
                    tercih_str = ""
                    if tercihler:
                        try:
                            tercih_list = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
                            tercih_str = " Tercihler:(" + ",".join(map(str, tercih_list)) + ")"
                        except:
                            pass
                    info += f"{i:3}. {ad:25} (GPA: {ort:.2f}){tercih_str}\n"
            
            conn.close()
            
            self.info_text.insert(tk.END, info)
            
        except Exception as e:
            self.info_text.insert(tk.END, f"Hata: {str(e)}")
    
    def update_database_info(self):
        """Veritabanı detaylarını güncelle"""
        if hasattr(self, 'db_info_text'):
            self.db_info_text.delete(1.0, tk.END)
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                info = "╭──────────────────────────────────────────╮\n"
                info += "│      VERİTABANI DETAYLI BİLGİLER         │\n"
                info += "╰──────────────────────────────────────────╯\n\n"
                
                info += "FİRMALAR:\n"
                info += "─" * 60 + "\n"
                cursor.execute("SELECT firma_adi, kontenjan, kalan_kontenjan, min_ort FROM firmalar ORDER BY firma_adi")
                firmalar = cursor.fetchall()
                
                if firmalar:
                    for firma_adi, kontenjan, kalan, min_ort in firmalar:
                        dolu = kontenjan - kalan
                        doluluk = (dolu / kontenjan * 100) if kontenjan > 0 else 0
                        info += f"  {firma_adi:20} | Kont: {kontenjan:2} | Dolu: {dolu:2} ({doluluk:5.1f}%) | Min GPA: {min_ort:.2f}\n"
                else:
                    info += "  (Henüz firma verisi yok)\n"
                
                info += "\n"
                
                info += "ÖĞRENCİLER (ÖZET):\n"
                info += "─" * 60 + "\n"
                
                cursor.execute("SELECT COUNT(*), AVG(ort) FROM ogrenciler")
                total, avg_ort = cursor.fetchone()
                avg_ort = avg_ort or 0
                
                cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlestirildi'")
                yerlesen = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE durum='Yerlesemedi'")
                yerlesemeyen = cursor.fetchone()[0]
                
                info += f"  Toplam Öğrenci: {total}\n"
                info += f"  Ortalama GPA: {avg_ort:.2f}\n"
                info += f"  Yerleşen: {yerlesen}\n"
                info += f"  Yerleşemeyen: {yerlesemeyen}\n"
                
                conn.close()
                
                self.db_info_text.insert(tk.END, info)
                
            except Exception as e:
                self.db_info_text.insert(tk.END, f"Bilgi alınamadı: {str(e)}")
    
    def show_random_data_dialog(self):
        # Random veri oluşturur (10 firma, otomatik öğrenci)
        try:
            result = self.random_generator.generate_all(firma_count=10, ogrenci_count=None)
                
            actual_ogrenci = result['stats']['ogrenci_count']
            toplam_kontenjan = result['stats']['toplam_kontenjan']
            
            self.firma_yuklendi = True
            self.ogrenci_yuklendi = True
            
            self.firma_btn.config(text="Firmalar Yüklendi (Random)", bg="#2E7D32")
            self.ogrenci_btn.config(text="Öğrenciler Yüklendi (Random)", bg="#1565C0")
            self.sim_start_btn.pack(pady=(20,10))
            
            self.update_info_panel()
            
        except Exception as e:
                messagebox.showerror("Hata", f"Random veri oluşturma hatası: {str(e)}")
        
    def show_random_data_dialog(self):
        # Random veri oluşturur (10 firma, otomatik öğrenci)
        try:
            result = self.random_generator.generate_all(firma_count=10, ogrenci_count=None)
            
            firma_count = result['stats']['firma_count']
            actual_ogrenci = result['stats']['ogrenci_count']
            toplam_kontenjan = result['stats']['toplam_kontenjan']
            
            self.firma_yuklendi = True
            self.ogrenci_yuklendi = True
            
            self.firma_btn.config(text="Firmalar Yüklendi (Random)", bg="#2E7D32")
            self.ogrenci_btn.config(text="Öğrenciler Yüklendi (Random)", bg="#1565C0")
            self.sim_start_btn.pack(pady=(20,10))
            
            self.update_info_panel()
            
            messagebox.showinfo("Başarılı", 
                f"{firma_count} firma oluşturuldu\n"
                f"Toplam kontenjan: {toplam_kontenjan}\n"
                f"{actual_ogrenci} öğrenci oluşturuldu\n"
                f"Oran: {actual_ogrenci/toplam_kontenjan:.2f}x")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Random veri oluşturma hatası: {str(e)}")
    
    def clear_database(self):
        # Veritabanındaki tüm verileri temizler
        if messagebox.askyesno("Onay", "Tüm veriler silinecek. Emin misiniz?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM ogrenciler")
                cursor.execute("DELETE FROM firmalar")
                cursor.execute("UPDATE firmalar SET kalan_kontenjan = kontenjan")
                
                conn.commit()
                conn.close()
                
                self.firma_yuklendi = False
                self.ogrenci_yuklendi = False
                
                self.firma_btn.config(text="Firmalar Dosyası Seç", bg="#4CAF50")
                self.ogrenci_btn.config(text="Öğrenciler Dosyası Seç", bg="#2196F3")
                self.sim_start_btn.pack_forget()
                
                self.update_info_panel()
                
                messagebox.showinfo("Başarılı", "Veritabanı temizlendi!")
                
            except Exception as e:
                messagebox.showerror("Hata", f"Temizleme hatası: {str(e)}")
    
    def show_export_options(self, format_type):
        # Export format seçim penceresini açar
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Export - {format_type.upper()}")
        dialog.geometry("350x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Ne export etmek istersiniz?", 
                font=("Arial", 12, "bold")).pack(pady=20)
        
        tk.Button(dialog, text="Yerleşenler", 
                 command=lambda: [self.export_yerlesenler(format_type), dialog.destroy()],
                 bg="#4CAF50", fg="white", width=20, height=2).pack(pady=5)
        
        tk.Button(dialog, text="Yerleşemeyenler", 
                 command=lambda: [self.export_yerlesemeyenler(format_type), dialog.destroy()],
                 bg="#FF5722", fg="white", width=20, height=2).pack(pady=5)
    
    def export_yerlesenler(self, format_type):
        # Yerleşenleri belirtilen formatta dışa aktarır
        try:
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
                title="Yerleşenler - Export dosyası kaydet",
                defaultextension=ext,
                filetypes=[file_filter],
                initialfile=f"yerlesenler{ext}"
            )
            
            if dosya_yolu:
                self.export_service.export_data_yerlesenler(dosya_yolu, format_type)
                messagebox.showinfo("Başarılı", f"Yerleşenler {format_type.upper()} formatında export edildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Export hatası: {str(e)}")
    
     # Yerleşemeyenleri belirtilen formatta dışa aktarır
    def export_yerlesemeyenler(self, format_type):
        try:
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
                title="Yerleşemeyenler - Export dosyası kaydet",
                defaultextension=ext,
                filetypes=[file_filter],
                initialfile=f"yerlesemeyenler{ext}"
            )
            
            if dosya_yolu:
                self.export_service.export_data_yerlesemeyenler(dosya_yolu, format_type)
                messagebox.showinfo("Başarılı", f"Yerleşemeyenler {format_type.upper()} formatında export edildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Export hatası: {str(e)}")
    
    # Ekrandaki tüm bileşenleri temizler
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def dosya_sec(self, tür):
        # Kullanıcıdan dosya seçmesini ister
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
        # Seçilen dosyayı içe aktarır
        try:
            self.import_service.import_data(dosya_yolu, tür)
            
            messagebox.showinfo("Başarılı", f"{tür.capitalize()} dosyası başarıyla yüklendi!")
            
            if tür == "firmalar":
                self.firma_yuklendi = True
                self.firma_btn.config(text="Firmalar Yüklendi", bg="#2E7D32")
            elif tür == "ogrenciler":
                self.ogrenci_yuklendi = True
                self.ogrenci_btn.config(text="Öğrenciler Yüklendi", bg="#1565C0")
            
            if self.firma_yuklendi and self.ogrenci_yuklendi:
                self.sim_start_btn.pack(pady=(20,10))
            
            self.update_info_panel()
                
        except Exception as e:
            messagebox.showerror("Hata", str(e))
    
    def run_greedy(self):
        # Greedy algoritmasını çalıştırır
        try:
            from greedy import Greedy
            
            greedy = Greedy()
            yerlestirilen = greedy.yerlestir()
            
            stats = self.get_stats()
            
            messagebox.showinfo("Başarılı", 
                f"Greedy algoritması tamamlandı!\n\n"
                f"Yerleşen: {stats['yerlesen']}\n"
                f"Yerleşemeyen: {stats['yerlesemeyen']}\n"
                f"Başarı Oranı: %{stats['oran']:.1f}\n"
                f"\u0130şlem Sayısı: {greedy.islem_sayisi}\n"
                f"Çalışma Süresi: {greedy.calisma_suresi:.4f} saniye")
            
            self.update_info_panel()
            
            # Sonuçları kaydet karşılaştırma için
            if not hasattr(self, 'algorithm_results'):
                self.algorithm_results = {}
            self.algorithm_results['greedy'] = {
                'yerlesen': stats['yerlesen'],
                'yerlesemeyen': stats['yerlesemeyen'],
                'oran': stats['oran'],
                'islem_sayisi': greedy.islem_sayisi,
                'sure': greedy.calisma_suresi
            }
            
            # Eğer heuristik de varsa karşılaştır
            if 'heuristik' in self.algorithm_results:
                self.show_comparison()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Greedy hatası: {str(e)}")
    
    def run_heuristik(self):
        # Heuristik algoritmasını çalıştırır
        try:
            from heuristik import Heuristik
            
            heuristik = Heuristik()
            yerlestirilen = heuristik.yerlestir()
            
            stats = self.get_stats()
            
            messagebox.showinfo("Başarılı", 
                f"Heuristik algoritması tamamlandı!\n\n"
                f"Yerleşen: {stats['yerlesen']}\n"
                f"Yerleşemeyen: {stats['yerlesemeyen']}\n"
                f"Başarı Oranı: %{stats['oran']:.1f}\n"
                f"\u0130şlem Sayısı: {heuristik.islem_sayisi}\n"
                f"Çalışma Süresi: {heuristik.calisma_suresi:.4f} saniye")
            
            self.update_info_panel()
            
            # Sonuçları kaydet karşılaştırma için
            if not hasattr(self, 'algorithm_results'):
                self.algorithm_results = {}
            self.algorithm_results['heuristik'] = {
                'yerlesen': stats['yerlesen'],
                'yerlesemeyen': stats['yerlesemeyen'],
                'oran': stats['oran'],
                'islem_sayisi': heuristik.islem_sayisi,
                'sure': heuristik.calisma_suresi
            }
            
            # Eğer greedy de varsa karşılaştır
            if 'greedy' in self.algorithm_results:
                self.show_comparison()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Heuristik hatası: {str(e)}")
    
    def run_reject(self):
        # Reject simülasyonunu çalıştırır
        try:
            stats_before = self.get_stats()
            
            reddedilenler = self.simulation.reject_simulation()
            
            stats_after = self.get_stats()
            rejected_count = stats_before['yerlesen'] - stats_after['yerlesen']
            
            # Reddedilen öğrencilerin detaylarını hazırla
            red_detay = ""
            if reddedilenler:
                red_detay = "\n\nReddedilen Öğrenciler:\n"
                for i, ogr in enumerate(reddedilenler[:10], 1):  # İlk 10'unu göster
                    red_detay += f"{i}. {ogr['ad']} - {ogr['firma']}\n"
                if len(reddedilenler) > 10:
                    red_detay += f"... ve {len(reddedilenler)-10} öğrenci daha"
            
            messagebox.showinfo("Başarılı", 
                f"Reject simülasyonu tamamlandı!\n\n"
                f"{rejected_count} öğrenci reddedildi\n"
                f"Yeni durum: Yerleşen={stats_after['yerlesen']}, "
                f"Yerleşemeyen={stats_after['yerlesemeyen']}{red_detay}")
            
            self.update_info_panel()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Reject hatası: {str(e)}")
    
    def run_ort_dusur(self):
        """Minimum ortalama düşürme işlemi"""
        try:
            self.simulation.reduce_min_ort()
            
            messagebox.showinfo("Başarılı", "Tüm firmaların min_ort değeri %10 azaltıldı!")
            
            self.update_info_panel()
            self.update_database_info()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ort düşürme hatası: {str(e)}")
    
    def get_stats(self):
        # Yerleşme istatistiklerini hesaplar
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
    
    def show_comparison(self):
        """Her iki algoritmanın sonuçlarını karşılaştırır"""
        if not hasattr(self, 'algorithm_results') or len(self.algorithm_results) < 2:
            return
        
        greedy = self.algorithm_results.get('greedy', {})
        heuristik = self.algorithm_results.get('heuristik', {})
        
        comparison = "="*60 + "\n"
        comparison += "ALGorİTMA KARŞILAŞTIRMASI\n"
        comparison += "="*60 + "\n\n"
        
        comparison += f"{'Metrik':<25} {'Greedy':<15} {'Heuristik':<15}\n"
        comparison += "-"*60 + "\n"
        comparison += f"{'Yerleşen':<25} {greedy['yerlesen']:<15} {heuristik['yerlesen']:<15}\n"
        comparison += f"{'Yerleşemeyen':<25} {greedy['yerlesemeyen']:<15} {heuristik['yerlesemeyen']:<15}\n"
        comparison += f"{'Başarı Oranı (%)':<25} {greedy['oran']:<15.2f} {heuristik['oran']:<15.2f}\n"
        comparison += f"{'İşlem Sayısı':<25} {greedy['islem_sayisi']:<15} {heuristik['islem_sayisi']:<15}\n"
        comparison += f"{'Çalışma Süresi (sn)':<25} {greedy['sure']:<15.4f} {heuristik['sure']:<15.4f}\n"
        comparison += "\n" + "="*60 + "\n\n"
        
        # Kazananları belirle
        comparison += "KAZANANLAR:\n"
        comparison += "-"*60 + "\n"
        
        if greedy['yerlesen'] > heuristik['yerlesen']:
            comparison += "✅ Yerleştirme: Greedy\n"
        elif heuristik['yerlesen'] > greedy['yerlesen']:
            comparison += "✅ Yerleştirme: Heuristik\n"
        else:
            comparison += "⚖️ Yerleştirme: Eşit\n"
        
        if greedy['sure'] < heuristik['sure']:
            comparison += f"⏱️ Hız: Greedy ({greedy['sure']:.4f}s)\n"
        else:
            comparison += f"⏱️ Hız: Heuristik ({heuristik['sure']:.4f}s)\n"
        
        if greedy['islem_sayisi'] < heuristik['islem_sayisi']:
            comparison += f"🔢 Verimlilik: Greedy ({greedy['islem_sayisi']} işlem)\n"
        else:
            comparison += f"🔢 Verimlilik: Heuristik ({heuristik['islem_sayisi']} işlem)\n"
        
        messagebox.showinfo("Algoritma Karşılaştırması", comparison)

    # Ana pencereyi çalıştırır
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Gui()
    app.run()

