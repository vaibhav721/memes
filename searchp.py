import os
import sys
import pygtrie as pygtrie
import json
import argparse as arg
from PIL import Image
from collections import defaultdict
import logo
from difflib import get_close_matches

currentpath = os.path.dirname(os.path.abspath(__file__))
indexpath = os.path.join(currentpath, 'index')

l = pygtrie.CharTrie()
p = defaultdict(list)

with open(os.path.join(indexpath,'searchtrie.json')) as f:
	l._root.__setstate__(json.load(f))

with open(os.path.join(indexpath,'searchdict.json')) as f:
	p = json.load(f)

with open(os.path.join(indexpath,'index.json')) as f:
	data = json.load(f)


def str_search(inp, args):
	image_idx = list()
	inp = inp.split(' ')

	try:
		for word in inp:
			word = word.lower()
			indices = sorted(l[word:])

			for str_idx in indices:
				image_idx += p[str(str_idx)]
	except:
		try:
			with open(os.path.join(indexpath,'memedb.json')) as f:
				data = json.load(f)
			if args.mode=="1":
				print ("Did you mean %s instead?" % get_close_matches(inp[0], data.keys())[0])
				response = input("Enter y for yes and n for no - ")
				if response == 'y':
					image_idx = data[get_close_matches(inp[0], data.keys())[0]]
				else:
					image_idx = []
			else:
				image_idx = data[get_close_matches(inp[0], data.keys())[0]]
		except:
			pass

	if len(image_idx)!=0:
		display(image_idx, args)
	else:
		print("This meme or simmilar doesn't exist in our DB")
	'''
	for str_idx in image_idx:
		file = data["data"][str_idx]["location"]
		Image.open(file).show()
'''

def idx_search(index, args):

	display(index,string_search=False)
	'''
	for idx in index:
		file = data["data"][int(idx)]["location"]
		Image.open(file).show()
'''

def display(indices,args,string_search=True):
	search_result_json(indices)
	#print(args.result)
	index_count = len(indices)
	if args.result != 0:
		index_count = min(args.result,len(indices))

	if args.display_info == 0:
		if string_search:
			for str_idx in indices:
				if index_count > 0:
					file = data["data"][str_idx]["location"]
					Image.open(file).show()
				index_count -=1
		else:
			for idx in indices:
				if index_count > 0:
					file = data["data"][int(idx)]["location"]
					Image.open(file).show()
				index_count -=1
	else:
		for str_idx in indices:
			if index_count > 0:
				text = data["data"][int(str_idx)]["description"]
				print('-'*30)
				print(text)
			index_count -= 1

def search_result_json(indices):#stores all search results
	data1 = []
	path = []
	description = []
	for i in indices:
		data1.append(data["data"][int(i)]["name"])
		description.append(data["data"][int(i)]["description"])
		path.append(data["data"][int(i)]["location"])
	with open(os.path.join(indexpath,'search_results.json'), 'w') as f:
		json.dump({'data': [{'name': w, 'description': x, 'location': y}
              for (w, x, y) in zip(data1, description, path)]}, f,
              sort_keys=False, indent=4, ensure_ascii=False)

def start(args):
	if args.index_search == 0:
		if args.mode == '0':
			if args.search_str is not None:
				inp = args.search_str
				str_search(inp, args)
			else:
				print('Missing arguments')
		elif args.mode == '1':
			logo.print_logo()
			inp = input('Enter the search string: ')
			str_search(inp, args)
		else:
			print('Unknown arguments')

	elif args.index_search == 1:

		if args.mode == '0':

			if args.search_idx is not None:
				index = args.search_idx
				idx_search(index, args)

			else:
				print('Missing arguments')

		elif args.mode == '1':
			logo.print_logo()
			index = input('Enter image index: ')
			idx_search(index, args)
		else:
			print('Unknown argument')

	else:
		print('Unknown argument')

	#print(sorted(l['Tyr':]))
	#print(p[str(l['Tyrion'])]))
