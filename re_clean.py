import json
from email.utils import parseaddr
docs = []
new_info = []
## get field values from docs
### @lt: content list
### @value: field value
def getValues(lt, value):
	entry = [x for x in lt if x.startswith(value)]
	return entry
## read docs
def readFiles():
	with open("file_path.txt", "r") as f:
		for row in f:
			docs.append(row.rstrip())
## data cleaning process
### @item: documents file path
def dataCleaning(item):
	with open(item, "r") as f:
		text = [x.rstrip() for x in f.readlines()]
		text = list(filter(None, text))
		pre = text.index(getValues(text, "X-FileName:")[0])
		header = text[:pre+1]
		body = text[pre+1:]
		receiver = getValues(header, "To:")
		## check is there is a receiver
		if not receiver:
			pass
		else:
			receiver = receiver[0][4:].split(",")
			receiver = list(filter(None, receiver))
			receiver = [x.strip() for x in receiver]
			cc = getValues(header, "Cc")
			if not cc:
				pass
			else:
				cc = cc[0].split(":")[1].split(",")
				cc = [x.strip() for x in cc]
				cc = list(filter(None, cc))
			receiver.extend(cc)
			receiver = [parseaddr(x)[1] for x in receiver]
			sender = getValues(header, "From:")[0].split(":")[1].lstrip()
			## get mid
			mid = getValues(header, "Message-ID:")[0].split(":")[1].lstrip()
			## get date
			dt = getValues(header, "Date:")[0].split(":")[1].lstrip()
			## get body length
			body = list(map(lambda x:x.strip(), body))
			bd = " ".join(body).strip()
			bd_len = len(bd.split())
			## get subject
			sub = getValues(header, "Subject:")[0].split(":")[1]
			## write to dictionary
			for each in receiver:
				dc = {}
				writeToNode(dc, each, sender, mid, dt, sub, bd_len, bd)
				new_info.append(dc)
## write data to node dictionary
### @dc: dictionary that contains extracted edge info
### @receiver_email": receiver email
### @sender_email: sender email
### @mid: message id
### @date: message date
### @sub: message subject
### @ble: message body length
### @bd: email content
def writeToNode(dc, receiver_email, sender_email, mid, date, sub, ble, bd):
	dc["receiver"] = receiver_email
	dc["sender"] = sender_email
	dc["mid"] = mid
	dc["date"] = date
	dc["subject"] = sub
	dc["body_len"] = ble
	dc["body"] = bd
def writeFiles():
	with open("new_info.json", "w") as outfile:
		json.dump(new_info, outfile, indent = 4,  sort_keys = True)
def run():
	readFiles()
	for item in docs:
		## pass if UnicodeDecodeError is thrown
		try:
			dataCleaning(item)
		except UnicodeDecodeError:
			pass
	writeFiles()
	print("finish!")
run()