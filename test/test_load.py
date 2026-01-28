import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import simpan_ke_csv, simpan_ke_postgresql, simpan_ke_google_sheet

class TestLoad(unittest.TestCase):

    @patch('pandas.DataFrame.to_csv')
    def test_simpan_ke_csv(self, mock_to_csv):
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        simpan_ke_csv(df)
        mock_to_csv.assert_called_once_with("data_fashions.csv", index=False)

    @patch('pandas.DataFrame.to_sql')
    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql(self, mock_create_engine, mock_to_sql):
        # Mock objek engine dan koneksi
        mock_engine = MagicMock()
        mock_connect = mock_engine.connect.return_value.__enter__.return_value
        mock_create_engine.return_value = mock_engine

        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        simpan_ke_postgresql(df)

        mock_create_engine.assert_called_once()
        mock_to_sql.assert_called_once_with(
            name='fashionstudio',
            con=mock_connect,
            if_exists='append',
            index=False
        )

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_simpan_ke_google_sheet(self, mock_credentials, mock_build):
        # Setup mock credentials dan service
        mock_credential_instance = mock.Mock()
        mock_credentials.return_value = mock_credential_instance

        mock_service = mock.Mock()
        mock_build.return_value = mock_service
        mock_sheet = mock_service.spreadsheets.return_value
        mock_values = mock_sheet.values.return_value
        mock_values.update.return_value.execute.return_value = {}

        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        simpan_ke_google_sheet(df)

        mock_credentials.assert_called_once()
        mock_build.assert_called_once()
        mock_values.update.assert_called_once()
