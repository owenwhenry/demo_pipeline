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
    
    def validate(pull_obj):
        raise NotImplementedError

    def map(val_obj):
        raise NotImplementedError

    def push(push_obj):
        raise NotImplementedError
    
    def run(self):
        logging.info("Running pipe!")
        try:
            for pull_item in self.pull():
                logging.info("Trying validation")
                val_item = self.validate(pull_item)
                logging.info("Trying to map")
                push_item = self.map(val_item)
                logging.info("Trying to push")
                self.push(push_item)
            logging.info("Finished, committing.")
            self.session.commit()
        finally:
            self.session.close()
    
class GenericCDGPipe(GenericPipe):

    def __init__(self, logger=None):
        super().__init__(logger)
        self._url_base = "https://api.congress.gov/v3"