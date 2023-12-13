import unittest
from unittest.mock import Mock, patch

from pipelines.connectors import congressDotGovClient

class test_congressDotGovClient(unittest.TestCase):

    def setUp(self):
        self.cdg_client = congressDotGovClient("something.com")
        self.response_mock = Mock()
        self.response_mock.status_code = 200
        self.response_mock.json.return_value = {"key" : "value"}

    @patch('pipelines.connectors.req')
    def test_mock_good_call(self, mock_requests):
        mock_requests.get.return_value = self.response_mock
        assert self.cdg_client.call("https://some.data").status_code == 200
        
    @patch('pipelines.connectors.req')
    def test_mock_good_get(self, mock_requests):
        mock_requests.get.return_value = self.response_mock
        assert self.cdg_client.get() == {"key" : "value"}
        assert self.cdg_client._url == "something.com"