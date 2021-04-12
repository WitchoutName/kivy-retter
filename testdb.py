from database import *

db = Database(dbtype='sqlite', dbname='retter.db')
# db = Database(dbtype='mysql', username='root', password='', dbname='retter')

user = User()
user.email = "tom@tom.com"
user.username = "tom1"
user.password = "mot!"
db.add_object(user)

thread = Thread()
thread.title = "test"
thread.description = "lorem inpsum rrrrr rrrrrrr rrrrrr rrrrrr rrrr rrrrrrrrr rrrrrrrrrr rrrrrrr"
thread.author = db.get_object_by_attr(User, "username", "tom1")[0]
thread.tags = "test,test,test,test"
db.add_object(thread)

comment = Comment()
comment.text = "this is also a test"
comment.thread = db.list_query(db.query(Thread))[0]
comment.author = db.get_object_by_attr(User, "username", "tom1")[0]
db.add_object(comment)