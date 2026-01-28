import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest import mock, TestCase
from unittest.mock import patch
from bs4 import BeautifulSoup
from utils.extract import ambil_konten, ekstraksi_data_produk, jalankan_scraping

class TestExtract(TestCase):

    @patch('utils.extract.requests.Session')
    def test_fetching_content_success(self, mock_session):
        mock_response = mock.Mock()
        mock_response.content = b'<html><body><p>Tests</p></body></html>'
        mock_response.status_code = 200
        mock_response.raise_for_status = mock.Mock()
        mock_session.return_value.__enter__.return_value.get.return_value = mock_response

        result = ambil_konten("https://example.com")

        self.assertIsNotNone(result)
        self.assertIn("Tests", result.text)

    @patch('utils.extract.requests.Session')
    def test_fetching_content_failure(self, mock_session):
        mock_response = mock.Mock()
        mock_response.content = b''
        mock_response.raise_for_status.side_effect = Exception("error")
        mock_session.return_value.__enter__.return_value.get.return_value = mock_response

        result = ambil_konten("https://example.com")
        self.assertIsNone(result)

    def test_extract_fashion_data_success(self):
        html = '''
        <div class='product-details'>
            <h3>Cool Shirt</h3>
            <div class='price-container'><span class='price'>$19.99</span></div>
            <p>Gender: Unisex</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Rating: 4.5</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div')
        result = ekstraksi_data_produk(div)
        self.assertEqual(result['Title'], 'Cool Shirt')
        self.assertEqual(result['Price'], '$19.99')
        self.assertEqual(result['Gender'], 'Unisex')
        self.assertEqual(result['Colors'], '3')
        self.assertEqual(result['Size'], 'M')
        self.assertEqual(result['Rating'], '4.5')

    def test_extract_fashion_data_failure(self):
        result = ekstraksi_data_produk(None)
        self.assertIsNone(result)

    @patch('utils.extract.ambil_konten')
    def test_scrape_fashion_success(self, mock_fetching_content):
        html_page1 = '''
        <div class='product-details'>
            <h3>Cool Shirt</h3>
            <div class='price-container'><span class='price'>$19.99</span></div>
            <p>Gender: Unisex</p>
            <p>Colors: Blue, Red</p>
            <p>Size: M</p>
            <p>Rating: 4.5</p>
        </div>
        <li class='page-item next'></li>
        '''
        html_page2 = '''
        <div class='product-details'>
            <h3>Cool Pants</h3>
            <div class='price-container'><span class='price'>$29.99</span></div>
            <p>Gender: Male</p>
            <p>Colors: Black</p>
            <p>Size: L</p>
            <p>Rating: 4.0</p>
        </div>
        '''

        soup1 = BeautifulSoup(html_page1, 'html.parser')
        soup2 = BeautifulSoup(html_page2, 'html.parser')

        mock_fetching_content.side_effect = [soup1, soup2, None]

        data = jalankan_scraping('https://example.com/{}', delay=0)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Title'], 'Cool Shirt')
        self.assertEqual(data[1]['Title'], 'Cool Pants')

    @patch('utils.extract.ambil_konten')
    def test_scrape_fashion_failure(self, mock_fetching_content):
        mock_fetching_content.side_effect = Exception("Scraping failed")
        with self.assertRaises(Exception):
            jalankan_scraping('https://example.com/{}')

if __name__ == '__main__':
    unittest.main()
