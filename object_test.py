# SQLAlchemy manages the mapped objects in a so-called session.



import model
from sqlalchemy import orm
from sqlalchemy import create_engine

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///:memory:', echo=True)
model.metadata.bind = engine
model.metadata.create_all()

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
    expire_on_commit=True)
session = orm.scoped_session(sm)


# ------------------------------ Run separately...

# INSERT
from object_test import session
import model
test_page = model.Page()
test_page.title = u'Test Page'
test_page.content = u'Test content'
test_page.title

# Add the object to the session
session.add(test_page)
print (test_page.id)

session.flush()
print (test_page.id)

# commit the changes:
session.commit()

for page in page_q:
     print (page.title)



