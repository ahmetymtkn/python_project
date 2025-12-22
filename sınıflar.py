class Ogrenciler:
   def __init__(self, id, ogrenci_adi, ort, tercihler, yerlesen_firma_id=None, durum="Yerlesemedi"):
      self.id = id
      self.ogrenci_adi = ogrenci_adi
      self.ort = ort  
      self.tercihler = tercihler
      self.yerlesen_firma_id = yerlesen_firma_id
      self.durum = durum
      self.tercihler_listesi = tercihler.split(",")
      self.tercihler_listesi = [int(i) for i in self.tercihler_listesi]

class Firmalar:
     def __init__(self, id, firma_adi, kontenjan, min_ort, kalan_kontenjan=None):  
         self.id = id
         self.firma_adi = firma_adi
         self.kontenjan = kontenjan
         self.min_ort = min_ort
         self.kalan_kontenjan = kalan_kontenjan if kalan_kontenjan is not None else kontenjan
            