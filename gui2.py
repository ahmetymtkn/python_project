import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from ImportService import ImportService
from simulation import Simulation
from ExportService import ExportService
from RandomDataGenerator import RandomDataGenerator
from connection import get_connection
from database_info import tablo_olustur


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

        self.clear_screen()
        
        # Ana container
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(container, width=450, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Bölüm 1: Dosyadan Import
        tk.Label(left_frame, text="━━━ Dosyadan İçe Aktar ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(5,2))
        
        # Butonlar için frame
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=2)
        
        # Firmalar butonu
        self.firma_btn = tk.Button(button_frame, text="📁 Firmalar Dosyası Seç", 
                       command=lambda: self.dosya_sec("firmalar"),
                       bg="#4CAF50", fg="white", width=20, height=2)
        self.firma_btn.pack(side='left', padx=2)
        
        # Öğrenciler butonu
        self.ogrenci_btn = tk.Button(button_frame, text="📁 Öğrenciler Dosyası Seç", 
                         command=lambda: self.dosya_sec("ogrenciler"),
                         bg="#2196F3", fg="white", width=20, height=2)
        self.ogrenci_btn.pack(side='left', padx=2)
        
        # Bölüm 2: Random Veri Oluştur
        tk.Label(left_frame, text="━━━ Veri İşlemleri ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,2))
        
        # Random ve Temizle butonları için frame
        data_ops_frame = tk.Frame(left_frame)
        data_ops_frame.pack(pady=2)

        # Random veri oluştur butonu
        tk.Button(data_ops_frame, text="🎲 Random Veri", 
                 command=self.show_random_data_dialog,
                 bg="#9C27B0", fg="white", width=18, height=2).pack(side='left', padx=2)
        
        # Temizle butonu
        tk.Button(data_ops_frame, text="🗑️ Temizle", 
                 command=self.clear_database,
                 bg="#F44336", fg="white", width=12, height=2).pack(side='left', padx=2)
        

        tk.Label(left_frame, text="━━━ Yerleştirme Algoritmaları ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,2))
        
        tk.Button(left_frame, text="Greedy Algoritması", 
                 command=self.run_greedy,
                 bg="#4CAF50", fg="white", width=28, height=2).pack(pady=2)
        
        tk.Button(left_frame, text="Heuristik Algoritması", 
                 command=self.run_heuristik,
                 bg="#2196F3", fg="white", width=28, height=2).pack(pady=2)
        
        tk.Label(left_frame, text="━━━ Algoritma Karşılaştırma ━━━", 
            font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,2))
        
        # Karşılaştırma sonuçları için grid düzeni
        comparison_frame = tk.LabelFrame(left_frame, text="Algoritma Karşılaştırma", padx=5, pady=2)
        comparison_frame.pack(fill='both', expand=False, pady=(5,2))

        # Headers
        tk.Label(comparison_frame, text="", width=12).grid(row=0, column=0)
        tk.Label(comparison_frame, text="Greedy", font=("Arial", 9, "bold")).grid(row=0, column=1)
        tk.Label(comparison_frame, text="Heuristik", font=("Arial", 9, "bold")).grid(row=0, column=2)

        # Rows
        # İşlem Sayısı
        tk.Label(comparison_frame, text="İşlem Sayısı:", anchor="w", font=("Arial", 8)).grid(row=1, column=0, sticky="w", pady=1)
        self.lbl_greedy_ops = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_greedy_ops.grid(row=1, column=1, pady=1)
        self.lbl_heuristik_ops = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_heuristik_ops.grid(row=1, column=2, pady=1)

        # Süre
        tk.Label(comparison_frame, text="Süre (sn):", anchor="w", font=("Arial", 8)).grid(row=2, column=0, sticky="w", pady=1)
        self.lbl_greedy_time = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_greedy_time.grid(row=2, column=1, pady=1)
        self.lbl_heuristik_time = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_heuristik_time.grid(row=2, column=2, pady=1)

        # Memnuniyet
        tk.Label(comparison_frame, text="Memnuniyet:", anchor="w", font=("Arial", 8)).grid(row=3, column=0, sticky="w", pady=1)
        self.lbl_greedy_sat = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_greedy_sat.grid(row=3, column=1, pady=1)
        self.lbl_heuristik_sat = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_heuristik_sat.grid(row=3, column=2, pady=1)
        
        # Tur Sayısı
        tk.Label(comparison_frame, text="Tur Sayısı:", anchor="w", font=("Arial", 8)).grid(row=4, column=0, sticky="w", pady=1)
        self.lbl_greedy_iter = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_greedy_iter.grid(row=4, column=1, pady=1)
        self.lbl_heuristik_iter = tk.Label(comparison_frame, text="-", font=("Arial", 8))
        self.lbl_heuristik_iter.grid(row=4, column=2, pady=1)

        # Kazanan (Özet)
        tk.Label(comparison_frame, text="Sonuç:", anchor="w", font=("Arial", 8, "bold")).grid(row=5, column=0, sticky="nw", pady=2)
        self.lbl_winner = tk.Label(comparison_frame, text="Henüz karşılaştırma yok", font=("Arial", 8), justify="left", wraplength=250, fg="#555")
        self.lbl_winner.grid(row=5, column=1, columnspan=2, sticky="w", pady=2)

             
        tk.Label(left_frame, text="━━━ Simülasyon İşlemleri ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,2))
        
        sim_button_frame = tk.Frame(left_frame)
        sim_button_frame.pack(pady=2)
        
        tk.Button(sim_button_frame, text="Reject Simülasyonu", 
             command=self.run_reject,
             bg="#FF5722", fg="white", width=20, height=2).pack(side='left', padx=2)

        tk.Button(sim_button_frame, text="Min Ort Düşür (%10)", 
             command=self.run_ort_dusur,
             bg="#FF9800", fg="white", width=20, height=2).pack(side='left', padx=2)

        tk.Button(sim_button_frame, text="Otomatik Döngü", 
             command=self.run_auto_loop,
             bg="#673AB7", fg="white", width=20, height=2).pack(side='left', padx=2)
        
        tk.Label(left_frame, text="━━━ Sonuçlar ve Raporlar ━━━", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,2))
        
        tk.Button(left_frame, text="Export Et", 
                 command=self.setup_export,
                 bg="#9C27B0", fg="white", width=28, height=2,
                 font=("Arial", 10, "bold")).pack(pady=(10,2))
        
        # Log/Sonuç Paneli
        log_frame = tk.LabelFrame(left_frame, text="İşlem Logları / Reject Sonuçları", padx=5, pady=2)
        log_frame.pack(fill='both', expand=True, pady=(5,2))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=("Consolas", 8))
        self.log_text.pack(fill='both', expand=True)
        
        self.setup_info_panel(container)
        
        self.update_info_panel()
    
    
    def setup_export(self):
        # Export seçeneklerini dialog olarak göster
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Seçenekleri")
        export_window.geometry("300x250")
        
        tk.Label(export_window, text="Format Seçin", 
                font=("Arial", 10, "bold"), fg="#555").pack(pady=(10,5))
        
        tk.Button(export_window, text="Excel (.xlsx)", 
                 command=lambda: [self.show_export_options("excel"), export_window.destroy()],
                 bg="#217346", fg="white", width=20).pack(pady=5)
        
        tk.Button(export_window, text="CSV (.csv)", 
                 command=lambda: [self.show_export_options("csv"), export_window.destroy()],
                 bg="#4CAF50", fg="white", width=20).pack(pady=5)
        
        tk.Button(export_window, text="JSON (.json)", 
                 command=lambda: [self.show_export_options("json"), export_window.destroy()],
                 bg="#FF9800", fg="white", width=20).pack(pady=5)
    
    def setup_info_panel(self, parent):
        # Veritabanı bilgi panelini oluşturur
        self.right_frame = tk.Frame(parent)
        self.right_frame.pack(side='right', fill='both', expand=True, padx=0, pady=0)
        
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self.right_frame)
        self.top_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        # İçerik genişlesin diye
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        
        self.bottom_frame = tk.Frame(self.right_frame)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        # İçerik genişlesin diye
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(0, weight=1)
    
    def update_info_panel(self):
        # Veritabanı bilgilerini günceller ve gösterir
        if not hasattr(self, 'top_frame') or not hasattr(self, 'bottom_frame'):
            return

        # Tabloları temizle
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
            
        try:
            tablo_olustur(self.top_frame, "firmalar", "Firmalar")
            tablo_olustur(self.bottom_frame, "ogrenciler", "Öğrenciler")
        except Exception as e:
            print(f"Tablo oluşturma hatası: {e}")
    
    
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
                # cursor.execute("UPDATE firmalar SET kalan_kontenjan = kontenjan") # Firmalar silindiği için gerek yok
                
                conn.commit()
                conn.close()
                
                self.firma_yuklendi = False
                self.ogrenci_yuklendi = False
                
                if hasattr(self, 'firma_btn'):
                    self.firma_btn.config(text="Firmalar Dosyası Seç", bg="#4CAF50")
                if hasattr(self, 'ogrenci_btn'):
                    self.ogrenci_btn.config(text="Öğrenciler Dosyası Seç", bg="#2196F3")
                
                self.update_info_panel()
                
                # Reset labels if they exist
                if hasattr(self, 'lbl_greedy_ops'):
                    self.lbl_greedy_ops.config(text="-")
                    self.lbl_greedy_time.config(text="-")
                    self.lbl_greedy_sat.config(text="-")
                    self.lbl_greedy_iter.config(text="-")
                    self.lbl_heuristik_ops.config(text="-")
                    self.lbl_heuristik_time.config(text="-")
                    self.lbl_heuristik_sat.config(text="-")
                    self.lbl_heuristik_iter.config(text="-")
                
                if hasattr(self, 'algorithm_results'):
                    self.algorithm_results = {}
                
                if hasattr(self, 'lbl_winner'):
                    self.lbl_winner.config(text="Henüz karşılaştırma yok")

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
        self._export_generic(format_type, "yerlesenler")
    
     # Yerleşemeyenleri belirtilen formatta dışa aktarır
    def export_yerlesemeyenler(self, format_type):
        self._export_generic(format_type, "yerlesemeyenler")
    
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
            
            self.update_info_panel()
                
        except Exception as e:
            messagebox.showerror("Hata", str(e))
    
    def calculate_satisfaction(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tercihler, yerlesen_firma_id FROM ogrenciler WHERE durum='Yerlestirildi'")
        rows = cursor.fetchall()
        conn.close()
        
        total_score = 0
        for tercihler, yerlesen_id in rows:
            if not tercihler or not yerlesen_id:
                continue
            try:
                tercih_list = [int(t.strip()) for t in str(tercihler).split(",") if t.strip()]
                if yerlesen_id in tercih_list:
                    rank = tercih_list.index(yerlesen_id) + 1
                    score = max(0, 110 - rank * 10)
                    total_score += score
            except:
                pass
        return total_score

    def run_greedy(self):
        # Greedy algoritmasını çalıştırır
        from greedy import Greedy
        self._run_single_algorithm(Greedy, "Greedy")
    
    def run_heuristik(self):
        # Heuristik algoritmasını çalıştırır
        from heuristik import Heuristik
        self._run_single_algorithm(Heuristik, "Heuristik")

    
    def run_reject(self):
        # Reject simülasyonunu çalıştırır
        try:
            stats_before = self.get_stats()
            
            reddedilenler = self.simulation.reject_simulation()
            
            stats_after = self.get_stats()
            rejected_count = stats_before['yerlesen'] - stats_after['yerlesen']
            
            # Log paneline yaz
            self.log_text.delete(1.0, tk.END) # Önce temizle
            self.log_text.insert(tk.END, f"=== REJECT SİMÜLASYONU SONUÇLARI ===\n")
            self.log_text.insert(tk.END, f"Reddedilen Öğrenci Sayısı: {rejected_count}\n")
            self.log_text.insert(tk.END, f"Yeni Durum: Yerleşen={stats_after['yerlesen']}, Yerleşemeyen={stats_after['yerlesemeyen']}\n\n")
            
            if reddedilenler:
                self.log_text.insert(tk.END, "REDDEDİLEN ÖĞRENCİLER LİSTESİ:\n")
                self.log_text.insert(tk.END, "-" * 40 + "\n")
                for i, ogr in enumerate(reddedilenler, 1):
                    self.log_text.insert(tk.END, f"{i}. {ogr['ad']} (Firma: {ogr['firma']})\n")
            else:
                self.log_text.insert(tk.END, "Hiçbir öğrenci reddedilmedi.\n")
            
            self.log_text.see(tk.END) # En sona kaydır
            
            self.update_info_panel()
            
        except Exception as e:
            self.log_text.insert(tk.END, f"\nHATA: {str(e)}\n")
            messagebox.showerror("Hata", f"Reject hatası: {str(e)}")
    
    def run_ort_dusur(self):
        """Minimum ortalama düşürme işlemi"""
        try:
            self.simulation.reduce_min_ort()
            
            messagebox.showinfo("Başarılı", "Tüm firmaların min_ort değeri %10 azaltıldı!")
            
            self.update_info_panel()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ort düşürme hatası: {str(e)}")
            
    def run_auto_loop(self):
        # Otomatik döngü simülasyonu
        choice = messagebox.askquestion("Algoritma Seçimi", "Otomatik döngü için hangi algoritma kullanılsın?\n\nEvet: Greedy\nHayır: Heuristik", icon='question')
        algo_type = "greedy" if choice == 'yes' else "heuristik"
        
        MAX_ITERATIONS = 50 # Sonsuz döngü koruması
        iteration = 0
        stable_counter = 0
        last_yerlesen = -1
        
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"=== OTOMATİK DÖNGÜ BAŞLATILIYOR ({algo_type.upper()}) ===\n")        
        try:
            while iteration < MAX_ITERATIONS:
                iteration += 1
                self.log_text.insert(tk.END, f"--- TUR {iteration} ---\n")
                self.log_text.update() # UI güncellensin
                
                # 1. Yerleştirme
                if algo_type == "greedy":
                    from greedy import Greedy
                    algo = Greedy()
                    algo.yerlestir()
                    algo_name = "Greedy"
                else:
                    from heuristik import Heuristik
                    algo = Heuristik()
                    algo.yerlestir()
                    algo_name = "Heuristik"
                
                stats = self.get_stats()
                satisfaction = self.calculate_satisfaction()
                current_yerlesen = stats['yerlesen']
                
                # Karşılaştırma Panelini Güncelle
                self._update_algorithm_results(algo_name, algo.islem_sayisi, algo.calisma_suresi, stats, satisfaction, 1)

                self.log_text.insert(tk.END, f"{algo_name} Çalıştı. Yerleşen: {current_yerlesen}\n")
                
                # 1. Herkes yerleşti mi kontrolü
                if stats['yerlesemeyen'] == 0:
                    self.log_text.insert(tk.END, "\n>>> TÜM ÖĞRENCİLER YERLEŞTİ! <<<\n")
                    break

                # 2. Stabilite Kontrolü
                if current_yerlesen == last_yerlesen:
                    stable_counter += 1
                else:
                    stable_counter = 0
                    last_yerlesen = current_yerlesen
                
                if stable_counter >= 3:
                    break
                
                # 2. Reject
                reddedilenler = self.simulation.reject_simulation()
                rejected_count = len(reddedilenler)
                self.log_text.insert(tk.END, f"Reject Simülasyonu: {rejected_count} öğrenci reddedildi.\n")

                # 3. Min Ort Düşür
                self.simulation.reduce_min_ort()
                self.log_text.insert(tk.END, "Otomatik: Firmaların min_ort değeri %10 düşürüldü.\n")
                
                self.update_info_panel()
                self.root.update() # Arayüzü canlı tut
                
            self.log_text.insert(tk.END, f"\n=== SİMÜLASYON TAMAMLANDI ({iteration} Tur) ===\n")
            self.log_text.see(tk.END)
            self.update_info_panel()
            
        except Exception as e:
            self.log_text.insert(tk.END, f"\nHATA: {str(e)}\n")
            messagebox.showerror("Hata", f"Otomatik döngü hatası: {str(e)}")
    
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
        """Her iki algoritmanın sonuçlarını karşılaştırır ve etikete yazar"""
        if not hasattr(self, 'algorithm_results') or len(self.algorithm_results) < 2:
            return
        
        greedy = self.algorithm_results.get('greedy', {})
        heuristik = self.algorithm_results.get('heuristik', {})
        
        summary = ""
        
        # Yerleştirme
        if greedy['yerlesen'] > heuristik['yerlesen']:
            summary += "✅ Yerleştirme: Greedy\n"
        elif heuristik['yerlesen'] > greedy['yerlesen']:
            summary += "✅ Yerleştirme: Heuristik\n"
        else:
            summary += "⚖️ Yerleştirme: Eşit\n"
            
        # Memnuniyet
        if greedy.get('satisfaction', 0) > heuristik.get('satisfaction', 0):
             summary += "✅ Memnuniyet: Greedy\n"
        elif heuristik.get('satisfaction', 0) > greedy.get('satisfaction', 0):
             summary += "✅ Memnuniyet: Heuristik\n"
        else:
             summary += "⚖️ Memnuniyet: Eşit\n"
        
        # Hız
        if greedy['sure'] < heuristik['sure']:
            summary += f"⏱️ Hız: Greedy\n"
        else:
            summary += f"⏱️ Hız: Heuristik\n"
            
        # Verimlilik
        if greedy['islem_sayisi'] < heuristik['islem_sayisi']:
            summary += f"🔢 Verimlilik: Greedy"
        else:
            summary += f"🔢 Verimlilik: Heuristik"
            
        if hasattr(self, 'lbl_winner'):
            self.lbl_winner.config(text=summary, fg="#000")

    def _update_algorithm_results(self, algo_name, delta_ops, delta_time, stats, satisfaction, delta_iter=1):
        """Ortak algoritma sonuç güncelleme ve kaydetme metodu (Kümülatif)"""
        prefix = "greedy" if algo_name.lower() == "greedy" else "heuristik"
        
        # Mevcut değerleri al
        if not hasattr(self, 'algorithm_results'):
            self.algorithm_results = {}
            
        current_data = self.algorithm_results.get(prefix, {
            'islem_sayisi': 0,
            'sure': 0,
            'iteration': 0
        })
        
        # Kümülatif toplama
        new_ops = current_data.get('islem_sayisi', 0) + delta_ops
        new_time = current_data.get('sure', 0) + delta_time
        new_iter = current_data.get('iteration', 0) + delta_iter
        
        # Label güncelleme
        if hasattr(self, f'lbl_{prefix}_ops'):
            getattr(self, f'lbl_{prefix}_ops').config(text=str(new_ops))
            getattr(self, f'lbl_{prefix}_time').config(text=f"{new_time:.4f}")
            getattr(self, f'lbl_{prefix}_sat').config(text=str(satisfaction))
            getattr(self, f'lbl_{prefix}_iter').config(text=str(new_iter))

        # Sonuçları kaydet
        self.algorithm_results[prefix] = {
            'yerlesen': stats['yerlesen'],
            'yerlesemeyen': stats['yerlesemeyen'],
            'oran': stats['oran'],
            'islem_sayisi': new_ops,
            'sure': new_time,
            'satisfaction': satisfaction,
            'iteration': new_iter
        }
        
        if 'greedy' in self.algorithm_results and 'heuristik' in self.algorithm_results:
            self.show_comparison()

    def _run_single_algorithm(self, algo_class, algo_name):
        """Tekil algoritma çalıştırma ve raporlama metodu"""
        try:
            algo = algo_class()
            algo.yerlestir()
            
            stats = self.get_stats()
            satisfaction = self.calculate_satisfaction()
            
            # Kümülatif güncelleme için delta değerleri gönderiyoruz
            self._update_algorithm_results(algo_name, algo.islem_sayisi, algo.calisma_suresi, stats, satisfaction, 1)
            
            # Mesaj kutusunda o anki (son) çalışmanın sonuçlarını gösteriyoruz
            # Ancak toplam değerleri göstermek istersek self.algorithm_results'dan çekebiliriz.
            # Kullanıcı "tekil adım adım" dediği için, mesaj kutusunda o anki çalışmayı göstermek mantıklı olabilir,
            # ama panelde kümülatif artacak.
            
            messagebox.showinfo("Başarılı", 
                f"{algo_name} algoritması tamamlandı!\n\n"
                f"Yerleşen: {stats['yerlesen']}\n"
                f"Yerleşemeyen: {stats['yerlesemeyen']}\n"
                f"Başarı Oranı: %{stats['oran']:.1f}\n"
                f"İşlem Sayısı (Bu Tur): {algo.islem_sayisi}\n"
                f"Çalışma Süresi (Bu Tur): {algo.calisma_suresi:.4f} saniye\n"
                f"Memnuniyet Skoru: {satisfaction}")
            
            self.update_info_panel()
            
        except Exception as e:
            messagebox.showerror("Hata", f"{algo_name} hatası: {str(e)}")

    def _export_generic(self, format_type, data_type):
        """Ortak export metodu"""
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
            
            title_prefix = "Yerleşenler" if data_type == "yerlesenler" else "Yerleşemeyenler"
            default_filename = f"{data_type}{ext}"
            
            dosya_yolu = filedialog.asksaveasfilename(
                title=f"{title_prefix} - Export dosyası kaydet",
                defaultextension=ext,
                filetypes=[file_filter],
                initialfile=default_filename
            )
            
            if dosya_yolu:
                if data_type == "yerlesenler":
                    self.export_service.export_data_yerlesenler(dosya_yolu, format_type)
                else:
                    self.export_service.export_data_yerlesemeyenler(dosya_yolu, format_type)
                    
                messagebox.showinfo("Başarılı", f"{title_prefix} {format_type.upper()} formatında export edildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Export hatası: {str(e)}")

    # Ana pencereyi çalıştırır
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Gui()
    
    app.run()

