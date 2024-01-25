from app import db
from flask_login import UserMixin
from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship


# personal details about user, their postcode, energy provider
class User(UserMixin, db.Model):
    __tablename__ = "userInfo"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(45))
    email = Column(String(45), unique=True)
    passwordHash = Column(String(128))
    dateCreated = Column(DateTime())
    postcode = Column(String(45))
    provider= Column(String(45))
    energyTarget = Column(Float(), default=0.0)
    emissionTarget = Column(Float(), default=0.0)
    costTarget = Column(Float(), default=0.0)

    # one to many relationship
    appliances = relationship("Appliance", backref="User", lazy="dynamic")
    usage = relationship("Usage", backref="User", lazy="dynamic")
    energyProvider = relationship("Provider", backref="User", lazy="dynamic")

    __table_args__ = (UniqueConstraint('email', name='unique_email_constraint'),)

    def __repr__(self):
        return self.name

    # get id for log in
    def get_id(self):
        return self.id

# details about appliance & their usage per email Id
class Appliance(db.Model):
    __tablename__ = "applianceInfo"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    email = Column(String(45), ForeignKey("userInfo.email"))
    applianceName = Column(String(45))
    powerRating = Column(Integer())
    hoursPerDay = Column(Integer())
    dateUsedOn = Column(Date()) # this is in seconds now
    energyUsed = Column(Float())
    cost = Column(Float())
    emissions = Column(Float())
    

# details about provider and their tariffs(to be entered into the database by programmers)
# user while logging in can have a few choices to choose from
class Provider(db.Model):
    __tablename__ = "energyProviderInfo"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    energyProvider = Column(String(45), ForeignKey("userInfo.id"))
    tariff = Column(Float())


# energy,cost,CO2 emissions per email id
class Usage(db.Model):
    __tablename__ = "usageInfo"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    email = Column(String(45), ForeignKey("userInfo.email"))
    energyConsumed = Column(Float())
    cost = Column(Float())
    carbonEmissions = Column(Float())

# Text prompts used by the dynamic cards in goal tracking. 
class Prompt(db.Model):
    __tablename__ = "promptInfo"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    message = Column(String(120))
