# -*- coding: utf-8 -*-
from app import app
from flask import request, jsonify
from time import gmtime, strftime

dict = {}

@app.route('/')
@app.route('/index')
def index():
    return "Server working"

@app.route('/dictionary', methods = ['GET', 'POST', 'DELETE', 'PUT'], defaults={'path': ''})
@app.route('/dictionary/<path:path>', methods = ['GET', 'DELETE', 'PUT'])
def dictionary(path):
	#no switch case operation in python?
	if request.method == 'GET':
		value = dict.get(path)
		if value:
			response = { 'result': value, 'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
			return jsonify(response)
		else:
			response = { 'result': value, 'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
			return '', 404
	elif request.method == 'POST':
		json = request.json #request.get_json() введен только в 0.10 и на версии 0.9 альтернативы .json нет
		key = json.get("key")
		value = json.get("value")
		if dict.get(key):
			return '', 409
		elif (not key) or (not value):
			return '', 400
		else:
			dict[key] = value
			response = { 'result': dict.get(key), 'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
			return jsonify(response)
	elif request.method == 'DELETE':
		if dict.get(path):
			dict.pop(path)
		response = { 'result': dict.get(path), 'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
		return jsonify(response), 200
	elif request.method == 'PUT':
		json = request.json #request.get_json() введен только в 0.10 и на версии 0.9 альтернативы .json нет
		value = json.get("value")
		if path == '':					#В техзадании Route: /dictionary/<key>, но при этом запрос "аналогичен
			key = json.get("key") 	    #POST", т.е. ключ в параметрах, использовал комбинированный подход
		else:
			key = path
		if (not key) or (not value):
			return '', 409
		elif dict.get(key):
			dict[key] = value
			response = { 'result': dict.get(key), 'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
			return jsonify(response)
		else:
			return '', 404
	else:
		return "Not implemented", 501