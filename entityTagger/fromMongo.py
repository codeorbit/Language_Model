# -*- coding: utf-8 -*-
import json
import re ,string
import db_config
import unicodedata
from redirect_indexing_new import index_main
from py2neo import Graph,Node,Relationship,authenticate
authenticate("localhost:7474",db_config.username,db_config.password)
graph = Graph()
import urllib
import pymongo
from srmse import text
client = pymongo.MongoClient()
mdb = client["cron-dbpedia"]
col = mdb["redirects_en"]
instance_col = mdb["instance-types-transitive_en"] 
instance_list = instance_col.find()
instance_count = instance_col.find().count()
print instance_count
 
index_log = open("indexlogFromMongo.txt","a")
doc_list = col.find(no_cursor_timeout=True) #To avoid pymongo.errors.CursorNotFound
doc_count = doc_list.count()

def splittingCamelCase(word):
	split_list = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
	sentence = " ".join(split_list).lower()
	return sentence

def remove_punctuations(s):
        try:
        	#regex without .
        	exclude=set(string.punctuation.replace(".",""))
        	l=[]
        	
        	for ch in s:
        		if ch in exclude:
        			#punc
        			l.append(" ")
        		else:
        			l.append(ch)
                output = ''.join(l)
                output = re.sub(r'\s+'," ", output).strip()
                return output
        except Exception as e:
		print "[ERROR] in remove_punctuations()"
		raise Exception

def link_filter(original_link):
	try :
		original_link = original_link.replace(",_"," ").replace("#dot#",".")
		original_link = text.removeStopWords(original_link)
		#print "inside ",original_link
		original_link = remove_punctuations(original_link)
		#print "outside ",original_link
		original_link = str(filter(lambda x:ord(x)>31 and ord(x)<128,original_link)).strip().lower()
		
		
		
		return original_link
	except Exception as e:
		return original_link
			
for ind in range(doc_count):
	doc=None
	try:
		doc=doc_list[ind]
	except Exception as e:
		print e
		continue
	list_of_doc=[]
	doc_dic_batch = {}
	ct=1
	try:
		
		instance_doc = instance_col.find_one({"_id":doc["_id"]})
		
		
		prop = instance_doc["dbc"]
		prop_list = []
		for i in prop:
			rmvd_base_url = i.replace("http://dbpedia.org/ontology/","")
			filtered_camel_case = splittingCamelCase(rmvd_base_url)
			filtered = link_filter(filtered_camel_case)
			prop_list.append(filtered) 
		
		
		doc_dic_batch["property"] = prop_list
	except Exception as e:
		doc_dic_batch["property"] = [""]
		
				
	print "------------------------------------------------------"
	
	link = doc["_id"].replace("http://dbpedia#dot#org/resource/","").encode("utf-8")
	
	#print unicodedata.normalize('NFD',link).encode('ascii','ignore')
	#print (urllib.quote(link))
	#test.write(urllib.quote(link)+"\n")
	#urllib.quote(link)
	if "Template:" in link:
		continue
	else:
		print link
		filtered_link = link_filter(link)
		print "after filter",filtered_link
		doc_dic_batch["real_link"] = filtered_link
		redirects = doc["from"]
		filtered_redirects_link = []
		for redirect_link in redirects:
			org_redirect_link = redirect_link.replace("http://dbpedia.org/resource/","")
			filtered_org_redirect_link = link_filter(org_redirect_link)
			filtered_redirects_link.append(filtered_org_redirect_link)
		
		doc_dic_batch["from_link"] = filtered_redirects_link
		doc_dic_batch["redirect"] = 1
		
		list_of_doc.append(doc_dic_batch)
		
		for indi_link in filtered_redirects_link:
			temp_dic = {}
			temp_dic["from_link"] = indi_link
			temp_dic["redirect"] = 0
			temp_dic["real_link"] = filtered_link 
			temp_dic["property"] = doc_dic_batch["property"]
			list_of_doc.append(temp_dic)
			
		
		index_main(list_of_doc)
		index_log.write((doc["_id"].encode("utf-8")+"\n"))
		
		
	print "========================================================="
