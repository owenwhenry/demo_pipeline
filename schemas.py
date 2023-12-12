from pydantic import BaseModel
from typing import Dict, Optional
from datetime import date, datetime

class LatestAction(BaseModel):
    actionDate : date
    text : str

class BillBase(BaseModel):
    congress : int
    latestAction : LatestAction
    number : int
    originChamber : str
    originChamberCode : Optional[str] = None
    type : str
    updateDate : date
    updateDateIncludingText : datetime
    url : Optional[str] = None

class DictBase(BaseModel):
    count: int
    url : str

class CosponsorsList(DictBase):
    countIncludingWithdrawnCosponsors : int

class MemberBase(BaseModel):
    bioguideId : str
    firstName : str
    fullName : str
    lastName : str
    party : str
    state : str
    url: str

class BillExtended(BillBase):
    actions: DictBase
    #congress
    cosponsors : CosponsorsList
    introducedDate: date
    #latestAction
    #number
    #originChamber
    sponsors : list
    title : str
    titles : DictBase
    #type
    updateDate : datetime
    #updateDateIncludingText






