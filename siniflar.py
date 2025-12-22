class Ogrenciler:
   def __init__(self, id, ogrenci_adi, ort, tercihler, yerlesen_firma_id=None, durum="Yerlesemedi"):
      self.id = id
      self.ogrenci_adi = ogrenci_adi
      self.ort = ort  
      self.tercihler = tercihler
      self.yerlesen_firma_id = yerlesen_firma_id
      self.durum = durum
      # Boş string kontrolü - boş ise liste de boş olsun
      if tercihler and tercihler.strip():
          self.tercihler_listesi = [int(i.strip()) for i in tercihler.split(",") if i.strip()]
      else:
          self.tercihler_listesi = []

class Firmalar:
     def __init__(self, id, firma_adi, kontenjan, min_ort, kalan_kontenjan=None):  
         self.id = id
         self.firma_adi = firma_adi
         self.kontenjan = kontenjan
         self.min_ort = min_ort
         # Sadece None ise kontenjan'a eşitle (ilk import için)
         # 0 geçerli bir değer (kontenjan dolmuş demek)
         self.kalan_kontenjan = kalan_kontenjan if kalan_kontenjan is not None else kontenjan
            