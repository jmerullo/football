#
# Extract all name mentions from tagged transcripts
#

import json
import re
import xml.etree.ElementTree as ET


def load_data(data_dir):
	'''
	data_dir: string file path to tagged transcripts file
	'''
	data = {}
	with open(data_dir, 'r') as f:
		data = json.load(f)
	return data


def extract_mentions(samples):
	'''
	samples: a list of games. Each game is stored as a dictionary with keys:
			 {'teams', 'transcript', 'year'}
	'''
	ments = []
	for s in samples:
		matches = re.findall(r'<person .*?</person>', s['transcript'])
		for match in matches:
			xml = ET.fromstring(match)
			label = {'race':xml.attrib['race'], 'position':xml.attrib['position'],
					'player':xml.attrib['player'], 'year':s['year'], 
					'teams':s['teams'], 'reference':xml.text}
			
			ments.append(label)
	return ments

if __name__ == "__main__":
	import sys
	data = load_data(sys.argv[1])
	#get a list of all games in dictionary form
	samples =  list(data.values())
	mention_contexts = extract_mentions(samples)
	#...