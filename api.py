from bottle import route,run,response
from main import autoMain
@route('/')
def hello():
	return "Welcome to the language model"

@route('/language_model/')
def default_list():
    return "Welcome to the language model"

@route('/autocomplete/<name>', method='GET')
def automplete_show(name = " "):
	
	response.content_type = 'application/json'   
	response.set_header('Cache-Control', 'no-cache')
   	return {"content": autoMain(name)}

@route('/autocomplete/<name>', method='DELETE' )
def node_delete( name=" " ):
    return "DELETE RECIPE " + name

@route('/index/<word>', method='PUT')
def node_save( name=" " ):
    return "SAVE RECIPE " + name

run(host='localhost', port=7777, debug=True)

