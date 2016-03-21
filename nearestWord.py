'''

	Author = "AKHIL GUPTA"
	Email = "akhilgupta.official@gmail.com"

	This module is used to find the nearest word to a given word this could be
	used to tag entity in a query.

	NOTE ==> This module is now replaced by "Entity Tagger" module,
	Which not only detects entity but also gives the domain of entity as well,
	after resolving the diasmbiguation(if exists).

'''

from py2neo import Graph,authenticate,Node,Relationship
import operator
from config import db_config
import common.word_classify as wc


authenticate("localhost:7474",db_config.username,db_config.password)
graph = Graph()

def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False

def nearestWordMain(word,top_n):
	
	final_dic = {}
	word_label = word[0]
	if wordPrefixCheck(word):
		word_label = word[0:2]
	
	query = """MATCH(a:`%s`)-[r:belongs_auto]->(b) where a.auto_name = '%s' return b"""%(str(word_label),str(word))
		
	ret = graph.cypher.execute(query)
	for wrd in ret:
		name = wrd[0]['auto_name']
		count = wrd[0]['self_count']
		final_dic.update({name:count})
	return list(sorted(final_dic.items(), key=operator.itemgetter(1),reverse =True)[:int(top_n)])