from py2neo import Graph,authenticate,Node,Relationship
import operator
import db_config
authenticate("localhost:7474",db_config.username,db_config.password)
import word_classify as wc
graph = Graph()

def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		#print "true"
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False

def tagsMain(word,top_n):
	final_dic = {}
	word_label = word[0]
	if wordPrefixCheck(word):
		word_label = word[0:2]
	
	query = """MATCH(a:`%s`)-[r:belongs_auto]->(b) where a.auto_name = '%s' return b"""%(str(word_label),str(word))
		#print "try"
	ret = graph.cypher.execute(query)
	for wrd in ret:
		name = wrd[0]['auto_name']
		count = wrd[0]['self_count']
		final_dic.update({name:count})
	return list(sorted(final_dic.items(), key=operator.itemgetter(1),reverse =True)[:int(top_n)])
# tagsMain('google')

