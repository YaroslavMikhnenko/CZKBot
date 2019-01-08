import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool


APP_ROOT = os.path.abspath(os.path.pardir)

engine = create_engine('sqlite:///' + os.path.join(APP_ROOT, 'db/development.sqlite3'),
						connect_args={'check_same_thread':False},
                    	poolclass=StaticPool)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Answer(Base):
	__tablename__ = 'answers'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	question_id = Column(Integer)
	text = Column(String(255))
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Question(Base):
	__tablename__ = 'questions'
	id = Column(Integer, primary_key=True)
	text = Column(String(255))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    stage = Column(Integer)
