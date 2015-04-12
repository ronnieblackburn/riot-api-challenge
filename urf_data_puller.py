import requests
import io, json
import time
import calendar


#load key from file (NEVER share key.txt on GitHub!!)
key = io.open('key.txt', 'r', encoding='utf-8').readline()


def callAPI(url, param):
	"""Calls the API Challenge endpoint with the specific time bucket"""
	global key
	#print("Call: https://na.api.pvp.net/{0}{1}{2}{3}".format(url, param, "&api_key=", key))
	return requests.get("https://na.api.pvp.net/{0}{1}{2}{3}".format(url, param, "&api_key=", key))


def removeDuplicates():
	"""Removes duplicate match IDs from the urf_match_ids.txt file"""
	ids = []
	with open("urf_match_ids.txt", "r") as f:
		for line in f:
			ids.append(line)
	print("Size pre-culling: {0}".format(len(ids)))
	ids = map(str, (sorted(map(int, set(ids)), key=int)))
	print("Size post-culling: {0}".format(len(ids)))
	with open("urf_match_ids.txt", "w") as f:
		for item in ids:
			f.write(unicode("%s\n" % item))

def recordMatchIDs(matches):
	"""records the list of match IDs into the urf_match_ids.txt file"""
	with io.open('urf_match_ids.txt', 'a+', encoding='utf-8') as f:
		for item in matches:
			f.write(unicode("%s\n" % item))
		print("wrote {0} matches".format(len(matches)))

def writeURFGames(matches, timeBucket):
	"""Records the match ids and the time bucket used to get those ids"""
	recordMatchIDs(matches)
	recordBucket(timeBucket)

def recordBucket(time):
	"""Records the time bucket used to get match ids, to avoid future duplicate calls"""
	with io.open('urf_buckets_read.txt', 'a+', encoding='utf-8') as f:
		f.write(unicode("%s\n" % time))
		print("wrote matches for bucket {0}".format(time))

def getURFMatchesByTime(time):
	"""Gets the match ids for a specific time bucket"""
	apiStr = "api/lol/na/v4.1/game/ids?beginDate="
	print("Getting URF Data for {0}...".format(time))
	global key
	matchesCall = callAPI(apiStr, time)
	matches = matchesCall.json()
	#print(matches)
	return matches

def getURFMatches():
	"""Gets a list of the URF matches played in the last 8 hours.

	We make sure the time is rounded to the nearest 5-minute interval, 
	and that duplicate calls to the same timebucket are avoided.
	"""
	readBuckets = io.open('urf_buckets_read.txt', 'r', encoding='utf-8').readlines()
	readBuckets = map(lambda s: int(s.strip().encode('latin-1')), readBuckets) #remove newlines
	print(readBuckets)
	currentTime = calendar.timegm(time.gmtime())
	print(currentTime)
	correctedTime = currentTime - (currentTime%300) + 300
	print(correctedTime)
	eightHours = 60 * 60 * 8
	for timeBucket in range(correctedTime-eightHours, correctedTime, 300):
		if timeBucket not in readBuckets:
			writeURFGames(getURFMatchesByTime(str(timeBucket)), str(timeBucket))
			time.sleep(1.2) #sleep for rito
		else:
			print("{0} already read".format(str(timeBucket)))


def main():
	#print(key)
	getURFMatches()
	removeDuplicates()


if __name__ == "__main__":
	main()