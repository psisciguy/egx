# http://www.mapfish.org/doc/tutorials/sqlalchemy.html
# describe the database schema

from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

# EF
from abc import ABCMeta, abstractmethod		# for making StimUnit an Abstract Base Class (ABC); metaclass; virtual


metadata = schema.MetaData()

def now():
    return datetime.datetime.now()

page_table = schema.Table('page', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('page_seq_id', optional=True), primary_key=True),
    schema.Column('content', types.Text(), nullable=False),
    schema.Column('posted', types.DateTime(), default=now),
    schema.Column('title', types.Unicode(255), default=u'Untitled Page'),
    schema.Column('heading', types.Unicode(255)),
)
comment_table = schema.Table('comment', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('comment_seq_id', optional=True), primary_key=True),
    schema.Column('pageid', types.Integer,
        schema.ForeignKey('page.id'), nullable=False),
    schema.Column('content', types.Text(), default=u''),
    schema.Column('name', types.Unicode(255)),
    schema.Column('email', types.Unicode(255), nullable=False),
    schema.Column('created', types.TIMESTAMP(), default=now()),
)
pagetag_table = schema.Table('pagetag', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('pagetag_seq_id', optional=True), primary_key=True),
    schema.Column('pageid', types.Integer, schema.ForeignKey('page.id')),
    schema.Column('tagid', types.Integer, schema.ForeignKey('tag.id')),
)
tag_table = schema.Table('tag', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('tag_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(20), nullable=False, unique=True),
)

# EF:  Adding on a EF-specific class to test... Test StimUnit hierarchy/inheritance

# - Make a simplified version here, with 1 argument
#   - Add a getStimUnitType method ()... reaches into the data store
#   - Add a sendTestData() method that sends data to stdout as a test of using
#     SQLAlchemy with non-db based operations
class StimUnit(object):
	"""
		A stimulation unit
		
		Attributes:
			sn: pre-prog sn
			uaddr: dynamic assigned unit addr
			gaddr: assigned group addr ... ?We should save gaddr; yet when units moved around at end of season; need reset procedure
			utype: EC or MC
			model:
			voltage:
			freq: 
			install_date:
			op_hrs:
	"""
	# Code Notes:
	# - Should be an Abstract Base Class, since it is only meant to be inherited from
	
	__metaclass__ = ABCMeta
	
	# A class variable, counting number of StimUnits
	population = 0
	
	def __init__(self, sn=0, uaddr=0, gaddr=0, utype="EC", model=0, voltage=0, freq=0, install_date="", op_hrs=0):
		"""
		Return a StimUnit object whose sn is 0, etc...		
		"""
		self.sn = sn
		self.uaddr = uaddr					# retrieved during discovery phase
		self.gaddr = gaddr					# set based on uaddr & command		
		self.model = model					# Set based on discovery messages or unit query
		self.voltage = voltage				# Set based on command
		self.freq = freq					# Set based on command
		self.install_date = install_date	# set based on date of discovery
		self.op_hrs = op_hrs				# increment based on on-time, in hours (float)
		
		print("Initializing serial number: {})" .format(self.sn))
		# When a StimUnit is created, it is added to num_stim_units
		StimUnit.population += 1
	
	# abstractmethod - prevents us from directly creating instance of StimUnit... forces inheritance
	@abstractmethod
	def stimUnitType():
		"""Return a string representing the type of StimUnit this is."""
		pass
    
# define classes and mappers to work with the Object-Relational API
class Page(object):
    pass

class Comment(object):
    pass

class Tag(object):
    pass

orm.mapper(Page, page_table, properties={
    'comments':orm.relation(Comment, backref='page'),
    'tags':orm.relation(Tag, secondary=pagetag_table)
})
orm.mapper(Comment, comment_table)
orm.mapper(Tag, tag_table)