from py2neo import Graph,authenticate,Node,Relationship
import MySQLdb
import threading
authenticate("localhost:7474","neo4j","8760neo4j")
graph = Graph()
mynode = list(graph.find('fw', property_key='count'))
ct=1
fobj = open("textdump1.txt","r").readlines()
file_tacker=open("tarcker.txt","a")
#for i in fobj:

def indexing(i):
	global ct
	print "*********"
	print i
	print ct
	print "**********"
	i = i.lower().strip().replace("'","")
	file_tacker.write(str(i))


	s=b.split(" ",3)
	dic={}
	for i in range(len(s)):
		
		n2=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(s[i][0]),str(s[i])))
		

		if n2:
			
			#print n2[0][0]
			n2=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a.self_count"""%(str(s[i][0]),str(s[i])))
			count=int(n2[0][0])+1
			#print "increased self_count"
			n2=graph.cypher.execute("""MATCH (a : `%s`) where a.auto_name = '%s' set a.self_count = '%s' """%(str(s[i][0]),str(s[i]),str(count)))
			
			flag=0

			if i!=0:
				#print "yes"
				#print "finding Relationship"
				belongs = graph.cypher.execute("""MATCH (n:`%s`)-[r:belongs]->(m:`%s`) WHERE n.auto_name ='%s' AND m.auto_name = '%s' return r.score """%(str(s[i-1][0]),str(s[i][0]),str(s[i-1]),str(s[i])))
				#print belongs
				#print "---------------------"
				#print belongs[0][0]
				if belongs:
					score=int(belongs[0][0])+1
					score_update=graph.cypher.execute("""MATCH (n:`%s`)-[r:belongs]->(m:`%s`) WHERE n.auto_name='%s' AND m.auto_name ='%s'set r.score = '%s' RETURN r"""%(str(s[i-1][0]),str(s[i][0]),str(s[i-1]),str(s[i]),str(score)))
					#print "updated sore " +str(score)
					flag=1
		
				if (flag==0):
					#print "flag"
					node1=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(s[i-1][0]),str(s[i-1])))
					node1=node1[0][0]
					#print node1
					#print "n2"
					nod=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(s[i][0]),str(s[i])))
					nod=nod[0][0]
					dic["score"]=1
					graph.create(Relationship(node1 , ("belongs",dic),nod))
		
					
		else:
			#print " not found "
			n=Node(str(s[i][0]),auto_name=str(s[i]),self_count=1)
			graph.create(n)
			
			if i!=0:
				print s[i-1][0]
				print s[i-1]
				#rel=graph.cypher.execute("MATCH (a:`autotest`), (b:`autotest`) where a.name = '"+str(s[i-1])+"' AND  where b.name = '"+str(s[i])+"' CREATE (a)-[r:belongs]->(b) return r")
				#n1=graph.cypher.execute("""MATCH (n: `%s`) where n.name = '%s' return n"""%(str(s[i-1])))

				n1=graph.cypher.execute("""MATCH (n: `%s`) where n.auto_name = '%s' return n"""%(str(s[i-1][0]),str(s[i-1])))
				print n1
				n1=n1[0][0]
				dic["score"]=1
				graph.create(Relationship(n1 , ("belongs",dic),n))
	ct+=1

		
counter =0
while counter<len(fobj):
	if threading.activeCount()<100:
		print counter
		t=threading.Thread(target=indexing,args=(fobj[counter],))
 		t.start()
 		counter+=1
