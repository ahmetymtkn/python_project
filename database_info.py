import tkinter as tk
from tkinter import ttk
from connection import get_connection


def tablo_yukle(tree, tabloadi):
    # Önce her şeyi temizle
    tree.delete(*tree.get_children())
    tree["columns"] = ()

    conn = get_connection()
    cursor = conn.cursor()

    # Kolon isimlerini HER ZAMAN al
    cursor.execute(f"PRAGMA table_info({tabloadi})")
    kolonlar = [k[1] for k in cursor.fetchall()]

    tree["columns"] = kolonlar
    tree["show"] = "headings"

    for col in kolonlar:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    # Veriler (boş olabilir)
    cursor.execute(f"SELECT * FROM {tabloadi}")
    veriler = cursor.fetchall()

    if not veriler:
        # Boş tablo mesajı
        tree.insert(
            "",
            tk.END,
            values=["(Kayıt yok)"] + [""] * (len(kolonlar) - 1)
        )
    else:
        for satir in veriler:
            tree.insert("", tk.END, values=satir)

    conn.close()

# -------------------------------------------------
# GUI
# -------------------------------------------------
pencere = tk.Tk()
pencere.title("Staj Yerleştirme Sistemi")
pencere.geometry("1100x600")

# Style (grid çizgileri için)
style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    rowheight=26,
    bordercolor="gray",
    borderwidth=1,
    relief="solid"
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold"),
    borderwidth=1,
    relief="solid"
)

# ---------------- FİRMALAR ----------------
firma_frame = tk.LabelFrame(
    pencere,
    text="Firmalar",
    font=("Arial", 11, "bold"),
    padx=5,
    pady=5
)
firma_frame.pack(fill="both", expand=True, padx=10, pady=5)

firma_tree = ttk.Treeview(firma_frame)
firma_tree.pack(fill="both", expand=True)

# ---------------- ÖĞRENCİLER ----------------
ogrenci_frame = tk.LabelFrame(
    pencere,
    text="Öğrenciler",
    font=("Arial", 11, "bold"),
    padx=5,
    pady=5
)
ogrenci_frame.pack(fill="both", expand=True, padx=10, pady=5)

ogrenci_tree = ttk.Treeview(ogrenci_frame)
ogrenci_tree.pack(fill="both", expand=True)

# İlk yükleme (tablolar boş olsa bile görünür)
tablo_yukle(firma_tree, "firmalar")
tablo_yukle(ogrenci_tree, "ogrenciler")

pencere.mainloop()
