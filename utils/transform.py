import pandas as pd

def ubah_ke_dataframe(data):
    """
    Mengkonversi data mentah menjadi objek DataFrame.
    """
    return pd.DataFrame(data)

def bersihkan_dan_transformasi(data, kurs_dollar):
    """
    Melakukan pembersihan dan transformasi data secara menyeluruh.

    Langkah-langkah:
    1. Menghapus data tidak valid pada kolom Title, Price, dan Rating
    2. Menghapus duplikat dan nilai kosong
    3. Konversi:
       - Price: dari dolar ke rupiah
       - Rating: ke float
       - Colors: ke integer
       - Size & Gender: string
    4. Menambahkan kolom waktu (Timestamp jika belum ada)
    """
    try:
        # Filter data yang tidak valid
        data = data[~data['Title'].str.contains("Unknown Product", na=False, case=False)]
        data = data[~data['Price'].str.contains("Price Unavailable", na=False, case=False)]
        data = data[~data['Rating'].str.contains("Not Rated|Invalid Rating", na=False, case=False)]

        # Ambil angka dari Rating
        data['Rating'] = data['Rating'].str.extract(r'(\d+(?:\.\d+)?)')

        # Hilangkan baris duplikat dan kosong
        data = data.drop_duplicates()
        data = data.dropna()

        # Konversi tipe data
        data['Title'] = data['Title'].astype("string")

        # Hapus simbol dolar dan konversi ke rupiah
        data["Harga_Dollar"] = data["Price"].str.replace(r'[\$,]', '', regex=True).astype(float)
        data["Harga_Rupiah"] = (data["Harga_Dollar"] * kurs_dollar).astype(float)

        # Buang kolom lama dan ubah nama kolom harga
        data.drop(columns=["Price", "Harga_Dollar"], inplace=True)
        data.rename(columns={"Harga_Rupiah": "Price"}, inplace=True)

        # Konversi tipe lainnya
        data['Colors'] = data['Colors'].astype(int)
        data['Rating'] = data['Rating'].astype(float)

        # Susun ulang kolom
        urutan_kolom = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"]
        data = data[urutan_kolom]

        return data

    except Exception as err:
        print("Gagal memproses data fashion:", err)
        return None
