from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, desc
from sqlalchemy.types import Float, String, Integer, DateTime, Enum, Text, BLOB, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    image = Column(BLOB)
    threads = relationship("Thread", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="threads")
    comments = relationship("Comment", back_populates="thread")
    date = Column(DateTime, default=datetime.datetime.utcnow)
    tags = Column(String)
    image = Column(Boolean)
    likes = Column(Integer, default=0)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(160), unique=True, nullable=False)
    likes = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="comments")
    thread_id = Column(Integer, ForeignKey('threads.id'))
    thread = relationship("Thread", back_populates="comments")


class Database:
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}',
        'mysql': 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='retter.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def order_query(self, query, order):
        try:
            return query.order_by(order)
        except:
            print("attribute not found")
            return False

    def join_query(self, query, object_type):
        try:
            return query.join(object_type)
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def filter_query(self, query, by):
        try:
            return query.filter(by)
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def list_query(self, query):
        try:
            return query.all()
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def add_object(self, object):
        try:
            self.session.add(object)
            self.session.commit()
            return True
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def query(self, object_type):
        try:
            return self.session.query(object_type)
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def get_object_by_attr(self, object, by, attr, contition=lambda x, v: x.is_(v)):
        try:
            return self.list_query(self.filter_query(self.query(object), contition(getattr(object, by), attr)))
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def get_object_by_relation(self, object, rel, by=None, value=None, contition=lambda b, v: True):
        try:
            return self.list_query(self.filter_query(self.join_query(self.query(object), rel), contition(by, value)))
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False

    def del_object(self, object, by, attr):
        try:
            obj = self.get_object_by_attr(object, by, attr)[0]
            self.session.delete(obj)
            self.session.commit()
            return True
        except Exception as e:
            print(e.__traceback__.tb_next)
            return False
