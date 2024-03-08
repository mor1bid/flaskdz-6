import databases, sqlalchemy
from fastapi import FastAPI
from datetime import date
from dzms import *
from faker import Faker
import random

app = FastAPI()

DATABASE_URL = "sqlite:///templates/my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
fake = Faker()

wares = sqlalchemy.Table(
    "wares",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.String)
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("uid", sqlalchemy.String),
    sqlalchemy.Column("wid", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.String)
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=User)
async def createuser(user: User):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    query = users.insert().values(**users.dict())
    lastid = await database.execute(query)
    return {**users.dict(), "id": lastid}

@app.get("/fakers/{count}")
async def create_note(count: int):
    for i in range(count):
        fname = fake.first_name()
        fsur = fake.last_name()
        fmail = fake.unique.email()
        fword = fake.unique.password()
        query = wares.insert().values(name=fname, surname=fsur, email=fmail, password=fword)
        await database.execute(query)
    return {'message': f'{count} fake users create'}

@app.post("/wares/", response_model=Ware)
async def createuser(ware: Ware):
    query = wares.insert().values(name=ware.name, description=ware.description, price=ware.price)
    query = wares.insert().values(**wares.dict())
    lastid = await database.execute(query)
    return {**wares.dict(), "id": lastid}

@app.get("/fares/{count}")
async def create_note(count: int):
    wares = {
        1: "Продовольствие",
        2: "Медикаменты",
        3: "Техника",
        4: "Роскошь",
        5: "Минералы",
        6: "Алкоголь",
        7: "Оружие",
        2: "Наркотики",
    }
    for i in range(count):
        fname = wares[i]
        fdesc = "A qualified ware. Buy it."
        fprice = random.randint(0, 500)
        # lastid = await database.execute(query)
        query = wares.insert().values(name=fname, description=fdesc, price=fprice)
        await database.execute(query)
    return {'message': f'{count} fake users create'}

@app.post("/orders/", response_model=Order)
async def createuser(order: Order):
    query = orders.insert().values(uid=order.uid, wid=order.wid, date=order.date, status=order.status)
    query = orders.insert().values(**orders.dict())
    lastid = await database.execute(query)
    return {**orders.dict(), "id": lastid}