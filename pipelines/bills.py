
from pipelines.generic import GenericCDGPipe
from pipelines.connectors import congressDotGovClient
from database.models import Bill
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
        if self._congress:
            self._url_base += f"/bills/{self._congress}"
            self._data_root = "bills"
        if self._congress & self._obj_type:
            self._url_base += f"/bills/{self._congress}/{self._obj_type}"
            self._data_root = 'bills'
        if self._obj_num & self._obj_type & self._congress:
            self._url_base += f"/bills/{self._congress}/{self._obj_type}/{self._obj_num}"
            self._data_root = 'bill'
        data = congressDotGovClient(url = self._url_base).paginate()
        for item in data[self._data_root]:
            yield item
        
    def map(pull_obj):
        return Bill(
            congress = pull_obj.congress,
            latest_action_date = pull_obj.latestAction.actionDate,
            bill_num = pull_obj.number,
            origin_chamber = pull_obj.originChamber,
            origin_chamber_code = pull_obj.originChamberCode,
            bill_type = pull_obj.type,
            last_update_date = pull_obj.updateDate,
            url = pull_obj.url)
    
    def push(self, push_obj):
        self.session.add(push_obj)
