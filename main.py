import logging
import requests as req
from keys import API_KEY
import os
import schemas, models
from database import SessionLocal, ENGINE

#from google.cloud import pubsub_v1

models.Base.metadata.create_all(bind=ENGINE)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class APIClient():

    def __init__(self, url=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._url = url
        self._api_key = API_KEY
        self.params = {'api_key': self._api_key}
    
    def get(self, target_url=None):
        """
        Method for fetching data from the API and returning it as JSON.

        If you want the full request object, try call() instead.
        """
        object_raw = self.call(target_url) if target_url else self.call(self._url)
        object_json = object_raw.json()
        return object_json
    
    def call(self, url):
        """
        Makes an API call and returns the full request object.

        Raises errors if a non-200 status is returned
        """
        self.logger.info('Making call with %s' % url)
        data = req.get(url, params=self.params)
        self.status_code = data.status_code
        self.logger.info('Call made, returning response')
        if data.status_code != 200:
            self.logger.warning('Call returned non-200'
                                ' status of %s' % data.status_code)
        return data

    def paginate(self):
        """
        Generator that makes the initial call to a URL then paginates through
        the rest of the results.

        Returns the entire response, one page at a time then clears the params.
        """
        target_url = self._url
        while target_url:
            self.logger.info('Getting data')
            data = self.get(target_url)
            yield data
            if 'next' in data['pagination'].keys():
                self.logger.info('Heading to next page')
                target_url = data['pagination']['next']
            else:
                self.logger.debug('No more target_url, finishing pagination')
                target_url = None


def map_pyd_to_sqlalch(pyd_model_type : str, pyd_data):
    if pyd_model_type == 'bill':
        return models.Bill(
            congress = pyd_data.congress,
            latest_action_date = pyd_data.latestAction.actionDate,
            bill_num = pyd_data.number,
            origin_chamber = pyd_data.originChamber,
            origin_chamber_code = pyd_data.originChamberCode,
            bill_type = pyd_data.type,
            last_update_date = pyd_data.updateDate,
            url = pyd_data.url)


if __name__ == "__main__":
    client = APIClient(url='https://api.data.gov/congress/v3/bill/118/sjres')
    session = SessionLocal()
    for data in client.paginate():
        for item in data['bills']:
            #print(item)
            pydantic_bill = schemas.BillBase.model_validate(item)
            sqlalch_bill = map_pyd_to_sqlalch('bill', pydantic_bill)
            #print(sqlalch_bill.__dict__)
            session.add(sqlalch_bill)
        session.commit()
        print(session.query(models.Bill).count())
        session.close()
