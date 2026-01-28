import time
import pandas as pd

from utils.transform import bersihkan_dan_transformasi, ubah_ke_dataframe
from utils.load import simpan_ke_postgresql, simpan_ke_csv, simpan_ke_google_sheet
from utils.extract import jalankan_scraping

def main():
    """
    Proses utama: scraping, transformasi, dan penyimpanan data fashion.
    """
    try:
        # 1. Ambil data dari website
        data_mentah = jalankan_scraping()

        if data_mentah:
            # 2. Ubah ke DataFrame
            df = ubah_ke_dataframe(data_mentah)

            # 3. Transformasi data
            kurs_dollar = 16000  # Sesuaikan dengan nilai tukar saat ini
            df_bersih = bersihkan_dan_transformasi(df, kurs_dollar)

            if df_bersih is not None:
                # 4. Simpan ke tiga tujuan
                simpan_ke_csv(df_bersih)
                simpan_ke_postgresql(df_bersih)
                simpan_ke_google_sheet(df_bersih)
        else:
            print("❌ Data kosong, proses dihentikan.")

    except Exception as e:
        print(f"❌ Terjadi kesalahan dalam proses utama: {e}")

if __name__ == "__main__":
    main()
