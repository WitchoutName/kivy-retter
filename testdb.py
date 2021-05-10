from database import *

db = Database(dbtype='sqlite', dbname='retter.db')
# db = Database(dbtype='mysql', username='root', password='', dbname='retter')

#user = User()
#user.email = "tom@tomp.com"
#user.username = "catowner123"
#user.password = "mot!2"
#db.add_object(user)

#thread = Thread()
#thread.title = "My cat"
#thread.description = "She had a name among the children;\nBut no one loved though someone owned.\nHer, locked her out of doors at bedtime/nAnd had her kittens duly drowned.\nIn Spring, nevertheless, this cat\nAte blackbirds, thrushes, nightingales,\nAnd birds of bright voice and plume and flight,\nAs well as scraps from neighbours’ pails …"
#thread.author = db.get_object_by_attr(User, "username", "catowner123")[0]
#thread.image = True
#thread.tags = "test,test,test,test"
#db.add_object(thread)

comment = Comment()
comment.text = "agree, very nice cat"
comment.thread = db.get_object_by_attr(Thread, "id", 2)[0]
comment.author = db.get_object_by_attr(User, "username", "tom1")[0]
db.add_object(comment)