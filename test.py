from database import *


db = Database(dbtype='sqlite', dbname='retter.db')

com = db.get_object_by_attr(Comment, "id", 2)[0]
com.thread_id = 2
db.session.commit()