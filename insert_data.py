import os
import scrape
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import time
import helper

# Load env variables
load_dotenv()

engine = create_engine(os.environ['MARIADB_ADDRESS'],echo=True)
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"
    rgno = Column(String(length=10),primary_key = True)
    season = Column(Text)
    ay = Column(Text)
    course_no = Column(Text)
    old_cno = Column(Text)
    lang = Column(Text)
    section = Column(Text)
    title_e = Column(Text)
    title_j = Column(Text)
    schedule = Column(Text)
    room = Column(Text)
    comment = Column(Text)
    maxnum = Column(Text)
    instructor = Column(Text)
    unit = Column(Text)

Base.metadata.drop_all(bind=engine, tables=[Course.__table__])
Base.metadata.create_all(engine)

SessionClass = sessionmaker(engine)
session = SessionClass()

courses_list = helper.getCourseInfo()

course_object_list = []
for i in courses_list:
    obj = Course(rgno = i['rgno'],season = i['season'],ay = i['ay'],course_no = i['course_no'],old_cno = i['old_cno'],lang = i['lang'],section = i['section'],title_e = i['title_e'],title_j = i['title_j'],schedule = i['schedule'],room = i['room'],comment = i['comment'],maxnum = i['maxnum'],instructor = i['instructor'],unit = i['unit'])
    course_object_list.append(obj)

print(course_object_list)
session.bulk_save_objects(course_object_list)

session.commit()
