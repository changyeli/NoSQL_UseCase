from arango import ArangoClient

class analyze:
	def __init__(self):
		self.client = ArangoClient(protocol = 'http', host = 'localhost', 
			port = 8529, username = 'root', password = '', enable_logging = True)
		self.db = self.client.database('test_db')
		self.email = self.db.collection("email")
		self.people = self.db.collection("people")
	def stat(self):
		print "----------------------------------------"
		print "The statistics of email collection is: "
		for k, v in self.email.statistics().iteritems():
			print k, v
		print "----------------------------------------"
		print "The statistics of people collection is: "
		for k, v in self.people.statistics().iteritems():
			print k, v
		print "----------------------------------------"
	def sentStat(self):
		s1 = "FOR x IN email COLLECT people = x._to WITH COUNT INTO counter SORT counter DESC RETURN{people:FIRST(people), number:FIRST(counter)}"
		d1 = self.db.aql.execute(s1)
		
		


x = analyze()
x.stat()
x.sentStat()