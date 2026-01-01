# Veritabanı verilerini tksheet ile gösteren GUI modülü
import tkinter as tk
from tksheet import Sheet
from connection import get_connection


def tablo_olustur(parent, tablo_adi, baslik):
    # Üst çerçeve oluştur
    frame = tk.LabelFrame(
        parent,
        text=baslik,
        font=("Arial", 11, "bold")
    )
    frame.grid(row=0, column=0, sticky="nsew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    # Veritabanından veri çek
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({tablo_adi})")
    kolonlar = [k[1] for k in cursor.fetchall()]

    cursor.execute(f"SELECT * FROM {tablo_adi}")
    veriler = cursor.fetchall()
    conn.close()

    # tksheet ile tablo oluştur
    sheet = Sheet(
        frame,
        data=veriler,
        headers=kolonlar,
        show_row_index=False,
        header_height=30,
        default_header_height=30,
        table_font=("Arial", 11, "normal"),
        header_font=("Arial", 12, "bold")
    )

    sheet.enable_bindings((
        "single_select",
        "row_select",
        "column_select",
        "column_width_resize",
        "arrowkeys",
        "mousewheel",
        "right_click_popup_menu"
    ))
    
    # Satır yüksekliğini ayarla
    sheet.set_options(default_row_height=25)
    
    # Başlıkları göster
    sheet.headers(kolonlar)

    sheet.grid(row=0, column=0, sticky="nsew")

    # Pencere boyutu değiştiğinde kolonları yeniden ayarla
    def on_resize(event):
        # Mevcut genişliği al ve eşit dağıt
        mevcut_genislik = sheet.winfo_width()
        kolon_sayisi = len(kolonlar)
        
        if kolon_sayisi > 0 and mevcut_genislik > 100:
            # Her kolona eşit genişlik ver
            kolon_genisligi = int(mevcut_genislik / kolon_sayisi) - 10
            for c in range(kolon_sayisi):
                sheet.column_width(c, width=kolon_genisligi)
            # Başlıkları tekrar ayarla
            sheet.headers(kolonlar)
    
    # Resize olayını bağla
    sheet.bind("<Configure>", on_resize)
    
    # İlk yüklemede de ayarla
    sheet.after(100, lambda: on_resize(None))

    # Satır şeritleri ve metin ortalama
    for r in range(len(veriler)):
        stripe_bg = "#ffffff" if r % 2 == 0 else "#f6f6f6"
        for c in range(len(kolonlar)):
            sheet.highlight_cells(r, c, bg=stripe_bg)
            # Metni ortala
            sheet.align_cells(r, c, align="center")

    # Başlıkları da ortala
    for c in range(len(kolonlar)):
        sheet.align_header(c, align="center")

    # Durum renklendirme
    if "durum" in kolonlar:
        d = kolonlar.index("durum")
        for r, satir in enumerate(veriler):
            if str(satir[d]).lower() == "yerlestirildi":
                sheet.highlight_cells(r, d, bg="#90ee90")
            elif str(satir[d]).lower() == "yerlesemedi":
                sheet.highlight_cells(r, d, bg="#f08080")

    return sheet
