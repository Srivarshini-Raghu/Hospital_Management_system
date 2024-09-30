import datetime
import locale
from flask import Flask, jsonify, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
import pymongo
import requests
from random import randrange



app = Flask(__name__)
title = "Hospital management"
heading = "HOSPITAL MANAGEMENT"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.hospital    # database
coll1 = db.Patients #collection name1
coll2 = db.Doctors #collection name2


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
@app.route("/patients")
def lists ():
	#Display the all Tasks
	todos_l = coll1.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/d")
@app.route("/doctors")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = coll2.find()
	a2="active"
	return render_template('docindex.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/queries")
def completed ():
	#Display the Completed Tasks
	todos_l = coll2.find()
	a3="active"
	return render_template('qryindex.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])    
def action ():    
    #Adding a Task
	age=request.values.get("age")    
	pat_id=request.values.get("pat_id")
	name=request.values.get("name")
	admission_date=request.values.get("admission_date")    
	medicine=request.values.get("medicine")
	room_no=request.values.get("room_no")    
	Dr_referred=request.values.get("Dr_referred")
	fees=request.values.get("fees")
	coll1.insert_one({ "pat_id":pat_id,"name":name, "age":age, "admission_date":admission_date, "medicine":medicine,"room_no":room_no,"Dr_referred":Dr_referred,"fees":fees})    
	return redirect("/patients")

@app.route("/actiondoc", methods=['POST'])    
def actiondoc ():    
    #Adding a Task    
	name=request.values.get("name")
	specialization=request.values.get("specialization")
	date_of_joining=request.values.get("date_of_joining")    
	coll2.insert_one({ "name":name, "specialization":specialization, "date_of_joining":date_of_joining})    
	return redirect("/doctors")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=coll1.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	id=request.values.get("_id")
	age=request.values.get("age")    
	pat_id=request.values.get("pat_id")
	name=request.values.get("name")
	admission_date=request.values.get("admission_date")    
	discharge_date=request.values.get("discharge_date")
	room_no=request.values.get("room_no")    
	Dr_referred=request.values.get("Dr_referred")
	fees=request.values.get("fees")
	coll1.update_one({"_id":ObjectId(id)}, {'$set':{ "pat_id":pat_id,"name":name, "age":age, "admission_date":admission_date, "discharge_date":discharge_date,"room_no":room_no,"Dr_referred":Dr_referred,"fees":fees }})
	return redirect("/")

@app.route("/updatedoc")
def docupdate ():
	id=request.values.get("_id")
	task=coll2.find({"_id":ObjectId(id)})
	return render_template('docupdate.html',tasks=task,h=heading,t=title)

@app.route("/action4", methods=['POST'])
def action4 ():
	#Updating a Task with various references
	id=request.values.get("_id")
	name=request.values.get("name")
	specialization=request.values.get("specialization")    
	date_of_joining=request.values.get("date_of_joining")    
	coll2.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "specialization":specialization, "date_of_joining":date_of_joining }})
	return redirect("/d")


@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = coll1.find({refer:ObjectId(key)})
	elif(refer=='age'):
			#x=key.split('-')
			#todos_l = coll1.find({'admission_date': { '$gt':datetime.datetime(int(x[0]),int(x[1]),int(x[2]))} })
			todos_l = coll1.find({'age' : int(key) })
	elif(refer=='admission_date'):
			x=key.split('-')
			todos_l = coll1.find({'admission_date': { '$eq':datetime.datetime(int(x[0]),int(x[1]),int(x[2]))} })
			
	else:
			todos_l = coll1.find({refer:key})	
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/docsearch", methods=['GET'])
def docsearch():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = coll2.find({refer:ObjectId(key)})
	else:
		todos_l = coll2.find({refer:key})
	#for doc in todos_l:
	#	print(doc)	
	return render_template('docsearch.html',todos=todos_l,t=title,h=heading)

@app.route("/namestartaction", methods=['POST'])
def namestart():
	#Searching a Task with various references
	key=request.values.get("nmst")
	print(key)
	todos_l = coll1.find({'name':{'$regex' : key}})	
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/ageaftaction", methods=['POST'])
def admaft():
	#Searching a Task with various references
	key=int(request.values.get("ageaft"))
	todos_l = coll1.find({'age':{ '$gt' : key }})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/admdaysaction", methods=['POST'])
def admdays():
	#Searching a Task with various references
	key=request.values.get("admdays").split(',')
	todos_l = coll1.find({'Dr_referred':{'$in' : key}})	
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/cityaction", methods=['POST'])
def city():
	#Searching a Task with various references
	key=request.values.get("city")
	todos_l = coll1.find({'address.city':key})	
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/mediaction", methods=['POST'])
def medi():
	#Searching a Task with various references
	key=request.values.get("medi")
	todos_l = coll1.find({'medicine':key})	
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/specializeaction", methods=['POST'])
def specialize():
	#Searching a Task with various references
	key=request.values.get("specialize")
	todos_l = coll2.find({'specialization':key})	
	return render_template('docsearch.html',todos=todos_l,t=title,h=heading)

@app.route("/patfeesaction", methods=['POST'])
def patfees():
	#Searching a Task with various references
	todos_l = coll1.find().sort('fees',-1).limit(1)
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/totfeesaction", methods=['GET'])
def totfees():
	#Searching a Task with various references
	key=request.values.get("totfees")
	todos_l = coll1.aggregate([ {'$match' : { 'Dr_referred' : key } }, {'$group' : { '_id' : '$Dr_referred' , '     Total_Fees_collected': {'$sum' : '$fees'}} }])
	return render_template('totfeeslist.html',todos=todos_l,t=title,h=heading)

@app.route("/maxfeesaction", methods=['POST'])
def maxfees():
	#Searching a Task with various references
	key=request.values.get("maxfees")
	todos_l = coll1.aggregate([ {'$match' : { 'Dr_referred' : key } }, {'$group' : { '_id' : '$Dr_referred' , '     Maximum_Fees_collected': {'$max' : '$fees'}} }])	
	return render_template('totfeeslist.html',todos=todos_l,t=title,h=heading)

@app.route("/minfeesaction", methods=['POST'])
def minfees():
	#Searching a Task with various references
	key=request.values.get("minfees")
	todos_l = coll1.aggregate([ {'$match' : { 'Dr_referred' : key } }, {'$group' : { '_id' : '$Dr_referred' , '      Minimum_Fees_collected': {'$min' : '$fees'}} }])
	return render_template('totfeeslist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()