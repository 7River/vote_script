import json
import requests
import time
from datetime import datetime
import winsound
from colorama import Fore, Back, Style,init
#winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
init(autoreset=True)

def split_strings(string):
	if(string[len(string)-1]=="<"):
		return string[:-1].split(":")
	return string.split(":")

def get_timer(string):
	return (int(string[0][:-1])*60)+(int(string[1][:-1]))
def color(string,color):
	co=Fore.WHITE
	if(color=="green"):
		co=Fore.GREEN
	elif(color=="red"):
		co=Fore.RED
	return co+string

def login():
	global sessions
	global session_validity
	sessions=[]
	session_validity=[]
	print("start logging ...")
	try:
		#init connection sessions
		for data in auth_data:
			sessions.append(requests.session())
			session_validity.append(1)
			
		#start connections	
		for i in range(0,len(sessions)):
			data=sessions[i].post(loginurl,auth_data[i])
			if((str(data.content)).find("Dashboard")==-1):
				print(color("[ERR] Access to "+auth_data[i]["username"],"red") )
				session_validity[i]=0
			else:
				print(color("[OK] Access to "+auth_data[i]["username"],"green") )
		print()
	except Exception as e:
		print(e)

def vote():
	try:
	
		login()
		print("Start Voting...")
		print("check time using ",auth_data[session_validity.index(1)]["username"])
		response=sessions[session_validity.index(1)].get("https://accounts.rzesua.com/index.php")
		res=str(response.content)
		if(res.find('<button type="button" class="btn btn green" style="padding: 13px 22px;">You can now vote</button>')==-1):
			first_index=res.find('<div class="alert alert-warning home-warning">You can vote in:')
			down_time_till_vote=get_timer(split_strings(res[first_index+71:first_index+71+6]))
			print(color("[NO] Vote not Done Time","red"))
			print(color("	reason: time not elapsed","red"))
			print("voting after ",down_time_till_vote," min")
			print()
			time.sleep((down_time_till_vote+5)*60)
		else:
			print("voting!!")
			for i in range(0,len(sessions)):
				if(session_validity[i]==1):
					sessions[i].get("https://accounts.rzesua.com/vote.php")
					print(color("[OK] Voting using username: "+auth_data[i]["username"],"green"))

			print("[OK] Vote Done Time:",datetime.now())
			print()
			time.sleep(7500)
	
	
	except Exception as e:
		
		print(color("err while voting re init prg","red"))
		print(e)
		vote()
		


sessions=[]
session_validity=[]
loginurl='https://accounts.rzesua.com/login.php?'
auth_data = (json.load(open('accounts.json')))["auth_data"]

while True:
	vote()
