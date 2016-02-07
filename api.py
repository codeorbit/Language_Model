from bottle import route,run,response
from middleware import autoMain
import tags
@route('/')
def hello():
	return "Welcome to the language model"

@route('/language_model/')
def default_list():
    return "Welcome to the language model"

@route('/get_tags/<name>/<top_n>',method = 'GET')
def get_tags(name = " ",top_n = " "):
	
	return {"tags":(tags.tagsMain(name,top_n))}

@route('/get_tags/<name>',method = 'GET')
def get_tags(name = " "):
	return {"tags":(tags.tagsMain(name,5))}

@route('/autocomplete/<name>', method='GET')
def automplete_show(name = " "):
	
	response.content_type = 'application/json'   
	response.set_header('Cache-Control', 'no-cache')
   	return {"content": autoMain(name)}

run(host='localhost', port=7777, debug=True)

