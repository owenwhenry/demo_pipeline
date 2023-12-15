import unittest
from pipelines.bills import billPipe
from unittest.mock import patch
from mocks import mocked_requests_get
import json

class test_bills(unittest.TestCase):

    def setUp(self):
        self.pipe_congress = billPipe(116)
        self.pipe_cong_type = billPipe(116, 'sjres')
        self.pipe_cong_type_num = billPipe(118, "sres", 475)
    
    def test_url(self):
        assert self.pipe_congress.url == "https://api.congress.gov/v3/bill/116"
        assert self.pipe_cong_type.url == "https://api.congress.gov/v3/bill/116/sjres"
        assert self.pipe_cong_type_num.url == "https://api.congress.gov/v3/bill/118/sres/475"
    
    def test_data_root(self):
        assert self.pipe_congress.data_root == "bills"
        assert self.pipe_cong_type.data_root == "bills"
        assert self.pipe_cong_type_num.data_root == "bill"
    
    patch('pipelines.connectors.req', side_effect=mocked_requests_get)
    def test_pull_pages(self):
        count = 0
        for item in self.pipe_cong_type.pull():
            count += 1
        assert count == 82

    patch('pipelines.connectors.req', side_effect=mocked_requests_get)
    def test_pull_page(self):
        count = 0
        with open('tests/json/example_bill.json') as f:
            for item in self.pipe_cong_type_num.pull():
                count =+ 1
                assert item == json.load(f)['bill']
        assert count == 1

