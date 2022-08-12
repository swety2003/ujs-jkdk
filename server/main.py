import asyncio
import multiprocessing
import threading
from typing import Optional
import uvicorn
from fastapi import FastAPI,BackgroundTasks
import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from Models import *
from pydantic import BaseModel
from fastapi import FastAPI

from fastapi_login import LoginManager

from fastapi import Depends
from starlette.responses import Response, RedirectResponse

SECRET = 'your-secret-key'

manager = LoginManager(SECRET, token_url='/auth/token', use_header=True)
app = FastAPI()

dbfile = "db/users.db"


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user

@app.get("/")
def goHome():
    response = RedirectResponse(url="index.html")
    return response

@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/auth')
def auth(response: Response, user=Depends(manager)):
    token = manager.create_access_token(
        data=dict(sub=user.email)
    )
    manager.set_cookie(response, token)
    return response

# @app.get("/")
# async def root(user = Depends(manager)):
#     return {"message": "Hello World"}


@app.get("/users")
async def GetAllUsers(user = Depends(manager)):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    results=c.execute("select * from USERS")
    users=results.fetchall()
    conn.close()
    us=Users()
    for user in users:
        print(user)
        u=User(id=user[0],pwd=pwdMSK,recv=user[2],enabled=user[3],extrainfo=user[4])
        us.data.append(u)

    return us

@app.post("/users")
async def AddUser(friends:User,user = Depends(manager)):

    conn = sqlite3.connect(dbfile)
    c = conn.cursor()

    t=c.execute(F'''SELECT ID FROM USERS WHERE ID = {friends.id} LIMIT 1''')

    isNew= len(t.fetchall())==0
    if(isNew):
        print("Added an user")
        c.execute(F'''INSERT INTO USERS
        VALUES(?,?,?,?,?)''', (friends.id, friends.pwd, friends.recv, friends.enabled, friends.extrainfo))
        conn.commit()
    conn.close()
    return friends


@app.put("/users")
async  def EditUser(friends:User,user = Depends(manager)):


    conn = sqlite3.connect(dbfile)
    c= conn.cursor()

    if friends.pwd==pwdMSK:
        c.execute(F'''UPDATE USERS 
            SET RECV=? ,ENABLED=?,EXINFO=?
            WHERE ID=?;''', (friends.recv, friends.enabled, friends.extrainfo, friends.id))
        pass
    else:
        c.execute(F'''UPDATE USERS 
        SET PWD=?, RECV=? ,ENABLED=?,EXINFO=?
            WHERE ID=?;'''
                  , (friends.pwd, friends.recv, friends.enabled, friends.extrainfo, friends.id))
    conn.commit()
    conn.close()
    return friends

@app.delete("/users")
async def DelUser(id:int,user = Depends(manager)):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute(F'''DELETE FROM USERS
WHERE ID={id};''',)
    conn.commit()
    conn.close()
    return id


@app.get("/cfg")
async def GetCFG(user = Depends(manager)):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    results=c.execute("select * from CFG")
    cfg=results.fetchall()[0]
    conn.close()

    return Config(senderaddress=cfg[0],mailkey=pwdMSK,appid=cfg[2],apikey=pwdMSK,secretkey=pwdMSK)

@app.post("/cfg")
async def SetCFG(cfg:Config,user = Depends(manager)):
    print(cfg.json())
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    t=c.execute(F'''SELECT * FROM CFG LIMIT 1''')
    oldvalue=t.fetchall()
    isNew= len(oldvalue)==0
    if(isNew):
        print("新加")
        c.execute(F'''INSERT INTO CFG
        VALUES(?,?,?,?,?)''',(cfg.senderaddress,cfg.mailkey,cfg.appid,cfg.apikey,cfg.secretkey))
    else:
        print("修改")
        c.execute(F'''UPDATE CFG 
        SET SENDERADDR=?, MAILKEY=? ,APPID=? ,APIKEY=? ,SECRETKEY=? ;''',(cfg.senderaddress,
                            cfg.mailkey if cfg.mailkey!=pwdMSK else oldvalue[0][1],
                            cfg.appid,
                            cfg.apikey if cfg.apikey!=pwdMSK else oldvalue[0][3],
                            cfg.secretkey if cfg.secretkey!=pwdMSK else oldvalue[0][4]
                            ))
    conn.commit()
    conn.close()

    return cfg


from Core.Manager import *

@app.post("/start")
async def START(req:REQ,user = Depends(manager)):
    global th
    if not th.is_alive():
        th = threading.Thread(target=start, )
        th.setDaemon(True)
        th.start()
    if req.id!=None:
        threading.Thread(target=test,args=(req.id,)).start()

        print("Single run.")
        return

    glo.set_value("state", True)
    glo.set_value("targetTime",req.targetTime)
    # glo.set_value("targetTime",time.strftime('%M:%S',time.localtime(time.time())))

    pass

        # backgroundTask.add_task(start,lock,req,status)

        # start(lock,req,status)
        # t=threading.Thread(target=start,args=(lock,req,status,))
        # t.start()

@app.get("/stop")
def STOP(user = Depends(manager)):
    glo.set_value("state",False)
    pass

@app.get("/state")
def GetState(user = Depends(manager)):

    return State(state=get_value('state'),max=get_value("max"),
                 finished=get_value("finished"),
                 targetTime=get_value("targetTime"))

def startAPP():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    import GlobalData as glo




    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE USERS(
        ID      INT     NOT NULL,
        PWD     INT     NOT NULL,
        RECV    TEXT    NOT NULL,
        ENABLED INT     NOT NULL,
        EXINFO  INT     NOT NULL
        );
        ''')

    except Exception as e:
        print(e)
        pass

    try:
        print("Creating CFG.")
        c.execute('''CREATE TABLE CFG(
        SENDERADDR      TEXT     NOT NULL,
        MAILKEY         TEXT     NOT NULL,
        APPID           TEXT     NOT NULL,
        APIKEY          TEXT     NOT NULL,
        SECRETKEY       TEXT     NOT NULL
        );''')
    except Exception as e:
        print(e)
        pass

    pwdMSK = "禁止查看密码"

    import os

    pwd="admin";

    pwd=os.environ.get("ACCESS_KEY")

    fake_db = {'admin': {'password': pwd}}

    glo._init()

    glo.set_value("targetTime", "07:00")

    set_value("state",False)
    set_value("max",-1)
    set_value("finished",-1)

    th=threading.Thread(target=start,)
    th.setDaemon(True)
    th.start()

    app.mount("/", StaticFiles(directory="static"), name="static")
    startAPP()



# uvicorn main:app --reload