import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from utils.transform import ubah_ke_dataframe, bersihkan_dan_transformasi

class TestTransform(unittest.TestCase):

    def setUp(self):
        self.data = [
            {
                "Title": "Stylish Shirt",
                "Price": "$25",
                "Rating": "4.2",
                "Colors": "2",
                "Size": "M",
                "Gender": "Female",
                "Timestamp": "2025-05-10 18:30:00"
            },
            {
                "Title": "Cool Jacket",
                "Price": "$30",
                "Rating": "4.8",
                "Colors": "3",
                "Size": "L",
                "Gender": "Male",
                "Timestamp": "2025-05-10 18:35:00"
            }
        ]
        self.df = ubah_ke_dataframe(self.data)

    def test_transformasi(self):
        hasil = bersihkan_dan_transformasi(self.df, kurs_dollar=16000)
        self.assertIsNotNone(hasil)
        self.assertIn("Price", hasil.columns)
        self.assertAlmostEqual(hasil.iloc[0]["Price"], 400000.0)  # 25 * 16000

if __name__ == '__main__':
    unittest.main()
