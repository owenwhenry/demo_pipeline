
from generic import GenericCDGPipe

class billPipe(GenericCDGPipe):

    def __init__(self, logger=None) -> None:
        super().__init__(logger)

    def pull(self, congress = None, obj_type = None, obj_num = None):
        if congress:
            self._url_base += f"/bills/{congress}"
        if congress & obj_type:
            self._url_base += f"/bills/{congress}/{obj_type}"
        if obj_num & obj_type & congress:
            self._url_base += f"/bills/{congress}/{obj_type}/{obj_num}"

    def map(pull_obj):
        pass