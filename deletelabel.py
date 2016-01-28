from py2neo import Graph,authenticate,Node,Relationship
import MySQLdb
import threading
authenticate("localhost:7474","neo4j","8760neo4j")
graph = Graph()



l=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','w','x','y','z','"','#','$','&','(','+','-','.',':','1','2','3','4','5','6','7','8','9']
for i in l:
	q="""MATCH (n:`%s`)OPTIONAL MATCH (n)-[r]-() DELETE n,r"""%(str(i)+"_auto")
	print i	
	graph.cypher.execute(q)
	q="""MATCH (n:`%s`)OPTIONAL MATCH (n)-[r]-() DELETE n,r"""%(str(i.upper())+"_auto")
	print i.upper()
	graph.cypher.execute(q)
	print "done"