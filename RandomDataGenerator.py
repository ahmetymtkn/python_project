# Test amaçlı rastgele veri üreten modül
import random
import string
from connection import get_connection

class RandomDataGenerator:
    # Test için rastgele firma ve öğrenci verileri oluşturur
    
    def __init__(self):
        # Firma ve kişi isimleri için hazır listeler
        self.firma_isimleri = [
            "TechCorp", "DataSoft", "CloudWorks", "InnoVate", "SmartSys",
            "CodeLab", "ByteForce", "NetPro", "SoftWave", "DigitalHub",
            "CyberTech", "InfoSys", "TechNova", "LogicFlow", "DataDrive",
            "AppMakers", "WebCraft", "DevTeam", "CodeFactory", "TechZone",
            "SystemPlus", "ProDev", "MegaCode", "EliteIT", "TechPoint"
        ]
        
        self.isimler = [
            "Ahmet", "Mehmet", "Ali", "Ayşe", "Fatma", "Zeynep", "Burak", "Can",
            "Deniz", "Ece", "Elif", "Emre", "Enes", "Furkan", "Gizem", "Hakan",
            "İrem", "Kaan", "Merve", "Mustafa", "Ömer", "Selin", "Serkan", "Tuna",
            "Ufuk", "Yağmur", "Yusuf", "Berk", "Cem", "Defne", "Emir", "Esra"
        ]
        
        self.soyadlar = [
            "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Öztürk", "Aydın",
            "Arslan", "Doğan", "Kılıç", "Aslan", "Koç", "Kurt", "Özdemir", "Polat",
            "Şen", "Erdoğan", "Çetin", "Ak", "Acar", "Güneş", "Korkmaz", "Bulut"
        ]
    
    def generate_random_companies(self, count=10):
        # Belirtilen sayıda rastgele firma oluşturur
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM firmalar")
        
        companies = []
        used_names = set()
        
        for i in range(count):
            while True:
                firma_adi = random.choice(self.firma_isimleri)
                if firma_adi not in used_names:
                    used_names.add(firma_adi)
                    break
            
            kontenjan = random.randint(2, 8)
            min_ort = round(random.uniform(2.0, 3.5), 2)
            
            cursor.execute(
                "INSERT INTO firmalar (firma_adi, kontenjan, kalan_kontenjan, min_ort) VALUES (?, ?, ?, ?)",
                (firma_adi, kontenjan, kontenjan, min_ort)
            )
            
            companies.append({
                'id': i + 1,
                'firma_adi': firma_adi,
                'kontenjan': kontenjan,
                'min_ort': min_ort
            })
        
        conn.commit()
        conn.close()
        
        return companies
    
    def generate_random_students(self, count=50, firma_count=10):
        # Belirtilen sayıda rastgele öğrenci oluşturur
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM ogrenciler")
        
        students = []
        
        for i in range(count):
            isim = random.choice(self.isimler)
            soyad = random.choice(self.soyadlar)
            ogrenci_adi = f"{isim} {soyad}"
            
            ort = round(random.uniform(1.5, 4.0), 2)
            
            tercih_sayisi = random.randint(3, min(5, firma_count))
            tercihler_list = random.sample(range(1, firma_count + 1), tercih_sayisi)
            tercihler = ",".join(map(str, tercihler_list))
            
            cursor.execute(
                "INSERT INTO ogrenciler (ogrenci_adi, ort, tercihler, durum) VALUES (?, ?, ?, ?)",
                (ogrenci_adi, ort, tercihler, "Yerlesemedi")
            )
            
            students.append({
                'id': i + 1,
                'ogrenci_adi': ogrenci_adi,
                'ort': ort,
                'tercihler': tercihler
            })
        
        conn.commit()
        conn.close()
        
        return students
    
    def generate_all(self, firma_count=10, ogrenci_count=None):
        # Firma ve öğrencileri birlikte oluşturur, öğrenci sayısı otomatik hesaplanabilir
        companies = self.generate_random_companies(firma_count)
        
        toplam_kontenjan = sum(company['kontenjan'] for company in companies)
        
        if ogrenci_count is None:
            min_ogrenci = int(toplam_kontenjan * 1.2)
            max_ogrenci = int(toplam_kontenjan * 1.5)
            ogrenci_count = random.randint(min_ogrenci, max_ogrenci)
        else:
            min_ogrenci = int(toplam_kontenjan * 1.2)
            if ogrenci_count < min_ogrenci:
                ogrenci_count = min_ogrenci
        
        students = self.generate_random_students(ogrenci_count, firma_count)
        
        return {
            'companies': companies,
            'students': students,
            'stats': {
                'firma_count': len(companies),
                'toplam_kontenjan': toplam_kontenjan,
                'ogrenci_count': len(students)
            }
        }
