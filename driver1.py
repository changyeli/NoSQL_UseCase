from arango import ArangoClient
import json
# Initialize the client for ArangoDB
client = ArangoClient(protocol = 'http', host = 'localhost', port = 8529,
    username = 'root', password = '', enable_logging = True)
db = client.database('test_db')

## read data
with open("edge.json") as f:
	edge = json.load(f, encoding = 'utf8')
with open("email_unique.json") as f:
	emails = json.load(f, encoding = 'utf8')
## create graph
gg = db.graph('enron_graph')
#people = gg.create_vertex_collection('people')
#for each in emails:
#	people.insert(each)

## create edge definition
#gg.create_edge_definition(
 #   name='email',
  #  from_collections=['people'],
   # to_collections=['people']
#)

ee = gg.edge_collection('email')
for each in edge:
	ee.insert(each)