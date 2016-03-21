from bottle import route,run,response
from autoComplete.middleware import autoMain
# from load_data import NWORDS
from spellcheck import correct
from nearestWord import nearestWordMain
from wordSegment.wordSegment import segment
import entityTagger.getEntity as GE
@route('/')
def hello():
	return "Welcome to the language model"

@route('/language_model/')
def default_list():
    return {" /wordsegment/words":"separated words" , \
   			" /spellcheck/incorrectWord ":" correct word", \
       		" /nearestwords/word" : "words near to the given word", \
    		" /nearestWords/word/number" : "return n words near to the given word where n is number", \
   			" /autocomplete/word": "will return the list of related words",\
   			" /getentity/query": "will detect entities and return domain/property "}

@route('/language_model/wordsegment/<name>',method = 'GET')
def wordSegment(name = " "):
	words = segment(name)
	return {"words" : words}	

@route('/language_model/nearestword/<name>/<top_n>',method = 'GET')
def nearestWords(name = " ",top_n = " "):
	return {"tags":(nearestWordMain(name,top_n))}

@route('/language_model/nearestword/<name>',method = 'GET')
def nearestWords(name = " "):
	return {"tags":(nearestWordMain(name,5))}

@route('/language_model/getentity/<name>',method = 'GET')
def getEntity(name = " "):
	query = name
	entity_info = GE.querySegment(name)
	entity_data = entity_info["entity_details"]
	entities = entity_info["segments"]
	return {"query": query,"entityData": entity_data,"Entities":entities}

@route('/language_model/spellcheck/<name>',method = 'GET')
def spellcheck(name = " " ):
    return {"candidates":correct(name)}


@route('/language_model/autocomplete/<name>', method='GET')
def automplete_show(name = " "):
	response.content_type = 'application/json'   
	response.set_header('Cache-Control', 'no-cache')

   	return {"content": autoMain(name)}

run(host='localhost', port=7777, debug=True)