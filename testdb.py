from database import *

db = Database(dbtype='sqlite', dbname='retter.db')
# db = Database(dbtype='mysql', username='root', password='', dbname='retter')

user = User()
user.email = "admin@admin.admin"
user.username = "admin1"
user.password = "admin"
db.add_object(user)

#thread = Thread()
#thread.title = "My other cat"
#thread.description = "Sara Tiedeman, a vet tech from California, took in a pair of kittens needing critical care. \"They were transferred to the rescue I work with from another organization who didn't have a foster home available for them,\" Sara told Love Meow.\n Sara who specializes in neonatal and critical care kittens, took them on right away. The kittens were frail and just skin and bones. \"Wild (the smaller grey kitten with very fuzzy hair) was very underweight and underdeveloped. Brave (the brown tabby) was limp and nearly unresponsive.\"\n She began tube-feeding the kittens around the clock to get vital nutrients into their tiny bellies. Not only did the feline sisters start to perk up, but Wild the fuzzy kitty even found her squeaky voice and didn't hesitate to use it. She figured out how to latch onto a bottle after just a couple of days."
#thread.author = db.get_object_by_attr(User, "username", "catowner123")[0]
#thread.image = True
#thread.tags = "test,test,test,test"
#db.add_object(thread)

#comment = Comment()
#comment.text = "it's really small!"
#comment.thread = db.get_object_by_attr(Thread, "id", 3)[0]
#comment.author = db.get_object_by_attr(User, "username", "catowner123")[0]
#db.add_object(comment)