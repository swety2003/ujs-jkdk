from pydantic import BaseModel


class User(BaseModel):
    id: int
    pwd: str
    recv: str
    enabled : bool = False
    extrainfo: str = "无信息"

class Users(BaseModel):
    data: list[User] =[]

class Config(BaseModel):
    senderaddress:str
    mailkey:str
    appid:str
    apikey:str
    secretkey:str

class REQ(BaseModel):
    id:int=None
    targetTime:str="07:00"


class State(BaseModel):
    state:bool=False
    max:int=0
    finished:int=0
    targetTime:str="07:00"