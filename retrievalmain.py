from py2neo import Graph,authenticate,Node,Relationship
authenticate("localhost:7474","neo4j","srmse")
import word_classify as wc
graph = Graph()
# a="value city furniture clearance"
import time
start_time = time.time()
REL=True


'''
	###### third_word ###

	1. all_probable_words :
		will find all the probable words 

	2. query_directed_path_rel:
		will find the directed path from first word to the probable third words (i.e first_word->second_word->third_word)

		return will get the the most probable words and will be of prime importance
	
	3. len(third_word)<3
		beacuse spelling errors occur happen after 3 letter of the word most probably 
	
'''

CLOSE_VALUES = {
	'a':'qwsz',
	'b':'vghn',
	'c':'xdfv',
	'd':'erfcxs',
	'e':'rdsw',
	'f':'rtgvcd',
	'g': 'tyhbvf',
    'h': 'yujnbg',
	'i':  'jkluo',
	'j': 'uikmnh',
	'k': 'iolmj',
	'l': 'opk',
	'm': 'njk',
	'n': 'bhjm',
	'o': 'iklp',
	'p': 'ol',
	'q': 'wa',
	'r': 'edft',
	's': 'wedxza',
	't': 'rfgy',
	'u': 'yhji',
	'v': 'cfgb',
	'w': 'qase',
	'x': 'zsdc',
	'y': 'tghu',
	'z': 'asx'
    	
}
def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		#print "true"
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False			

# print  wordPrefixCheck("advance")

def given_word_count(word):
	word_label=word[0]
	
	if wordPrefixCheck(word):
		word_label = word[0:2]

	query_word_count = """MATCH(a:`%s`) where a.auto_name = '%s' return a.self_count"""%(str(word_label),str(word))
			
	word_count = graph.cypher.execute(query_word_count)
	return int(word_count[0][0])



def rel_given_to_prev(given_word,prev_word):

	given_word_label = given_word[0]
	if wordPrefixCheck(given_word):
		given_word_label = given_word[0:2]
	prev_word_label = prev_word[0]
	if wordPrefixCheck(prev_word):
		prev_word_label = prev_word[0:2]

	
	# print given_word_label
	# print prev_word_label
	probable_words={}
	query_second_word = """MATCH (a:`%s`)-[r:belongs_auto]-(b:`%s`) where b.auto_name =~ '%s.*' AND a.auto_name = '%s' return b"""%(str(prev_word_label),str(given_word_label),str(given_word[0]),str(prev_word))
	#print "try"

	ret = graph.cypher.execute(query_second_word)


	# print (ret)

	for i in range(len(ret)):
		#print ret[i][0]["name"]
		name = ret[i][0]['auto_name']
	
		#print ret[i][0]["self_count"]
		rel_score="""MATCH(a:`%s`)-[r:belongs_auto]-(b:`%s`) where a.auto_name = '%s' AND b.auto_name = '%s' return r.auto_score, b.self_count"""%(str(prev_word_label),str(given_word_label),str(prev_word),str(name))
		ret_rel_score = graph.cypher.execute(rel_score)
		# print ret_rel_score
		probable_words[name]=[int(ret_rel_score[0][0]),int(ret_rel_score[0][1])]      # first is score and second is self_count 
	# print probable_words
	return probable_words

# rel_given_to_prev("yahoo","mail")



def first_word(first_word):
	first_word_label=first_word[0]
	
	if wordPrefixCheck(first_word_label):
		first_word_label = first_word_label[0:2]
	probable_words={}
	if len(first_word)<3:
		first_word_query = """MATCH(a:`%s`) where a.auto_name =~ '%s.*' return a.auto_name, a.self_count"""%(str(first_word_label),str(first_word))
		res_first_word = graph.cypher.execute(first_word_query)
		#print res_first_word
		for each_ele_first_word in res_first_word:
				probable_words[each_ele_first_word[0]]= int(each_ele_first_word[1])
		#print probable_words
		return probable_words

	else:

		probable_first_words = [first_word[:-1]+char
							for char in CLOSE_VALUES[first_word[-1]]]
		probable_first_words.append(first_word)
		# print probable_first_words
		for p_word in probable_first_words:
			first_word_query = """MATCH(a:`%s`) where a.auto_name =~ '%s.*' return a.auto_name, a.self_count"""%(str(first_word_label),str(p_word))
			res_first_word = graph.cypher.execute(first_word_query)			
				
			for each_ele_first_word in res_first_word:
				probable_words[each_ele_first_word[0]]= int(each_ele_first_word[1])
		
		#print probable_words
		return  probable_words



