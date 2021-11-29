from models import Session, User, Medicine, Category, Order, OrdersMedicine

session = Session()

user1 = User(uid=7976,
             username='kteter',
             firstname='Kseniia',
             lastname='Teterina',
             email='kteter@gmail.com',
             password='12345',
             phone='0993331245'
             )
user2 = User(uid=7946,
             username='ktetej',
             firstname='Ksenwdia',
             lastname='Tdaterina',
             email='ktetwder@gmail.com',
             password='1254345',
             phone='0993661245'
             )
category1 = Category(cid=2423,
                     name='Analgesic')
medicine1 = Medicine(mid=446,
                     category=category1.cid,
                     name='Spasmalgon',
                     manufacturer='Teva',
                     status='available',
                     demand=False)
medicine2 = Medicine(mid=2426,
                     category=category1.cid,
                     name='Paracetamol',
                     manufacturer='Galychfarm',
                     status='available',
                     demand=False)
order1 = Order(oid=9872,
               userId=user1.uid,
               shipDate='2008-10-23 10:37:22',
               status='placed',
               )
order2 = Order(oid=9871,
               userId=user1.uid,
               shipDate='2008-10-23 10:37:22',
               status='placed',
               )
order3 = Order(oid=9873,
               userId=user1.uid,
               shipDate='2008-10-23 10:37:22',
               status='dscsdc',
               )
order1.medicine = [medicine1, medicine2]
order2.medicine = [medicine1]
session.add(user1)
session.add(user2)

session.add(category1)

session.add(medicine1)
session.add(medicine2)

session.add(order1)
session.add(order2)
session.add(order3)
session.commit()

print(session.query(User).all()[0])
print(session.query(Medicine).all())
print(session.query(Order).all())

session.close()
