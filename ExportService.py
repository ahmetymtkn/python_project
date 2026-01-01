# Veritabanı verilerini Excel, CSV ve JSON formatlarında dışa aktaran modül
from connection import get_connection
import pandas as pd

class ExportService:
    # Veritabanı verilerini farklı formatlara aktarır
    
    def export_data_yerlesenler(self, file_path="yerlesenler.xlsx", format='excel'):
        # Yerleşen öğrencileri belirtilen formatta dışa aktarır
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, f.firma_adi, o.durum FROM ogrenciler o left join firmalar f on o.yerlesen_firma_id=f.id"
        df=pd.read_sql_query(sql, conn)
        if format=='excel':
            df.to_excel(file_path, index=False)
        elif format=='csv':
            df.to_csv(file_path, index=False)
        elif format=='json':
            df.to_json(file_path, orient='records', lines=True)
        conn.close()


    
    def export_data_yerlesemeyenler(self, file_path="yerlesemeyenler.xlsx", format='excel'):
        # Yerleşemeyen öğrencileri belirtilen formatta dışa aktarır
        conn = get_connection()
        sql="SELECT o.ogrenci_adi, o.ort, o.durum FROM ogrenciler o  WHERE o.durum='Yerlesemedi'"
        df=pd.read_sql_query(sql, conn)
        if format=='excel':
            df.to_excel(file_path, index=False)
        elif format=='csv':
            df.to_csv(file_path, index=False)
        elif format=='json':
            df.to_json(file_path, orient='records', lines=True)
        conn.close()
