from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name = db.Column(db.String(100),nullable=False) 
    #set relationship
    lgas = db.relationship("Lga", back_populates="state_deets")
    state_people = db.relationship("User", back_populates="mystate_deets")

class Lga(db.Model):
    lga_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    lga_name = db.Column(db.String(100),nullable=False)
    lga_stateid = db.Column(db.Integer, db.ForeignKey('state.state_id'))    
    #set relationships
    state_deets = db.relationship("State", back_populates="lgas")
    lga_people = db.relationship("User", back_populates="mylgadeets")
      
class User(db.Model):  
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fname = db.Column(db.String(100),nullable=False)
    user_lname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120),nullable=False) 
    user_password=db.Column(db.String(255),nullable=True)
    user_phone=db.Column(db.String(120),nullable=True) 
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)#default date
    #set the foreign key 
    user_levelid=db.Column(db.Integer, db.ForeignKey('level.level_id'))
    user_stateid=db.Column(db.Integer, db.ForeignKey('state.state_id')) 
    user_lgaid=db.Column(db.Integer, db.ForeignKey('lga.lga_id'))    
    #set relationships
    mystate_deets = db.relationship("State", back_populates="state_people")
    mylgadeets = db.relationship("Lga", back_populates="lga_people")
    myleveldeets = db.relationship("Level", back_populates="developers_inlevel")
 
class Level(db.Model):
    level_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    level_name = db.Column(db.String(100),nullable=False)
    #set relationship
    developers_inlevel = db.relationship("User", back_populates="myleveldeets")
    level_breakouts = db.relationship("Breakout", back_populates="breakleveldeets")
    
class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)

class Breakout(db.Model):
    break_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    break_title = db.Column(db.String(200),nullable=False)
    break_image = db.Column(db.String(120), nullable=True)    
    break_status = db.Column(db.Enum('1','0'),nullable=False)
    break_time = db.Column(db.DateTime(),default=datetime.utcnow)

    break_level = db.Column(db.Integer, db.ForeignKey('level.level_id'))

    breakleveldeets = db.relationship("Level", back_populates="level_breakouts")