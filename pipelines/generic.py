import logging

class GenericPipe():
    '''
    Place to put some common code that'll be used for most pipes and define
    a common structure
    '''

    def __init__(self, logger = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def pull():
        raise NotImplementedError

    def map(pull_obj):
        raise NotImplementedError

    def push():
        raise NotImplementedError
    
    def run(self):
        for pull_item in self.pull():
            push_item = self.map(pull_item)
            self.push(push_item)
        raise NotImplementedError
    
class GenericCDGPipe(GenericPipe):

    def __init__(self, logger=None) -> None:
        super().__init__(logger)
        self._url_base = "api.congress.gov/v3"