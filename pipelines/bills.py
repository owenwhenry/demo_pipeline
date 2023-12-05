
from pipelines.generic import GenericCDGPipe
from pipelines.connectors import congressDotGovClient
from database.models import Bill
from schemas import BillBase
import logging

logger = logging.getLogger(__name__)


class billPipe(GenericCDGPipe):

    def __init__(
            self, congress=None, obj_type=None, obj_num=None):
        super().__init__()
        logging.info(f"billPipe {congress}{obj_type}{obj_num}")
        print(f"billPipe {congress}{obj_type}{obj_num}")
        self._congress = congress
        self._obj_type = obj_type
        self._obj_num = obj_num

    def pull(self):
        logging.debug('Pulling data.')
        if self._congress:
            self.url = self._url_base + f"/bill/{self._congress}"
            self.data_root = "bills"
        if self._congress and self._obj_type:
            self.url = self._url_base + f"/bill/{self._congress}/{self._obj_type}"
            self.data_root = 'bills'
        if self._obj_num and self._obj_type and self._congress:
            self._url_base += f"/bill/{self._congress}/{self._obj_type}/{self._obj_num}"
            self.data_root = 'bill'
        logging.debug(f'Set url to {self.url}')
        logging.debug(f'Set data root to {self.data_root}')
        data = congressDotGovClient(url = self.url).paginate()
        for page in data:
            for item in page[self.data_root]:
                logging.debug(f'Yielding {item}')
                yield item

    def validate(self, pull_obj):
        logging.debug(f'Validating {pull_obj}')
        return BillBase.model_validate(pull_obj)
        
    def map(self, val_obj):
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
