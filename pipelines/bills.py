
from pipelines.generic import GenericCDGPipe
from pipelines.connectors import congressDotGovClient
from database.models import Bill
from schemas import BillBase, BillExtended
import logging

logger = logging.getLogger(__name__)


class billPipe(GenericCDGPipe):

    def __init__(
            self, congress: int = None, 
            obj_type: str = None, 
            obj_num: str = None):
        super().__init__()
        logging.info(f"Set billPipe {congress}{obj_type}{obj_num}")
        print(f"billPipe {congress}{obj_type}{obj_num}")
        self._congress = congress
        self._obj_type = obj_type
        self._obj_num = obj_num
        self._url = ""

    @property
    def url(self):
        if self._obj_num and self._obj_type and self._congress:
            self._url = self._url_base + f"/bill/{self._congress}/{self._obj_type}/{self._obj_num}"
        elif self._congress and self._obj_type:
            self._url = self._url_base + f"/bill/{self._congress}/{self._obj_type}"
        elif self._congress:
            self._url = self._url_base + f"/bill/{self._congress}"
        else:
            self._url = self._url_base
        return self._url
    
    @property
    def data_root(self):
        if self._obj_num and self._obj_type and self._congress:
            self._data_root = 'bill'
        elif self._congress:
            self._data_root = "bills"
        else:
            raise Exception('Root not identified')
        return self._data_root

    def pull(self) -> dict:
        logging.debug(f'Set url to {self.url}')
        logging.debug(f'Set data root to {self.data_root}')
        if self.data_root == "bills":
            data = congressDotGovClient(url = self.url).paginate()
            for page in data:
                for item in page[self.data_root]:
                    logging.debug(f'Yielding {item}')
                    yield item
        elif self.data_root == 'bill':
            data = congressDotGovClient(url = self.url).get()
            logging.debug(f'Data found: {data[self.data_root]}')
            yield data[self.data_root]

    def validate(self, pull_obj) -> BillBase:
        logging.debug(f'Validating {pull_obj}')
        if self.data_root == 'bills':
            return BillBase.model_validate(pull_obj)
        elif self.data_root == 'bill':
            return BillExtended.model_validate(pull_obj)
        else:
            raise Exception("Data root not set, can't determine object type")
        
    def map(self, val_obj) -> Bill:
        logging.debug(f'Maping object {val_obj}')
        return Bill(
            congress = val_obj.congress,
            latest_action_date = val_obj.latestAction.actionDate,
            bill_num = val_obj.number,
            origin_chamber = val_obj.originChamber,
            origin_chamber_code = val_obj.originChamberCode,
            bill_type = val_obj.type,
            last_update_date = val_obj.updateDate,
            url = val_obj.url)
    
    def push(self, push_obj):
        self.session.add(push_obj)
