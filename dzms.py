from pydantic import BaseModel, Field
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ware(BaseModel):
    id: int = Field(title="id", max_length=3)
    name: str = Field(title="name")
    description: str = Field(title="description")
    price: int = Field(title="price")

class OrderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("uid"))
    wid = db.Column(db.Integer, db.ForeignKey("wid"))
    description = db.Column(db.String)
    price = db.Column(db.String)

class Order(BaseModel):
    id: int = Field(title="id", max_length=3)
    uid: int = Field(title="uid", max_length=3)
    wid: int = Field(title="wid", max_length=3)
    date: str = Field(title="date")
    status: str = Field(title="status")

class User(BaseModel):
    id: int = Field(title="id", max_length=3)
    name: str = Field(title="name")
    surname: str = Field(title="surname")
    email: str = Field(title="email")
    password: str = Field(title="password")