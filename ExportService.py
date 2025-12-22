from connection import get_connection
import pandas as pd


class ExportService:

    def export_yerlesenler_excel(self,file_path="exported_yerlesenler.xlsx"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, f.firma_adi FROM ogrenciler o join firmalar f on o.yerlesen_firma_id=f.id WHERE o.durum='Yerlestirildi'"
        df=pd.read_sql_query(sql, conn)
        df.to_excel(file_path, index=False)
        conn.close()
  
    def export_yerlesenler_csv(self,file_path="exported_yerlesenler.csv"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, f.firma_adi FROM ogrenciler o join firmalar f on o.yerlesen_firma_id=f.id WHERE o.durum='Yerlestirildi'"
        df=pd.read_sql_query(sql, conn)
        df.to_csv(file_path, index=False)
        conn.close()
    
    def export_yerlesenler_json(self,file_path="exported_yerlesenler.json"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, f.firma_adi FROM ogrenciler o join firmalar f on o.yerlesen_firma_id=f.id WHERE o.durum='Yerlestirildi'"
        df=pd.read_sql_query(sql, conn)
        df.to_json(file_path, orient='records', lines=True)
        conn.close()


    def export_yerlesemeyenler_excel(self,file_path="exported_yerlesemeyenler.xlsx"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, o.durum FROM ogrenciler o  WHERE o.durum='Yerlesemedi'"
        df=pd.read_sql_query(sql, conn)
        df.to_excel(file_path, index=False)
        conn.close()
  
    def export_yerlesemeyenler_csv(self,file_path="exported_yerlesemeyenler.csv"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, o.durum FROM ogrenciler o  WHERE o.durum='Yerlesemedi'"
        df=pd.read_sql_query(sql, conn)
        df.to_csv(file_path, index=False)
        conn.close()
    
    def export_yerlesemeyenler_json(self,file_path="exported_yerlesemeyenler.json"):
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, o.durum FROM ogrenciler o  WHERE o.durum='Yerlesemedi'"
        df=pd.read_sql_query(sql, conn)
        df.to_json(file_path, orient='records', lines=True)
        conn.close()
