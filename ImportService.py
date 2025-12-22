from connection import get_connection
import pandas as pd

class ImportService:
    def import_excel_firmalar(self,file_path="firmalar.xlsx"):
        conn = get_connection()
        df=pd.read_excel(file_path)
        df['kalan_kontenjan'] = df['kontenjan']  # kalan_kontenjan = kontenjan
        df.to_sql('firmalar',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()
  
    def import_excel_ogrenciler(self,file_path="ogrenciler.xlsx"):
        conn = get_connection()
        df=pd.read_excel(file_path)
        df.to_sql('ogrenciler',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()
    
    def import_csv_firmalar(self,file_path="firmalar.csv"):
        conn = get_connection()
        df=pd.read_csv(file_path)
        df['kalan_kontenjan'] = df['kontenjan']  # kalan_kontenjan = kontenjan
        df.to_sql('firmalar',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()

    def import_csv_ogrenciler(self,file_path="ogrenciler.csv"):
        conn = get_connection()
        df=pd.read_csv(file_path)
        df.to_sql('ogrenciler',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()

    def import_json_firmalar(self,file_path="firmalar.json"):
        conn = get_connection()
        df=pd.read_json(file_path)
        df['kalan_kontenjan'] = df['kontenjan']
        df.to_sql('firmalar',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()

    def import_json_ogrenciler(self,file_path="ogrenciler.json"):
        conn = get_connection()
        df=pd.read_json(file_path)
        df.to_sql('ogrenciler',conn,if_exists='replace',index=False)
        conn.commit()
        conn.close()
    
  