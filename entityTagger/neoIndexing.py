import word_classify as wc
import db_config
import json 
import sys,traceback
from py2neo import Graph,authenticate,Node,Relationship
authenticate("localhost:7474",db_config.username,db_config.password)

graph = Graph()

index_log = open("indexlog.txt","a")
error_log = open("errorlog.txt","a")

# redirect_link = wiki_page , rel_count is relationship count between two nodes, rel is dic of relationship

word_prefix = False

def nodeIndex(current_word_label,current_word,disambiguation_link,disambiguation_status,redirect_link,redirect_status,proprty,change_status,redirect,prev_word_label=None,prev_word=None):

	
	try: 
		# list of wiki pages
		wiki_pages_lst = []
		
		
		crnt=graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a"""%(str(current_word_label),str(current_word)))
		if crnt:
			# if current_word exist as node 
			
			crnt=graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.wiki_self_count """%(str(current_word_label),str(current_word)))
			
			count=int(crnt[0][0])+1
		  #print "increased wiki_self_count"
			crnt=graph.cypher.execute("""MATCH (a : `%s`) where a.node_name = '%s' set a.wiki_self_count = '%s' """%(str(current_word_label),str(current_word),str(count)))
			if redirect:
				rdstats = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.redirect_status """%(str(current_word_label),str(current_word)))
				status = int(rdstats[0][0])+1
				rdstats_chng = graph.cypher.execute("""MATCH (a : `%s`) where a.node_name = '%s' set a.redirect_status = '%s' """%(str(current_word_label),str(current_word),str(status)))

			else : 
				disstats = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.disambiguation_status """%(str(current_word_label),str(current_word)))
				status = int(disstats[0][0])+1
				disstats_chng = graph.cypher.execute("""MATCH (a : `%s`) where a.node_name = '%s' set a.disambiguation_status = '%s' """%(str(current_word_label),str(current_word),str(status)))
			
			
			wiki_list_ret = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.wiki_pages_lst """%(str(current_word_label),str(current_word)))

			wiki_pg_res = eval(wiki_list_ret[0][0])
			wiki_pages_lst = wiki_pg_res
			print wiki_pages_lst
			if redirect_link not in wiki_pg_res:
				# it means incoming node is new with respect to NEW wiki_page
				
				indx_count = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.index_count """%(str(current_word_label),str(current_word)))
				print current_word
				print "index_count ",indx_count
				indx_count = int(indx_count[0][0])+1	
				
				wiki_pages_lst.append(redirect_link)
				print wiki_pages_lst
				wiki_pages_lst = "%s"%(wiki_pages_lst)
			
			 	print "modified wiki_pages_lst,",wiki_pages_lst
			 	
			 	#checking existance of node/word in NEW wiki_page
			 	nw_nd_flg = 0
			 	  
			 	if current_word == redirect_link or current_word in list(disambiguation_link) :
					nw_nd_flg = 1
					mn_nd_indx = 0
			 	
			 	if nw_nd_flg == 1:
			 		node_new = graph.cypher.execute("""MATCH (a : `%s`) where a.node_name = "%s" set a.redirects_%s = "%s", a.wiki_page_%s = "%s", a.proprty_%s = "%s", a.wiki_pages_lst = "%s" ,a.index_count = "%s" """%(str(current_word_label),str(current_word),str(indx_count),str(disambiguation_link),str(mn_nd_indx),str(redirect_link),str(mn_nd_indx),str(proprty),str(wiki_pages_lst),str(indx_count)))
			 	
			 	elif nw_nd_flg == 0:
			 	
			 		node_new = graph.cypher.execute("""MATCH (a : `%s`) where a.node_name = "%s" set a.redirects_%s = "%s", a.wiki_page_%s = "%s", a.proprty_%s = "%s", a.wiki_pages_lst = "%s" ,a.index_count = "%s" """%(str(current_word_label),str(current_word),str(indx_count),str(disambiguation_link),str(indx_count),str(redirect_link),str(indx_count),str(proprty),str(wiki_pages_lst),str(indx_count)))

			flag=0
			
			if prev_word and prev_word_label:
				
				prev_word_label = prev_word_label.replace(".","")
				prev_word = prev_word.replace(".","")
			  	
			  	#finding relationship
				
				belongs = graph.cypher.execute("""MATCH (n:`%s`)-[r:wiki_belongs]->(m:`%s`) WHERE n.node_name = "%s" AND m.node_name = "%s" return r """%(str(prev_word_label),str(current_word_label),str(prev_word),str(current_word)))
				
		
				if belongs:
					#increasing relationship count 
					print "belongs, ", belongs[0][0]["rel_count"]

					rel_count = int(belongs[0][0]["rel_count"])+1 
					
					indx_count = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.index_count """%(str(current_word_label),str(current_word)))
					indx_count = int(indx_count[0][0]) 
					score=int(belongs[0][0]["wiki_score"])+1
					exist_rel = eval(belongs[0][0]["rel"])
					# updating relation_score and relation wiki_page
								 
					
					
					
					
					if redirect_link not in exist_rel.keys():
						
						exist_rel.update({redirect_link:indx_count})
						rel = "%s"%(exist_rel)
						# updating relationship 
						rel_update = graph.cypher.execute("""MATCH (n:`%s`)-[r:wiki_belongs]->(m:`%s`) WHERE n.node_name="%s" AND m.node_name = "%s" set  r.rel = "%s",r.rel_count = "%s"  RETURN r"""%(str(prev_word_label),str(current_word_label),str(prev_word),str(current_word),str(rel),str(rel_count)))
						# print "updated between ",current_word,prev_word 
						# print "updated relation ", rel
					 
						
					
					rel_update=graph.cypher.execute("""MATCH (n:`%s`)-[r:wiki_belongs]->(m:`%s`) WHERE n.node_name='%s' AND m.node_name ='%s' set r.wiki_score = '%s' """%(str(prev_word_label),str(current_word_label),str(prev_word),str(current_word),str(score)))
					
					
					flag=1

		  		if (flag==0):
			
			  		indx_count = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a.index_count """%(str(current_word_label),str(current_word)))
					indx_count = int(indx_count[0][0])
					
					node1 = graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a"""%(str(prev_word_label),str(prev_word)))
											
			  		node1=node1[0][0]
			  
			  		node2=graph.cypher.execute("""MATCH (a: `%s`) where a.node_name = '%s' return a"""%(str(current_word_label),str(current_word)))
			  		node2=node2[0][0]
			  		dic= {}
			  		# setting score between two nodes and creating relation as rel_indx_count 
			 	 	dic["wiki_score"] = 1
			 	 	temp_dic = []
			 	 	rel_dic = {redirect_link:indx_count}
			 	 	dic["rel"] = "%s"%(rel_dic)
			 	 	dic["rel_count"] = 1
			 	 	
			  		graph.create(Relationship(node1 , ("wiki_belongs",dic),node2))
			  		
				  					
	 	else:
		  		# if relationship is not found 
				flag = 0 

				# for single Entity 
				if current_word == redirect_link or current_word in list(disambiguation_link) :
					flag = 1
				
				print "redirect_link :: ",redirect_link
				wiki_pages_lst = "%s"%[(redirect_link)]
				
				print "first wiki_pages_lst", wiki_pages_lst
				
				# node exists as single entity all prop will be under  _0 if not flag = 0  and redirects will start from 1 
				if flag == 1 :
					crnt_node=Node(str(current_word_label),node_name=str(current_word).replace(".",""),redirects_main = str(disambiguation_link),disambiguation_status = str(disambiguation_status),wiki_page_0 = str(redirect_link),redirect_status = str(redirect_status),proprty_0 = str(proprty),wiki_self_count=1,wiki_pages_lst = wiki_pages_lst,index_count = 0)
				
				elif flag == 0  :
					crnt_node=Node(str(current_word_label),node_name=str(current_word).replace(".",""),redirects_1 = str(disambiguation_link),disambiguation_status = str(disambiguation_status),wiki_page_1 = str(redirect_link),redirect_status = str(redirect_status),proprty_1 = str(proprty),wiki_self_count=1,wiki_pages_lst = str(wiki_pages_lst),index_count = 1)
				
				
				graph.create(crnt_node)
			
			  	if prev_word and prev_word_label:
			  		
			  		prev_word_label = prev_word_label.replace(".","")
					prev_word = prev_word.replace(".","")
			
				 	node1=graph.cypher.execute("""MATCH (n: `%s`) where n.node_name = '%s' return n"""%(str(prev_word_label),str(prev_word)))
				  	
				  	node1 = node1[0][0]
				  	dic ={}
				  	dic["wiki_score"] = 1
			 	 	rel_dic = {redirect_link:1}
			 	 	dic["rel"] = "%s"%(rel_dic)
 			 	 	dic["rel_count"] = 1
 				  	print "first time ", dic
				  	graph.create(Relationship(node1 , ("wiki_belongs",dic),crnt_node))
				  	
	except Exception as e:
		et,ev,etr=sys.exc_info()
		error_log.write(str(list_of_dic_from_mongo)+"\n")
  		print "EXCEPTION IN CREATING NODES :: "+ str(e)  
  		print etr.tb_lineno,"  err line num"


def wordPrefixCheck(word):
  	word_label = word[0:2]
	if word[0] in wc.prefix:
		
   		if word_label in wc.prefix[word[0]]:
			return True
	else:
		return False



# list_of_dic_from_mongo = [{	"real_link":"mount carmel indiana",
# 					"property":["state","university"],
# 					"from_link": ["mt carmel in","mount carmel in","mount carmel indiana"],
# 					"redirect":1 
# 				},{"from_link":"mount","real_link":"mount","property":["state","university"],"redirect":0},
# 				{"from_link":"google","real_link":"google","property":["state","university"],"redirect":0},
# 				{"from_link":"yahoo","real_link":"yahoo","property":["company","organization"],"redirect":0},
# 				{"from_link":"google college","real_link":"google college","property":["state","university"],"redirect":0}, 
# 				{"from_link":"google college","real_link":"google college","property":["state","university"],"redirect":0},
# 				{"from_link":"google college","real_link":"google college","property":["state","university"],"redirect":0},
# 				{"from_link":"mt carmel in","real_link":"mount carmel indiana","property":["state","university"],"redirect":0},
# 					{"from_link":"mount carmel in","real_link":"mount carmel indiana","property":["state","university"],"redirect":0},
# 					{"from_link":"mount carmel indiana","real_link":"mount carmel indiana","property":["state","university"],"redirect":0},
# 					{"from_link":"mount carmel indiana","real_link":"tested done","property":["state","university"],"redirect":0}
# 				]


def index_main(list_of_dic_from_mongo):

	for dic_from_mongo in list_of_dic_from_mongo :	
		global ct

		try: 	
			
			if dic_from_mongo["redirect"]:
				sentence = dic_from_mongo["real_link"]
				print "sentence direct " , sentence
				disambiguation_link = dic_from_mongo["from_link"]	
				redirect_link = sentence
				redirect_status = 1
				disambiguation_status = 0
				proprty  = dic_from_mongo["property"]
				change_status =1
				redirect = 1

			else :
				
				
				sentence = dic_from_mongo["from_link"]
				print "sentence from link" , sentence
				disambiguation_link = [sentence] #making single str into list
				redirect_link = dic_from_mongo["real_link"]
				disambiguation_status = 1
				redirect_status = 0
				proprty = dic_from_mongo["property"]
				change_status = 1
				redirect = 0 

			index_log.write(str(list_of_dic_from_mongo)+"\n")
			proprty = dic_from_mongo["property"]
			
			sentence = sentence.lower().replace("'","")
			print "sentence   ",sentence
			sentence = sentence.strip() 
			words_list = sentence.split(" ",3)
			
			dic={}
			for i in range(len(words_list)):

				
				current_word = words_list[i].strip()
				
			  	current_word_label = "rd_new_"+current_word[0]
			  	if wordPrefixCheck(current_word):
			  		current_word_label = "rd_new_"+current_word[0:2]
			  		if i!=0:
			  			
			  			prev_word = words_list[i-1].strip()
			  			prev_word_label = "rd_new_"+prev_word[0]
			  			if wordPrefixCheck(prev_word):
			  				prev_word_label = "rd_new_"+prev_word[0:2]
			  				
			  			nodeIndex(current_word_label,current_word,disambiguation_link,disambiguation_status,redirect_link,redirect_status,proprty,change_status,redirect,prev_word_label,prev_word)
			  		else:
			  			nodeIndex(current_word_label,current_word,disambiguation_link,disambiguation_status,redirect_link,redirect_status,proprty,change_status,redirect)
			  	else:
			  		if i!=0:
			  		
			  			prev_word = words_list[i-1].strip()
			  			prev_word_label = "rd_new_"+prev_word[0]
			  			if wordPrefixCheck(prev_word):
			  				prev_word_label = "rd_new_"+prev_word[0:2]
			  			
			  			nodeIndex(current_word_label,current_word,disambiguation_link,disambiguation_status,redirect_link,redirect_status,proprty,change_status,redirect,prev_word_label,prev_word)
			  		else:
			  			nodeIndex(current_word_label,current_word,disambiguation_link,disambiguation_status,redirect_link,redirect_status,proprty,change_status,redirect)
			  		
			print "_________________________________________________________________________"
			
		except Exception as e:
			error_log.write(str(list_of_dic_from_mongo)+"\n")
			et,ev,etr=sys.exc_info()
			print "EXCEPTION IN CHECKING LABELS "+ str(e)
			print etr.tb_lineno,"  err line num"


# index_main(list_of_dic_from_mongo)




