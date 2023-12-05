import logging
from database.definition import SessionLocal, ENGINE

class GenericPipe():
    '''
    Place to put some common code that'll be used for most pipes and define
    a common structure
    '''

    def __init__(self, session = None) -> None:
        self.session = session or SessionLocal()

    def pull():
        raise NotImplementedError

    def map(pull_obj):
        raise NotImplementedError

    def push(push_obj):
        raise NotImplementedError
    
    def run(self):
        logging.debug("Running pipe!")
        try:
            for pull_item in self.pull():
                push_item = self.map(pull_item)
                self.push(push_item)
            self.session.commit()
        finally:
            self.session.close()
    
class GenericCDGPipe(GenericPipe):

    def __init__(self, logger=None) -> None:
        super().__init__(logger)
        self._url_base = "api.congress.gov/v3"