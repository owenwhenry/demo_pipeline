from unittest import mock
import json

class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

def mocked_requests_get(*args, **kwargs):
    if args[0] == 'https://api.congress.gov/v3/bill/118/sres/475':
        return mockConstructor('tests/json/example_bill.json', 200)
    elif args[0] == 'https://api.congress.gov/v3/bill/116/sjres':
        return mockConstructor('tests/json/example_bills_p1.json', 200)
    elif args[0] == 'https://api.congress.gov/v3/bill/116/sjres?offset=20&limit=20&format=json':
        return mockConstructor('tests/json/example_bills_p2.json', 200)
    elif args[0] == 'https://api.congress.gov/v3/bill/116/sjres?offset=40&limit=20&format=json':
        return mockConstructor('tests/json/example_bills_p3.json', 200)
    elif args[0] == 'https://api.congress.gov/v3/bill/116/sjres?offset=60&limit=20&format=json':
        return mockConstructor('tests/json/example_bills_p4.json', 200)
    elif args[0] == 'https://api.congress.gov/v3/bill/116/sjres?offset=80&limit=20&format=json':
        return mockConstructor('tests/json/example_bills_p5.json', 200)
    return MockResponse(None, 404)

def mockConstructor(filename: str, status: int):
     with open(filename) as f:
          data = json.load(f)
          return MockResponse(data, status)