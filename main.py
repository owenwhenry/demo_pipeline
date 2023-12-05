"""
This is a demo docstring for a demo pipeline!

Goal here is to keep main.py as the central "control panel" for any like pipes. 

Practices borrowed from Guido Van Rossum's suggestions for main: 
https://www.artima.com/weblogs/viewpost.jsp?thread=4829
"""

#Generic iumports
import logging
import logging.config
import os
import sys
import getopt

#Project-specific imports
import schemas, database.models as models
from database.definition import SessionLocal, ENGINE
import pipelines.bills

#from google.cloud import pubsub_v1

models.Base.metadata.create_all(bind=ENGINE)

'''
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

def test_run():
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
'''

def process(arg, congress, type, number):
    '''
    This is the thing that maps arguments on to ensuing modules!
    '''
    try:
        logging.debug(f'Processing arg {arg}')
        if arg == 'bills':
            logging.debug('Found bill arg')
            pipe = pipelines.bills.billPipe(congress=congress, obj_type=type, 
                                     obj_num=number)
            pipe.run()
    except:
        pass
    else:
        pass

def main(argv = None):
    # start logger
    logging.config.fileConfig("logging.conf")
    congress = None
    otype = None
    num = None
    if argv is None:
        argv = sys.argv
    try:
        logging.info('Starting run')
        opts, args = getopt.getopt(
            argv[1:], "h:c:t:n:", ["help", 
                                       "--congress = ",
                                       "--type = ",
                                       "--number = ",
                                     ]
            )
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
  
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        if o in ("-c", "--congress"):
            congress = a
        if o in ("-t", "--type"):
            otype = a
        if o in ("-n", "--number"):
            num = a
    
    # process arguments
    for arg in args:
        if arg in ['bills']:
            process(arg, congress, otype, num) # process() is defined elsewhere
        else:
            raise Exception("argument %s not recognized"%arg)

if __name__ == "__main__":
    main()
    
