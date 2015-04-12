import requests
import io, json
import pprint
import time
import operator
import calendar
#import glob

key = ""

pp = pprint.PrettyPrinter(indent=4)

def callAPI(url, param):
	global key
	#print("Call: https://na.api.pvp.net/{0}{1}{2}{3}".format(url, param, "&api_key=", key))
	return requests.get("https://na.api.pvp.net/{0}{1}{2}{3}".format(url, param, "&api_key=", key))

def writeURFGames(matches):
	with io.open('urf.txt', 'a+', encoding='utf-8') as f:
		for item in matches:
			f.write(unicode("%s\n" % item))
		print("wrote {0} matches".format(len(matches)))

def getURFMatchesByTime(time):
	apiStr = "api/lol/na/v4.1/game/ids?beginDate="
	print("Getting URF Data for {0}...".format(time))
	global key
	matchesCall = callAPI(apiStr, time)
	matches = matchesCall.json()
	#print(matches)
	return matches

def getURFMatches():
	currentTime = calendar.timegm(time.gmtime())
	print(currentTime)
	correctedTime = currentTime - (currentTime%300) + 300
	print(correctedTime)
	eightHours = 60 * 60 * 8
	for timeBucket in range(correctedTime-eightHours, correctedTime, 300):
		writeURFGames(getURFMatchesByTime(str(timeBucket)))
		time.sleep(1.2) #sleep for rito

def main():
	getURFMatches()

if __name__ == "__main__":
	main()