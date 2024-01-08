import os
import scrape
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, JSON
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import time
import helper
from tqdm import tqdm

# Load env variables
load_dotenv()

engine = create_engine(os.environ['MARIADB_ADDRESS'],echo=True)
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"
    __table_args__ = {
        'mariadb_ENGINE': 'mroonga',
        'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    rgno = Column(Integer,primary_key = True)
    season = Column(Text)
    ay = Column(Text)
    course_no = Column(Text)
    old_cno = Column(Text)
    lang = Column(Text)
    section = Column(Text)
    title_e = Column(Text)
    title_j = Column(Text)
    schedule = Column(Text)
    schedule_meta = Column(JSON)
    room = Column(Text)
    comment = Column(Text)
    maxnum = Column(Text)
    instructor = Column(Text)
    unit = Column(Text)
    syllabus = relationship('Syllabus', back_populates='courses')

class Syllabus(Base):
    __tablename__ ="syllabi"
    __table_args__ = {
        'mariadb_ENGINE': 'mroonga',
        'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    rgno = Column(Integer, primary_key=True)
    ay = Column(String(length=5))
    term = Column(String(length=100))
    cno = Column(String(length=100))
    title_e = Column(String(length=300))
    title_j = Column(String(length=300))
    lang = Column(String(length=300))
    instructor = Column(String(length=100))
    unit_e = Column(String(length=100))
    koma_lecture_e = Column(String(length=10))
    koma_seminar_e = Column(String(length=10))
    koma_labo_e = Column(String(length=10))
    koma_act_e = Column(String(length=10))
    koma_int_e = Column(String(length=10))
    descreption = Column(Text)
    descreption_j = Column(Text)
    goals = Column(Text)
    goals_j = Column(Text)
    content = Column(Text)
    content_j = Column(Text)
    lang_of_inst = Column(Text)
    pollicy = Column(Text)
    individual_study = Column(Text)
    ref = Column(Text)
    notes = Column(Text)
    schedule = Column(String(length=500))
    url = Column(String(length=300))
    course_rgno = Column(Integer, ForeignKey('courses.rgno'))
    courses = relationship('Course', back_populates='syllabus')



# Base.metadata.drop_all(bind=engine, tables=[Course.__table__])
# Base.metadata.drop_all(bind=engine, tables=[Syllabus.__table__])
Base.metadata.create_all(engine)

SessionClass = sessionmaker(engine)
session = SessionClass()

courses_list = helper.getCourseInfo()

course_object_list = []
for i in courses_list:
    obj = Course(rgno = int(i['rgno']),season = i['season'],ay = i['ay'],course_no = i['course_no'],old_cno = i['old_cno'],lang = i['lang'],section = i['section'],title_e = i['title_e'],title_j = i['title_j'],schedule = i['schedule'],schedule_meta = i['schedule_meta'],room = i['room'],comment = i['comment'],maxnum = i['maxnum'],instructor = i['instructor'],unit = i['unit'])
    course_object_list.append(obj)

session.bulk_save_objects(course_object_list)

session.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

syllabus_flag = True 

if syllabus_flag == True:
    rgno_list = []
    for i in session.query(Course.rgno).all():
        rgno_list.append(i[0])
    

    syllabus_data = scrape.getSyllabus('2023',rgno_list)
    for f in tqdm(range(len(syllabus_data))):
        x = syllabus_data[f]
        newCourse = Syllabus(rgno=int(x['rgno']),ay=x['ay'],term=x['term'],cno=x['cno'],title_e=x['title_e'],title_j=x['title_j'],lang=x['lang'],instructor=x['instructor'],unit_e=x['unit_e'],koma_lecture_e=x['koma_lecture_e'],koma_seminar_e=x['koma_seminar_e'],koma_labo_e=x['koma_labo_e'],koma_act_e=x['koma_act_e'],koma_int_e=x['koma_int_e'],descreption=x['descreption'],descreption_j=x['descreption_j'],goals=x['goals'],goals_j=x['goals_j'],content=x['content'],content_j=x['content_j'],lang_of_inst=x['lang_of_inst'],pollicy=x['pollicy'],individual_study=x['individual_study'],ref=x['ref'],notes=x['notes'],schedule=x['schedule'],url=x['url'],course_rgno=int(x['rgno']))
        session.add(newCourse)

session.commit()
    
