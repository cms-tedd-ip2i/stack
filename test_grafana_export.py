import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import the script logic
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, 'grafana'))
from export_dashboards import get_request

class TestGrafanaExport(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_get_request_success(self, mock_urlopen):
        # Mocking a successful API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "success", "data": []}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        result = get_request("http://localhost:3001/api/search")
        
        self.assertEqual(result['status'], 'success')
        mock_urlopen.assert_called_once()

    def test_output_dir_setup(self):
        from export_dashboards import OUTPUT_DIR
        self.assertTrue(OUTPUT_DIR.endswith('grafana/dashboards'))

if __name__ == '__main__':
    unittest.main()