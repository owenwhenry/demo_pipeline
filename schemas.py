from pydantic import BaseModel
from datetime import date, datetime

class LatestAction(BaseModel):
    actionDate : date
    text : str

class BillBase(BaseModel):
    congress : int
    latestAction : LatestAction
    number : int
    originChamber : str
    originChamberCode : str
    type : str
    updateDate : date
    updateDateIncludingText : datetime
    url : str

class ListBase(BaseModel):
    count: int
    url : str

class CosponsorsList(ListBase):
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
    actions: ListBase
    #congress
    cosponsors : CosponsorsList
    introducedDate: date
    #latestAction
    #number
    #originChamber
    sponsors : list
    title : str
    titles : ListBase
    #type
    #updateDate
    #updateDateIncludingText
    request: dict






