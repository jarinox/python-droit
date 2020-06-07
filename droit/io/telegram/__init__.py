import json, telegram, time


TOKEN = open("droit/io/telegram/TOKEN", "r").read().strip()
bot = telegram.Bot(token=TOKEN)


def getStatus():
	return json.loads(open("droit/io/telegram/status.json", "r").read())

def setStatus(status):
	open("droit/io/telegram/status.json", "w").write(json.dumps(status))


def getinput(question):
	running = True
	status = getStatus()
	inp = ""
	while(inp == ""):
		updates = bot.getUpdates()
		for update in updates:
			uval = True
			for state in status:
				if(state["uid"] == update.update_id):
					uval = False
					break
			if(uval):
				inp = update.message.text
				status.append({"uid": update.update_id, "state": "wait"})
				setStatus(status)
				break
		if(inp == ""):
			time.sleep(1)
	return inp
	

def output(text):
	updates = bot.getUpdates()
	status = getStatus()
	uid = 0
	i = -1
	for state in status:
		if(state["state"] == "wait"):
			uid = state["uid"]
		i += 1
	if(uid != 0):
		for update in updates:
			if(update.update_id == uid):
				update.message.reply_text(text)
				status[i]["state"] = "answered"
				status[i]["answer"] = text
				setStatus(status)
				break


def binaryQuestion(question):
	print("not implemented")
	
