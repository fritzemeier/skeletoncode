import sys,os
import requests

def parse_args(INFO):

	MENU = {

		"USER":"String of a single username or list of usernames separated by commas.",
		"PASS":"String of a single password or list of passwords separated by commas.",
		"USERFILE":"Path to a file containing usernames, formatted one per line.",
		"PASSFILE":"Path to a file containing passwords, formatted one per line.",
		"URL":"Full URL to the page to attempt authentication against.",
		"HEADERS":"Add custom headers to the requests.",
		"DATA":"Add custom parameters to the requests.",
		"UPARAM":"Specify the username parameter specific to the request.",
		"PPARAM":"Specify the password parameter specific to the request.",
		"RAND":"Items that may change per request.",
		"FAILSTR":"String which occurs on failed a attempt.",
		"FAILCODE":"Status code that occurs on a failed attempt."

	}

	for i in range(1,len(sys.argv)):

		CURR = sys.argv[i]

		if CURR[0:2] == '--':

			if CURR[2:] == "help":
				print("Multi-Credential Login Tool\n")
				if (i+1) < len(sys.argv) and sys.argv[i+1] in MENU.keys():
					OPT = { sys.argv[i+1]:MENU[sys.argv[i+1]] }
					print_dict(OPT)
				else:
					print_dict(MENU)

				sys.exit()



		KEY = CURR.split("=")[0]

		if KEY in INFO.keys():
			if CURR == "BASIC":
				INFO["BASIC"] = True
				continue

			if CURR == "COOKIE":
				INFO["COOKIE"] = True
				continue

			VAL = CURR[(len(KEY)+1):]

			INFO[KEY] = VAL

	return INFO

def parse_params(STR):

	DICT = {}

	for ENTRY in STR.split(","):
		PARAM = ENTRY.split('=')[0]
		VAL = ENTRY[(len(PARAM)+1):]
		DICT[PARAM] = VAL

	return DICT

def print_dict(DICT):
	for i in DICT.keys():
		if DICT[i]:
			ITEM = i+" "*(10-len(i))
			print("    "+ITEM+"		"+str(DICT[i]))

def print_request(REQ):
	print("HTTP/1.1 {method} {url}\n{headers}\n\n".format( #{body}".format(
		method=REQ.method,
		url=REQ.url,
		headers=REQ.headers
#		body=REQ.body
		))

def print_response(RES):
	print("HTTP/1.1 {status_code}\n{headers}\n\n{body}".format(
		status_code=RES.status_code,
		url=RES.url,
		headers='\n'.join('{}: {}'.format(i,j) for i,j in RES.headers.items()),
		body=RES.content
		))

def request_login(NAME,PASS,INFO,SPEC):

	F_HEAD = {}
	F_DATA = {}

	if INFO["HEADERS"]:
		F_HEAD = parse_params(INFO["HEADERS"])

	if INFO["DATA"]:
		F_DATA = parse_params(INFO["DATA"])

#	if INFO["R_HEAD"]:

	if SPEC["COOKIE"]:
		TMP_REQ = requests.get(INFO["URL"], headers=F_HEAD, allow_redirects=False)
#		print(TMP_REQ.headers)
		F_HEAD["Cookie"] = TMP_REQ.headers["Set-Cookie"].split(";")[0]

	if SPEC["UPARAM"]:
		F_DATA[SPEC["UPARAM"]] = NAME
	else:
		F_DATA["username"] = NAME

	if SPEC["PPARAM"]:
		F_DATA[SPEC["PPARAM"]] = PASS
	else:
		F_DATA["password"] = PASS

	print("HEADERS: ")
	print_dict(F_HEAD)
	print()

	print("DATA: ")
	print_dict(F_DATA)
	print()

#		if not all(VAL == "" for VAL in SPEC.values()):
#			if SPEC["UPARAM"]:

#	if INFO["DATA"] and INFO["HEADERS"]:
	if F_DATA and F_HEAD:

		REQ = requests.Request("POST",INFO["URL"], headers=F_HEAD,data=F_DATA)
#		print_request(REQ)

		RES = requests.post(INFO["URL"], headers=F_HEAD,data=F_DATA)
#		print_response(RES)

#	elif INFO["DATA"]:
	elif F_DATA:
		print(2)
#	elif INFO["HEADERS"]:
	elif F_HEADERS:
		print(3)
	else:
		print(99)

	if SPEC["FAILSTR"] in RES.text:
		print("Fail")
	else:
		print("Success")

def main():

	requestInfo = {
		"URL":"",
		"HEADERS":"",
		"DATA":""
	}

	userData = {

		"USER":"",
		"PASS":"",
		"USERFILE":"",
		"PASSFILE":""

	}

	requestSpecifics = {

		"UPARAM":"",
		"PPARAM":"",
		"R_HEAD":"",
		"R_DATA":"",
		"COOKIE":False,
		"BASIC":False,
		"FAILSTR":"",
		"FAILCODE":""

	}

	if len(sys.argv) > 1:
		requestInfo = parse_args(requestInfo)
		userData = parse_args(userData)
		requestSpecifics = parse_args(requestSpecifics)

	if not all(VAL == "" for VAL in requestInfo.values()):
		print("Request Information")
		print_dict(requestInfo)
		print("")

	if not all(VAL == "" for VAL in userData.values()):
		print("User Data")
		print_dict(userData)
		print("")

	if not all(VAL == "" for VAL in requestSpecifics.values()):
		print("Request Specifics")
		print_dict(requestSpecifics)
		print("")

	if userData["USER"]:

		userArr = userData["USER"].split(",")

		for NAME in userArr:
			#BEGIN PROCESSING/MAKING REQUESTS BELOW

			if userData["PASS"]:

				passArr = userData["PASS"].split(",")

				for PASS in passArr:

					RES = request_login(NAME,PASS,requestInfo,requestSpecifics)



if __name__ == "__main__":
	main()
