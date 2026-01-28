import time
import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/{}"
MAX_PAGES = 50
TARGET_DATA = 1000
JEDA_WAKTU = 2  # detik


def ambil_konten(url):
    try:
        with requests.Session() as session:
            response = session.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil konten: {e}")
        return None


def ekstraksi_data_produk(container):
    if container is None:
        return None

    try:
        title_tag = container.find("h3")
        title = title_tag.text.strip() if title_tag else "Tidak diketahui"

        harga = container.find("div", class_="price-container")
        if harga:
            span_harga = harga.find("span", class_="price")
            price = span_harga.text.strip() if span_harga else "Tidak diketahui"
        else:
            paragraf_harga = container.find("p", class_="price")
            price = paragraf_harga.text.strip() if paragraf_harga else "Tidak diketahui"

        info_list = container.find_all("p")
        gender = rating = colors = size = ""

        for item in info_list:
            teks = item.text
            if "Gender" in teks:
                gender = teks.split()[-1]
            elif "Colors" in teks:
                colors = teks.split()[0][0]
            elif "Size" in teks:
                size = teks.split()[-1]
            elif "Rating" in teks:
                rating = teks.replace("Rating:", "").strip()

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as err:
        print(f"❌ Kesalahan saat ekstraksi data produk: {err}")
        return None


def jalankan_scraping(url_template=BASE_URL, delay=JEDA_WAKTU):
    hasil_scrape = []
    halaman = 1

    while halaman <= MAX_PAGES and len(hasil_scrape) < TARGET_DATA:
        url = url_template.format("" if halaman == 1 else f"page{halaman}")
        print(f"🔎 Mengakses halaman: {url}")

        konten = ambil_konten(url)
        if not konten:
            break

        produk_list = konten.find_all("div", class_="product-details")

        for produk in produk_list:
            data = ekstraksi_data_produk(produk)
            if data:
                hasil_scrape.append(data)

        tombol_selanjutnya = konten.find("li", class_="page-item next")
        if tombol_selanjutnya:
            halaman += 1
            time.sleep(delay)
        else:
            break

    print(f"✅ Total data yang berhasil dikumpulkan: {len(hasil_scrape)}")
    return hasil_scrape
