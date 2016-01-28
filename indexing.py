from multiprocessing import Pool
import threading
import word_classify as wc
import urllib2 
from py2neo import Graph,authenticate,Node,Relationship
authenticate("localhost:7474","neo4j","8760neo4j")

# graph = Graph("http://localhost:7474/db/data")
graph = Graph()
ct=1
fobj = open("testdata.txt","r").readlines()
file_tracker=open("tracker.txt","a")
#file_duplicates = open("duplicates.txt","a")
#for i in fobj:

word_prefix = False
'''
def nodesPool(words_list):
	p = Pool(15)
	p.map(makeLabel,words_list)

def bactchCall():
	print "EEEEEEEEEEEEEEEEEEEEEEEEE"
	url = urllib2.urlopen("http://localhost:3000/").read()
	words_list = eval(url)
	nodesPool(words_list)
'''
def nodeIndex(current_word_label,current_word,prev_word_label=None,prev_word=None):
	 # print current_word_label
	 # print current_word
	 # print prev_word
	 # print prev_word_label

	#print "**************************************************"
	try: 
		n2=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(current_word_label),str(current_word)))
		if n2:
		
		  #print n2[0][0]
			n2=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a.self_count"""%(str(current_word_label),str(current_word)))
			count=int(n2[0][0])+1
		  #print "increased self_count"
			n2=graph.cypher.execute("""MATCH (a : `%s`) where a.auto_name = '%s' set a.self_count = '%s' """%(str(current_word_label),str(current_word),str(count)))
		
			

			flag=0

			if prev_word and prev_word_label:
			  #print "yes"
			  #print "finding Relationship"
				belongs = graph.cypher.execute("""MATCH (n:`%s`)-[r:belongs_auto]->(m:`%s`) WHERE n.auto_name ='%s' AND m.auto_name = '%s' return r.auto_score """%(str(prev_word_label),str(current_word_label),str(prev_word),str(current_word)))
			  #print belongs
			  #print "---------------------"
			  #print belongs[0][0]
				if belongs:
					score=int(belongs[0][0])+1
					score_update=graph.cypher.execute("""MATCH (n:`%s`)-[r:belongs_auto]->(m:`%s`) WHERE n.auto_name='%s' AND m.auto_name ='%s' set r.auto_score = '%s' RETURN r"""%(str(prev_word_label),str(current_word_label),str(prev_word),str(current_word),str(score)))
				  #print "updated sore " +str(score)
					flag=1

		  		if (flag==0):
			  #print "flag"
					node1=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(prev_word_label),str(prev_word)))
			  		node1=node1[0][0]
			  #print node1
			  #print "n2"
			  		node2=graph.cypher.execute("""MATCH (a: `%s`) where a.auto_name = '%s' return a"""%(str(current_word_label),str(current_word)))
			  		node2=node2[0][0]
			  		dic= {}
			 	 	dic["auto_score"]=1
			  		graph.create(Relationship(node1 , ("belongs_auto",dic),node2))
			  		#print "relation " +current_word+"::"+prev_word
				  					
	 	else:
		  #print "not found "
			
				node2=Node(str(current_word_label),auto_name=str(current_word),self_count=1)
				graph.create(node2)
			
			  #statement = "MERGE (n:%s {auto_name:{N},self_count:{M}}) RETURN n"%(str(s[i][0]))
			  #tx.append(statement, {"N": s[i],"M":"1"})
			  #tx.process()
			  #tx.commit()
			  #n=graph.cypher.execute("""MATCH (n: `%s`) where n.auto_name = '%s' return n"""%(str(s[i][0]),str(s[i])))
			  	if prev_word and prev_word_label:
			
				 	node1=graph.cypher.execute("""MATCH (n: `%s`) where n.auto_name = '%s' return n"""%(str(prev_word_label),str(prev_word)))
				  	# print n1
				  	node1=node1[0][0]
				  	dic ={}
				  	dic["auto_score"]=1
				  	graph.create(Relationship(node1 , ("belongs_auto",dic),node2))
				  	#print "relation " +current_word+"::"+prev_word
	except Exception as e:
			
  		print "EXCEPTION IN CREATING NODES :: "+ str(e)  


def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		#print "true"
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False			




def makeLabel(sentence):
#for sentence in fobj:	
	try: 
		global ct
		print "*********"
		print sentence
		print ct
		
		# tx = graph.cypher.begin()
		sentence = sentence.lower().replace("'","")
		file_tracker.write(str(sentence))
		sentence=sentence.strip()
		s=sentence.split(" ",3)
		#print "sentence " + str(s)
		dic={}
		for i in range(len(s)):

			#current_wrd_prsnt = False
			current_word = s[i].strip()
		  	current_word_label = current_word[0]
		    
		  	if wordPrefixCheck(current_word):
		  		current_word_label = current_word[0:2]
		  		if i!=0:
		  			#prev_wrd_prsnt = False
		  			prev_word = s[i-1].strip()
		  			prev_word_label = prev_word[0]
		  			if wordPrefixCheck(prev_word):
		  				prev_word_label = prev_word[0:2]
		  				
		  			nodeIndex(current_word_label,current_word,prev_word_label,prev_word)
		  		else:
		  			nodeIndex(current_word_label,current_word)
		  	else:
		  		if i!=0:
		  		
		  			prev_word = s[i-1].strip()
		  			prev_word_label = prev_word[0]
		  			if wordPrefixCheck(prev_word):
		  				prev_word_label = prev_word[0:2]
		  			
		  			nodeIndex(current_word_label,current_word,prev_word_label,prev_word)
		  		else:
		  			nodeIndex(current_word_label,current_word)
		  		#print "False"
		print "_________________________________________________________________________"
		ct+=1
	except Exception as e:
		
		print "EXCEPTION IN CHECKING LABELS "+ str(e)


counter = 0
while len(fobj):
	if threading.activeCount()<3:
		t= threading.Thread(target = makeLabel, args = (fobj[counter],)) 
		t.start()
		counter+=1


