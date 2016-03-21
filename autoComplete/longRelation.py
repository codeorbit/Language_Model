'''
 	Author = "AKHIL GUPTA"
 	Email = "akhilgupta.official@gmail.com"


	This module is used to find the complete sentence or form a complete relations
	of nodes given one single word or half of the name of first node.

	Let's take traditional query search on google for e.g. 
	(a) "how to" => you will get auto suggestions like "how to make cake"
	(b) "yah"    => you will get auto suggestions like "yahoo mail india",
					"yahoo mail sign up" etc.

	NOTE :- This module would provide three long relations

'''

from py2neo import Graph,authenticate,Node,Relationship
from config import db_config
authenticate("localhost:7474",db_config.username,db_config.password)
import common.wordClassify as wc
graph = Graph()


def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		#print "true"
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False	

def secondWordDirect(first_word_label,first_word,second_word_list):
	final_word = {}
	for second_word in second_word_list:
		second_word_label = second_word[0]
		if wordPrefixCheck(second_word):
			second_word_label = second_word[0:2]

		query_directed_path_rel = """MATCH(f:`%s`)-[rel:belongs_auto]->(s:`%s`)-[rel2:belongs_auto]->(t) where f.auto_name= '%s' AND s.auto_name =~ '%s.*' RETURN t, rel.auto_score,rel2.auto_score"""%(str(first_word_label),str(second_word_label),str(first_word),str(second_word))
		res_directed_path_rel =  graph.cypher.execute(query_directed_path_rel)
		
		
		third_word_dic = {}
		for prob_word in res_directed_path_rel:
			node = prob_word[0]["auto_name"]
			score = int(prob_word[1])*int(prob_word[2])
			third_word_dic.update({node:score})

		
		word = sorted(third_word_dic,key = third_word_dic.get,reverse = True)[0:2]
		
		try:
			final_word.update({first_word+" "+second_word+" "+word[0]:(third_word_dic[str(word[0])])})
			final_word.update({first_word+" "+second_word+" "+word[1]:third_word_dic[word[1]]})
		except:
			pass
	return final_word

def longRelMain(first_word):
	
	global REL
	
	first_word_label = first_word[0]

	if wordPrefixCheck(first_word_label):
		first_word_label = first_word[0:2]

	probable_words = {}
	
	query_first = """MATCH(a:`%s`)-[rel:belongs_auto]->(s) where a.auto_name ='%s' return s, rel.auto_score """%(str(first_word_label),str(first_word))
	res_query_first = graph.cypher.execute(query_first)
	
	node = {}

	for rel_auto_score in res_query_first:
		name = rel_auto_score[0]['auto_name']
		rel_score = rel_auto_score[1]
		node.update({name:rel_score})
	
	second_word_node = sorted(node,key=node.get,reverse = True)[:3]
	
	return secondWordDirect(first_word_label,first_word,second_word_node)	