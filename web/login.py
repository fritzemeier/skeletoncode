import sys,os
import requests

def parse_args(INFO):

	for i in range(1,len(sys.argv)):

		CURR = sys.argv[i]
		KEY = CURR.split("=")[0]
		VAL = CURR.strip(KEY+"=")

		if KEY in INFO.keys():
			INFO[KEY] = VAL

	return INFO

def parse_params(STR):

	DICT = {}

	for ENTRY in STR.split(","):
		PARAM = ENTRY.split('=')[0]
		VAL = ENTRY.strip(PARAM+'=')
		DICT[PARAM] = VAL

	return DICT

def print_dict(DICT):
	for i in DICT.keys():
		if DICT[i]:
			print(i+": "+DICT[i])

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
	if INFO["DATA"] and INFO["HEADERS"]:

		F_HEAD = parse_params(INFO["HEADERS"])
		F_DATA = parse_params(INFO["DATA"])

		if SPEC["UPARAM"]:
			F_DATA[SPEC["UPARAM"]] = NAME
		else:
			F_DATA["username"] = NAME

		if SPEC["PPARAM"]:
			F_DATA[SPEC["PPARAM"]] = PASS
		else:
			F_DATA["password"] = PASS

		print("DATA: ")
		print_dict(F_DATA)
		print("HEADERS: ")
		print_dict(F_HEAD)

#		if not all(VAL == "" for VAL in SPEC.values()):
#			if SPEC["UPARAM"]:


		REQ = requests.Request("POST",INFO["URL"], headers=F_HEAD,data=F_DATA)
		print_request(REQ)

		RES = requests.post(INFO["URL"], headers=F_HEAD,data=F_DATA)
		print_response(RES)

	elif INFO["DATA"]:
		print(2)
	elif INFO["HEADERS"]:
		print(3)
	else:
		print(99)

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
		"RAND":"",
		"FAIL":""

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
