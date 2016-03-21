from config import db_config
from py2neo import Graph,authenticate,Node,Relationship
authenticate("localhost:7474",db_config.username,db_config.password)

import word_classify as wc

ENTITY = []
NODE_PROP = {}
graph = Graph()
AMB = []

def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
   		if word_label in wc.prefix[word[0]]:
			return True
	else:

		return False			

def singleEntity(word):
		
	global ENTITY,NODE_PROP
	word_label = "rd_new_"+word[0]
	if wordPrefixCheck(word):
		word_label = "rd_new_"+word[0:2]
	ret=graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a"""%(str(word_label),str(word)))
	
	node_dic = {}

	if ret :
		if word == ret[0][0]["wiki_page_0"]:
			ENTITY.append(word)
			node=(ret)[0][0]
		 
		
			node_dic["wiki_page"] = ret[0][0]["wiki_page_0"]
			node_dic["proprty_main"] = ret[0][0]["proprty_0"]
			node_dic["redirects"] = ret[0][0]["redirects_0"]
			NODE_PROP[word] = node_dic
			
			return node_dic
		
 	else:
 		
 		NODE_CACHE[word] = {}

def relationFirstSecond(first_word,second_word,third_word = None,fourth_word = None):
	
	global ENTITY,AMB
	global NODE_PROP
	dd,dd1,dd2,cc,cc1,cc2=("","","","","","")
	first_word_label = "rd_new_"+first_word[0]
	if wordPrefixCheck(first_word):
		first_word_label = "rd_new_"+first_word[0:2]
	second_word_label = "rd_new_"+second_word[0]
	if wordPrefixCheck(second_word):
		second_word_label = "rd_new_"+second_word[0:2]
	flag = 0
	if third_word is not None:
		third_word_label = "rd_new_"+third_word[0]
		if wordPrefixCheck(third_word):
			third_word_label = "rd_new_"+third_word[0:2]
		cc="-[r2:wiki_belongs]-(c:`%s`)"%(str(third_word_label))
		cc1="AND c.node_name = '%s'"%(str(third_word))
		cc2=",c"
		cc_rel = ",r2"
		flag = 1
	else:
		third_word_label = ""
		third_word = ""	
		cc_rel = ""
	if fourth_word is not None:
		fourth_word_label = "rd_new_"+fourth_word[0]
		if wordPrefixCheck(fourth_word):
			fourth_word_label = "rd_new_"+fourth_word[0:2]
		dd="-[r3:wiki_belongs]-(d:`%s`)"%(str(fourth_word_label))
		dd1="AND d.node_name = '%s'"%(str(fourth_word))
		dd2=",d"
		dd_rel = ",r3"
	else:
		fourth_word_label = ""
		fourth_word = ""
		dd_rel = ""	
			
	
	probable_words={}
	
	query_second_word = """MATCH (a:`%s`)-[r:wiki_belongs]-(b:`%s`)%s%s where a.node_name = '%s' AND b.node_name = '%s' %s %s return a,b%s%s,r%s%s"""%(str(first_word_label),str(second_word_label),str(cc),str(dd),str(first_word),str(second_word),str(cc1),str(dd1),str(cc2),str(dd2),str(cc_rel),str(dd_rel
		))
	
	ret = graph.cypher.execute(query_second_word)
	
	if ret:

		sent = ""
		node_dic = {}
		if third_word is "" :

			rel = eval(ret[0][2]["rel"])   # to get the relation btwn first and second word 
			sent = first_word+" "+second_word
		
		flag = 0   # for disambiguation resolver in entity 
		
		if third_word and fourth_word is "":
			
			ENTITY.remove(first_word+" "+second_word)
			NODE_PROP.pop(first_word+" "+second_word)
			rel = eval(ret[0][4]["rel"])   # to get the relation btwn first,second and third word 
			rel_prev = eval(ret[0][3]["rel"])
			
			flag = 1
			sent = first_word+" "+second_word+" "+third_word
			# print sent

		if third_word is not "" and fourth_word is not "":
			rel = eval(ret[0][5]["rel"])
			rel_prev = eval(ret[0][4]["rel"])
			rel_prev_prev = eval(ret[0][3]["rel"])
			sent = first_word+" "+second_word+" "+third_word+" "+fourth_word
			flag = 2
		
		# Checking common relationships in three nodes.

		if flag ==1:
			for k in rel.keys():
				if k in rel_prev.keys():
					rel.update({sent:rel[k]})

		# Checking common realtionships in four nodes.

		if flag ==2:
			for k in rel.keys():
				if k in rel_prev.keys() and k in rel_prev_prev.keys():
					rel.update({sent:rel[k]})

		if sent in rel.keys():
			index = rel[sent]   # for getting index in node property
			
		 	if (ret)[0][0]["wiki_page_"+str(index)] is None:
				index = 0
						
			if (ret)[0][0]["wiki_page_"+str(0)] is None and (ret)[0][0]["wiki_page_"+str(index)] is None:
				index =2 
			
		 	node_dic["redirects"] = [(ret)[0][0]["redirects_"+str(index)]]
		 
		 	node_dic["wiki_page"] =  (ret)[0][0]["wiki_page_"+str(index)]

		 	node_dic["property"] = (ret)[0][0]["proprty_"+str(index)]
		
		
		node_dic["rel_status"] = True
			
		t=""
		f=""

		if third_word is not "":
			t=third_word
		if fourth_word is not "":
			f=fourth_word
		
		ENTITY.append((first_word+" "+second_word+" "+t+" "+f).strip())
	
		NODE_PROP[(first_word+" "+second_word+" "+t+" "+f).strip()]=node_dic
	
		return node_dic
	else:
		
		if third_word is "" and fourth_word is "":
			
			AMB.append(first_word)
		
		return {"rel_status":False}	

def querySegment(query):
	global AMB
	global NODE_PROP
	NODE_PROP = {}
	global ENTITY
	ENTITY = []
	org_query=query
	prev_relation = False
	temp_sent = ""
	group = [] 
	keys=[]
	query = query.strip().split()
	if len(query)>1:
		for indx in range(len(query)-1):
			if prev_relation:
				
				wrd = temp_sent.split()
				wrd.append(query[indx+1])
				
				if len(wrd)!=4:
					rem=4-len(wrd)
					for i in range(rem):
						wrd.append(None)
				

				prop = relationFirstSecond(wrd[0],wrd[1],wrd[2],wrd[3])
				
				prev_relation = prop["rel_status"]
				if prev_relation:
					temp_sent += " "+query[indx+1]
				else:
					
					if temp_sent!="":
					
						singleEntity(query[indx])
					temp_sent=""		
			
			else:
				
				prop = relationFirstSecond(query[indx],query[indx+1])	
				
				prev_relation = prop["rel_status"]
				if prev_relation:
					
					temp_sent += query[indx]+" "+query[indx+1]
					
			 
	
	elif len(query)==1:
		
		singleEntity(query[0])
	
	
	if prev_relation is False:
		last=query.pop()
		singleEntity(last)
		
	
	for i in AMB:
		singleEntity(i)
	#adding index positions for substr
	for k in ENTITY:
		i=org_query.find(k)
		j=i+(len(k)-1)
		for g in NODE_PROP:
			if k in NODE_PROP:
				NODE_PROP[k]["start_index"]=i
				NODE_PROP[k]["end_index"]=j
						
	dic={}
	#dic is for final dictionary
	dic["entity_details"] = NODE_PROP
	dic["segments"] = list(set(ENTITY))
	
	return dic

#querySegment("mt carmel indiana yahoo")
#querySegment("google")
#querySegment(" google yahoo revolving cylinder engine wilmington ranger file manager mt carmel indiana ")

#querySegment("enigma machine google enigma machine mount carmel yahoo enigma machine rotor central statistical yahoo enigma machine rotor")