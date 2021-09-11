# import natas as nt
import re
from pathlib import Path
import json
from absl import app, flags
from absl.flags import FLAGS
from tqdm import tqdm
import sys
from rich.console import Console


flags.DEFINE_string('ocrjson', './detections/OCR_RESULT.json', 'path to OCR_RESULT.json file')
flags.DEFINE_string('processedjson', './detections/PROCESSED_OCR.json', 'path to PROCESSED_OCR.json file')



def retain_only_digits(label:str):
	"""takes a label and removes everything except digits [0-9] from it

	Parameters
	----------
	label : str
	    input string to be processed. `RAW string` (ocr results)

	Returns
	-------
	sub : str
	    cleaned string
	"""
	sub = re.sub('[^0-9]', "", label)
	return sub

def replace_non_alphabetic(label:str):

	"""takes in label and removes non alphabetic characters

	Parameters
	----------
	label : str
	    input raw string which needs to be cleaned

	Returns
	-------
	sub : str
	    cleaned string
	"""
	sub = re.sub('[^a-zA-Z]+'," ",label)
	return sub

def replace_non_alpha_numeric(label:str):
	"""takes a string as input and removes characters Except alphabets (small and capital case) and numbers

	Parameters
	----------
	label : str
	    string to be cleaned

	Returns
	-------
	sub : string
	    cleaned string (all chars. removed except alphabets and numbers)
	"""
	sub = re.sub('[^a-zA-Z0-9]+', " ", label)
	return sub

def retain_only_capital(label: str):
	"""takes in a string and removes the non-capital chars.

	Parameters
	----------
	label : str
	    input string needed to be cleaned

	Returns
	-------
	sub : str
 	    cleaned string
	"""
	sub = re.sub('[^A-Z]'," ",label)
	return sub

def process_gender(label:str):
	"""only retain M or F or m or f

	Parameters
	----------
	label : str
	    input string needed to be processed

	Returns
	-------
	sub  : str
	    cleaned string
	"""
	sub = re.sub('[^MFmf]'," ",label)
	return sub

def nationality(string):
	string = [i.strip() for i in string.split()]
	print(string)

	# string = [re.sub("(.*TAT.* | .*tat.*)", 'STATES', i, re.I) for i in string]
	string = [re.sub("(.*TAT.*)", 'STATES', i, re.I) for i in string]
	# print(string)
	string = [re.sub("(.*ITE.*)", 'UNITED', i, re.I) for i in string]
	# print(string)
	string = [re.sub("(.*MERI.*)", 'AMERICA', i, re.I) for i in string]
	# print(string)
	string = " ".join(string)
	return string





def main(argv):
	console = Console()
	console.rule("[bold underline red]Process_OCR")
	console.print(f"Opening the file [cyan]{FLAGS.ocrjson}[/cyan]", style="bold")
	ocr = json.load(open(FLAGS.ocrjson, 'r'))

# mrz
# image
#

	prev = sys.stdout
	with open('./detections/process_ocr_debug.txt', 'a')  as f:
		sys.stdout = f
		print(f"{'READING FILE FROM':<25}{'---->':<25}{FLAGS.ocrjson}")
		for key, val in tqdm(ocr.items(), total=len(ocr)):
			print(f"{'KEY':<25}{key}")
			print(f"{'VALUE':<25}{val}")
			if key == 'title':
				ocr['title'] = replace_non_alphabetic(ocr['title'])
			if key == 'nationality':
				ocr['nationality'] = nationality(ocr['nationality'])
			if key == 'type':
				ocr['type'] = retain_only_capital(ocr['type'])
			if key == 'surname':
				ocr['surname'] = replace_non_alphabetic(ocr['surname'])
			if key == 'name':
				ocr['name'] = replace_non_alphabetic(ocr['name'])
			if key == 'pob':
				ocr['pob'] = replace_non_alphabetic(ocr['pob'])
			if key == 'gender':
				ocr['gender'] = process_gender(ocr['gender'])
			if key == 'authority':
				ocr['authority'] = replace_non_alphabetic(ocr['authority'])
			if key == 'country_code':
				ocr['country_code'] = replace_non_alphabetic(ocr['country_code'])
			if key == 'endorsement':
				ocr['endorsement'] = replace_non_alpha_numeric(ocr['endorsement'])
			if key == 'passport_no':
				ocr['passport_no'] = retain_only_digits(ocr['passport_no'])
			if key == 'dob':
				ocr['dob'] = replace_non_alpha_numeric(ocr['dob'])
			if key == 'doi':
				ocr['doi'] = replace_non_alpha_numeric(ocr['doi'])
			if key == 'doe':
				ocr['doe'] = replace_non_alpha_numeric(ocr['doe'])



		json.dump(ocr, open(FLAGS.processedjson, 'w'), indent=6)
		print("..... Post processed the OCR succesfully")
		print(f"{'SAVED FILE':<25}{'---->':<25}{FLAGS.processedjson}")
	sys.stdout = prev
	console.print(f"Written the file ===> [bold cyan]{FLAGS.processedjson}[/bold cyan]", style="yellow underline")



if __name__=='__main__':
	# if imported in another module, code inside this place doesn't run
	app.run(main)
