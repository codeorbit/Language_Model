from py2neo import Graph,authenticate,Node,Relationship
import db_config
authenticate("localhost:7474",db_config.username,db_config.password)
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
	
	return probable_words




def first_word(first_word):
	first_word_label=first_word[0]
	
	if wordPrefixCheck(first_word_label):
		first_word_label = first_word_label[0:2]
	probable_words={}
	if len(first_word)<3:
		first_word_query = """MATCH(a:`%s`) where a.auto_name =~ '%s.*' return a.auto_name, a.self_count"""%(str(first_word_label),str(first_word))
		res_first_word = graph.cypher.execute(first_word_query)
		
		for each_ele_first_word in res_first_word:
				probable_words[each_ele_first_word[0]]= int(each_ele_first_word[1])
		
		return probable_words

	else:

		probable_first_words = [first_word[:-1]+char
							for char in CLOSE_VALUES[first_word[-1]]]
		probable_first_words.append(first_word)
		
		for p_word in probable_first_words:
			first_word_query = """MATCH(a:`%s`) where a.auto_name =~ '%s.*' return a.auto_name, a.self_count"""%(str(first_word_label),str(p_word))
			res_first_word = graph.cypher.execute(first_word_query)			
				
			for each_ele_first_word in res_first_word:
				probable_words[each_ele_first_word[0]]= int(each_ele_first_word[1])

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
	
	first_word_count = given_word_count(first_word)
	

	if len(second_word)<3:
		
		most_probable_words = rel_given_to_prev(second_word,first_word)
		if len(most_probable_words):
			REL=True
		else:
			REL=False
		
		return most_probable_words, first_word_count,REL
	
	else :
		flag=0
		probable_second_words = [second_word[:-1]+char
									for char in CLOSE_VALUES[second_word[-1]]]				
	
		probable_second_words.append(second_word)
		for trav in probable_second_words:
			

			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`) where f.auto_name= '%s' AND s.auto_name =~ '%s.*' RETURN s ,rel.auto_score """%(str(first_word_label),str(second_word_label),str(first_word),str(trav))
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)

			for each_ele in res_directed_path_rel:
				
				probable_words[each_ele[0]["auto_name"]]= [ int(each_ele[1]),each_ele[0]["self_count"]]
				
				flag=1
		if flag==1:
			REL=True
		else:
			REl=False

		return probable_words,first_word_count,REL




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
	
	
	rel_first_third = rel_given_to_prev(third_word,first_word)

	rel_second_third = rel_given_to_prev(third_word,second_word)

	rel_second_first = rel_given_to_prev(second_word,first_word)
	if len(rel_second_third):
		REL=True
	else:
		REL=False


	if len(third_word)<3:
		query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]-(s:`%s`)-[rela:belongs_auto]-(t:`%s`) where f.auto_name= '%s' AND s.auto_name = '%s' AND t.auto_name=~ '%s.*' RETURN t"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(first_word),str(second_word),str(third_word))
		res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		
		for trav in res_directed_path_rel:
			
			probable_words[trav[0]["auto_name"]]=int(trav[0]["self_count"])

		return first_word_count,second_word_count,rel_first_third,rel_second_third,probable_words,REL
		
	else:
		flag=0
		probable_third_words = [third_word[:-1]+char
								for char in CLOSE_VALUES[third_word[-1]]
								if len(third_word) > 2]
		
		probable_third_words.append(third_word)
			

	 	for trav in probable_third_words:
			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]-(s:`%s`)-[rel1:belongs_auto]-(t:`%s`) where f.auto_name= '%s' AND s.auto_name ='%s' AND t.auto_name=~ '%s.*' RETURN t"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(first_word),str(second_word),str(trav))

	 		
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		
			
			for i in range( len (res_directed_path_rel)):
		 		probable_words[res_directed_path_rel[i][0]["auto_name"]]=int(res_directed_path_rel[i][0]["self_count"])
		 		flag=1
			

		if flag==1:
			REL=True
		else:
			REL =False

		return first_word_count,second_word_count,rel_first_third,rel_second_third,probable_words,REL


def fourth_word(first_word,second_word,third_word,fourth_word):
	global REL
	probable_words={}

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

	
		res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		for trav in res_directed_path_rel:
			probable_words[trav[0]["auto_name"]]=trav[0]["self_count"]
		
		return probable_words,REL

	else:
		flag=0
		probable_fourth_words = [fourth_word[:-1]+char
								for char in CLOSE_VALUES[fourth_word[-1]]
								if len(fourth_word) > 2]
		
		probable_fourth_words.append(fourth_word)
	 	
	 	
		for trav in probable_fourth_words:
			

			query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`)-[rel1:belongs_auto]->(t:`%s`)-[rel2:belongs_auto]->(ft:`%s`) where f.auto_name= '%s' AND s.auto_name ='%s' AND t.auto_name= '%s' AND ft.auto_name =~ '%s.*' RETURN ft"""%(str(first_word_label),str(second_word_label),str(third_word_label),str(fourth_word_label),str(first_word),str(second_word),str(third_word),str(trav))

				
			res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
			

			for i in range( len (res_directed_path_rel)):
				probable_words[res_directed_path_rel[i][0]["auto_name"]]=int(res_directed_path_rel[i][0]["self_count"])
				flag=1
		

		if flag==1:
			REL=True
		else:
			REL =False

		return probable_words,REL

		



