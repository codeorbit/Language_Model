'''
	Author = "AKHIL GUPTA"
	Email = "akhilgupta.official@gmail.com"

	This script is used to delete all nodes and relationship under each labels.
	(just a automation script, after all i am lazy to do unproductive work :P).
	
	"The first rule of any technology used in a business is that automation applied
	to an efficient operation will magnify the efficiency.
	The second is that automation applied to an inefficient operation will magnify the inefficiency.
	by - Bill Gates "
	

'''

from py2neo import Graph,authenticate,Node,Relationship
import MySQLdb
import threading
import common.word_classify as wc
import config.db_config
authenticate("localhost:7474",db_config.username,db_config.password)
graph = Graph()


for k,v in wc.prefix.items():
	for pre in v :
		q="""MATCH (n:`%s`)OPTIONAL MATCH (n)-[r]-() DELETE n,r"""%(pre)
		graph.cypher.execute(q)
		q = """ MATCH (n:`%s`) delete  n"""%(str(pre))
		graph.cypher.execute(q)
		print "done ", pre

l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for i in l:
	q="""MATCH (n:`%s`)OPTIONAL MATCH (n)-[r]-() DELETE n,r"""%(i)
	graph.cypher.execute(q)
	# q = """ MATCH(n:`%s`) remove n:'%s' """%("rd_new_"+str(i))
	# graph.cypher.execute(q)
	print "done ", i


for i in range(10):
	q="""MATCH (n:`%s`)OPTIONAL MATCH (n)-[r]-() DELETE n,r"""%(str(i))
	graph.cypher.execute(q)
	# q = """ MATCH(n:`%s`) remove n:'%s' """%("rd_new_"+str(i))
	# graph.cypher.execute(q)
	print "done ", i