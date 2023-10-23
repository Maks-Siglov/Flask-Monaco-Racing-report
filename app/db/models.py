from peewee import Model, CharField, IntegerField, ForeignKeyField, FloatField
from app.db.config import db


class BaseModel(Model):
    class Meta:
        database = db


class Driver(BaseModel):
    abr = CharField()
    name = CharField()
    team = CharField()


class Result(BaseModel):
    owner = ForeignKeyField(Driver, backref='lap_time')
    minutes = IntegerField()
    seconds = FloatField()
    position = IntegerField(null=True)

    @property
    def total_seconds(self):
        return round(self.minutes * 60 + self.seconds, 3)