def second_word(first_word,second_word):
	global REL
	probable_words={}
	
	first_word_label = first_word[0]
	if wordPrefixCheck(first_word):
		
		first_word_label = first_word[0:2]

	second_word_label = second_word[0]
	if wordPrefixCheck(second_word):
		second_word_label = second_word[0:2]
	
	# print first_word_label
	# print second_word_label

	# first_first_aplha = first_word[0]
	# second_first_aplha = second_word[0]
	first_word_count = given_word_count(first_word)
	

	if len(second_word)<3:
		#print "second_word"
		most_probable_words = rel_given_to_prev(second_word,first_word)
		if len(most_probable_words):
			REL=True
		else:
			REL=False
		
		#print most_probable_words

		return most_probable_words, first_word_count,REL
	
	else :
		flag=0
		probable_second_words = [second_word[:-1]+char
									for char in CLOSE_VALUES[second_word[-1]]]				
	
		probable_second_words.append(second_word)
		# print probable_second_words
		for trav in probable_second_words:
			

			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`) where f.auto_name= '%s' AND s.auto_name =~ '%s.*' RETURN s ,rel.auto_score """%(str(first_word_label),str(second_word_label),str(first_word),str(trav))

	# 		query_directed_path_rel = """MATCH(p:`autotest`)-[t:belongs]->(n:`autotest`)-[r:belongs]->(m:`autotest`) where p.name= '%s' AND n.nprint most_probable_wordsame = '%s' AND m.name='%s' RETURN p,n,m"""%(str(first_word),str(second_word),str(trav))
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)

			for each_ele in res_directed_path_rel:
				
				probable_words[each_ele[0]["auto_name"]]= [ int(each_ele[1]),each_ele[0]["self_count"]]
				#probable_words[each_ele[0]["auto_name"]] = each_ele[1]
				flag=1
		if flag==1:
			REL=True
		else:
			REl=False

		
		# print probable_words,first_word_count,REL
		return probable_words,first_word_count,REL

# second_word("advance","auto")


def third_word(first_word,second_word,third_word):

	first_word_label = first_word[0]
	if wordPrefixCheck(first_word):
		first_word_label = first_word[0:2]
	second_word_label = second_word[0]
	if wordPrefixCheck(second_word):
		second_word_label = second_word[0:2]
	third_word_label = third_word[0]
	if wordPrefixCheck(third_word):
		third_word_label = third_word[0:2]



	global REL
	probable_words={}
	
	second_word_count = given_word_count(second_word)

	first_word_count = given_word_count(first_word) 
	#print first_word_count
	# first_first_aplha = first_word[0]
	# second_first_aplha = second_word[0]
	# third_first_aplha = third_word[0]	
	
	rel_first_third = rel_given_to_prev(third_word,first_word)
	#print rel_first_third
	rel_second_third = rel_given_to_prev(third_word,second_word)
	#print rel_second_third
	rel_second_first = rel_given_to_prev(second_word,first_word)
	if len(rel_second_third):
		REL=True
	else:
		REL=False

	# print first_word_label
	# print second_word_label
	# print third_word_label
	if len(third_word)<3:
		query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]-(s:`%s`)-[rela:belongs_auto]-(t:`%s`) where f.auto_name= '%s' AND s.auto_name = '%s' AND t.auto_name=~ '%s.*' RETURN t"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(first_word),str(second_word),str(third_word))
		res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		# print res_directed_path_rel
		for trav in res_directed_path_rel:
			
			probable_words[trav[0]["auto_name"]]=int(trav[0]["self_count"])
		# print probable_words
		#print first_word_count,second_word_count,rel_first_third,rel_second_third,probable_words
		return first_word_count,second_word_count,rel_first_third,rel_second_third,probable_words,REL
		
	else:
		flag=0
		probable_third_words = [third_word[:-1]+char
								for char in CLOSE_VALUES[third_word[-1]]
								if len(third_word) > 2]
		
		probable_third_words.append(third_word)
	 	
	 	#print probable_third_words				

	 	for trav in probable_third_words:
			#print trav
			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]-(s:`%s`)-[rel1:belongs_auto]-(t:`%s`) where f.auto_name= '%s' AND s.auto_name ='%s' AND t.auto_name=~ '%s.*' RETURN t"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(first_word),str(second_word),str(trav))

	 		
	 		#query_directed_path_rel = """MATCH(p:`autotest`)-[t:belongs]->(n:`autotest`)-[r:belongs]->(m:`autotest`) where p.name= '%s' AND n.name = '%s' AND m.name='%s' RETURN p,n,m"""%(str(first_word),str(second_word),str(trav))
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
			#print res_directed_path_rel
			
			for i in range( len (res_directed_path_rel)):
		 		probable_words[res_directed_path_rel[i][0]["auto_name"]]=int(res_directed_path_rel[i][0]["self_count"])
		 		flag=1
			#print probable_words

		if flag==1:
			REL=True
		else:
			REL =False
		# print probable_words
		return first_word_count,second_word_count,rel_first_third,rel_second_third,probable_words,REL
# print third_word("advance","auto","pa")

def fourth_word(first_word,second_word,third_word,fourth_word):
	global REL
	probable_words={}
	# first_first_aplha = first_word[0]
	# second_first_aplha = second_word[0]
	# third_first_aplha = third_word[0]
	first_word_label = first_word[0]
	if wordPrefixCheck(first_word):
		first_word_label = first_word[0:2]
	second_word_label = second_word[0]
	if wordPrefixCheck(second_word):
		second_word_label = second_word[0:2]
	third_word_label = third_word[0]
	if wordPrefixCheck(third_word):
		third_word_label = third_word[0:2]
	fourth_word_label = fourth_word[0]
	if wordPrefixCheck(fourth_word):
		fourth_word_label = fourth_word[0:2]
	
	
	if len(rel_given_to_prev(fourth_word,third_word)):
		REL=True
	else:
		REL=False

	if len(fourth_word)<3:
		query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`)-[rel1:belongs_auto]->(t:`%s`)-[rel2:belongs_auto]->(ft:`%s`) where f.auto_name= '%s' AND s.auto_name ='%s' AND t.auto_name= '%s' AND ft.auto_name =~ '%s.*' RETURN ft"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(fourth_word_label),str(first_word),str(second_word),str(third_word),str(fourth_word))

	
	#query_directed_path_rel = """MATCH(p:`autotest`)-[t:belongs]->(n:`autotest`)-[r:belongs]->(m:`autotest`) where p.name= '%s' AND n.name = '%s' AND m.name='%s' RETURN p,n,m"""%(str(first_word),str(second_word),str(trav))
		res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		for trav in res_directed_path_rel:
			probable_words[trav[0]["auto_name"]]=trav[0]["self_count"]
		#print probable_words
		return probable_words,REL

	else:
		flag=0
		probable_fourth_words = [fourth_word[:-1]+char
								for char in CLOSE_VALUES[fourth_word[-1]]
								if len(fourth_word) > 2]
		
		probable_fourth_words.append(fourth_word)
	 	
	 	#print probable_fourth_words,REL
		for trav in probable_fourth_words:
			#print trav

			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`)-[rel1:belongs_auto]->(t:`%s`)-[rel2:belongs_auto]->(ft:`%s`) where f.auto_name= '%s' AND s.auto_name ='%s' AND t.auto_name= '%s' AND ft.auto_name =~ '%s.*' RETURN ft"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(fourth_word_label),str(first_word),str(second_word),str(third_word),str(trav))

				
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
			#print res_directed_path_rel

			for i in range( len (res_directed_path_rel)):
				probable_words[res_directed_path_rel[i][0]["auto_name"]]=int(res_directed_path_rel[i][0]["self_count"])
				flag=1
		#print probable_words

		if flag==1:
			REL=True
		else:
			REL =False

		return probable_words,REL

		



