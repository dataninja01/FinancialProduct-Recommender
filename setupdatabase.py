from sql import db, Puppy

#CREATE ALL THE TABLES Model --> Db TABLE
db.create_all()

sam = Puppy('Sammy', 3)
frank = Puppy('Frankie', 4)

#None
#None

print(sam.id)
print(frank.id)

db.session.add_all([sam, frank])

##or you can add individually
# db.session.add(sam)
# db.session.add(frank)

db.session.commit()

print(sam.id)
print(frank.id)
