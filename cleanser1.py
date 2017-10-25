import json
from email.utils import parseaddr
import re
class cleanser1:
	def __init__(self):
		self.docs = []
		self.node = []
		self.edge = []
		self.email_unique = []
	## get field values from docs
	### @lt: content list
	### @value: field value
	def getValues(self, lt, value):
		entry = [x for x in lt if x.startswith(value)]
		return entry
	## write data to node dictionary
	### @dc: dictionary that contains extracted node info
	### @key: key for dictionary
	### @ty: type of the user, i.e. sender or receiver
	### @mid: message id
	### @date: message date
	### @sub: message subject
	### @ble: message body length
	def writeToNode(self, dc, key, ty, mid, date, sub, ble):
		dc["_key"] = key
		dc["type"] = ty
		dc["mid"] = mid
		dc["date"] = date
		dc["subject"] = sub
		dc["body_len"] = ble
	## write data to edge dictionary
	### @dc: dictionary that contains extracted edge info
	### @receiver_email": receiver email
	### @sender_email: sender email
	### @mid: message id
	### @date: message date
	### @sub: message subject
	### @ble: message body length
	### @fd: employee folder
	def writeToEdge(self, dc, receiver_email, sender_email, mid, date, sub, ble, fd):
		dc["_from"] = "people/" + receiver_email
		dc["_to"] = "people/" + sender_email
		dc["mid"] = mid
		dc["date"] = date
		dc["subject"] = sub
		dc["body_len"] = ble
		dc["employee"] = fd
	## write unique email to json file
	### @ls: list contains all unique emails
	def writeUniqueEmail(self, ls):
		ls = list(set(ls))
		temp = []
		for each in ls:
			dc = {}
			dc["_key"] = each
			temp.append(dc)
		with open("email_unique.json", "w") as outfile:
			json.dump(temp, outfile, encoding='utf8', indent = 4,  sort_keys = True)
	## read docs
	def readFiles(self):
		with open("file_path.txt", "r") as f:
			for row in f:
				self.docs.append(row.rstrip())
	## data cleaning process
	### @item: documents file path
	def dataCleaning(self, item):
		with open(item, "r") as f:
			s = item.split("/")[-3]
			node_d_r = {} ## receiver node dictionary
			node_d_s = {} ## sender node dictionary
			edge_d = {} ## edge dictionary
			text = [x.rstrip() for x in f.readlines()]
			text = filter(None, text)

			## get receiver
			receiver = self.getValues(text, "To")
			## check is there is a receiver
			if not receiver:
				pass
			else:
				sender = self.getValues(text, "From")[0].split(":")[1].lstrip()
				## get mid
				mid = self.getValues(text, "Message-ID")[0].split(":")[1].lstrip()
				
				## get date
				dt = self.getValues(text, "Date")[0].split(":")[1].lstrip()
				
				## get body length
				pre = self.getValues(text, "X-FileName")[0]
				index = text.index(pre) + 1
				body = text[index:]
				bd = " ".join(body).lstrip()
				bd_len = len(bd.split())
				
				## get subject
				sub = self.getValues(text, "Subject")[0].split(":")[1]

				## get receiver email
				r_e = receiver[0].split(":")[-1].split(",")
				
				## write to dictionary
				for each in r_e:
					each = each.lstrip()
					each = parseaddr(each)[1]
					sender = parseaddr(sender)[1]
					if not re.match(r"[^@]+@[^@]+\.[^@]+", each) or not re.match(r"[^@]+@[^@]+\.[^@]+", sender):
						pass
					else:
						if each and sender:
							if len(each.split("/")) > 1:
								pass
							else:
								## remove strange patterns in emails
								each = re.sub(r"\".'\"", ".", each)
								sender = re.sub(r"\".'\"", ".", sender)
								each = each.replace("\"", "")
								sender = sender.replace("\"", "")
								each = each.replace("'\"", "")
								sender = sender.replace("'\"", "")
								each = each.replace("&", "")
								sender = sender.replace("&", "")
								self.writeToNode(node_d_s, sender, "sender", mid, dt, sub, bd_len)
								self.writeToNode(node_d_r, each, "receiver", mid, dt, sub, bd_len)
								self.writeToEdge(edge_d, each, sender, mid, dt, sub, bd_len, s)
								self.email_unique.append(sender)
								self.email_unique.append(each)
			self.node.append(node_d_r)
			self.node.append(node_d_s)
			self.edge.append(edge_d)
	def writeFiles(self):
		self.edge = filter(None, self.edge)
		self.node = filter(None, self.node)
		self.writeUniqueEmail(self.email_unique)
		with open("node.json", "w") as outfile:
			json.dump(self.node, outfile, encoding='utf8', indent = 4,  sort_keys = True)
		with open("edge.json", "w") as outfile:
			json.dump(self.edge, outfile, encoding='utf8', indent = 4,  sort_keys = True)
	def run(self):
		self.readFiles()
		for item in self.docs:
			self.dataCleaning(item)
		self.writeFiles()
x = cleanser1()
x.run()