from fastapi import FastAPI
import uvicorn
import json 
import os 
import yaml 
from fastapi.responses import JSONResponse
from face2byte_array import cvt2bytes
import numpy as np
from pathlib import Path
import base64


app = FastAPI()




@app.get('/ocr/{base64str_img:path}')
async def paspport_ocr(base64str_img : str):
	# making a dir. to save the image restored from a byte array 
	Path('./inputByte2image').mkdir(exist_ok=True, parents=True)

	# read the base64 string from filepath provided by user
	b64stringimg = open(Path(base64str_img), 'rb').read()
	open('./inputByte2image/byte2img.jpg','wb').write(base64.b64decode(b64stringimg))


	#  reading the original yaml config file
	with open('./paths.yaml', 'r') as f:
		keys = yaml.load(f)

	keys['img'] = './inputByte2image/byte2img.jpg' # every time it will be replaced.
	#  modifying the yaml file 'img' entry inplace
	with open('./paths.yaml', 'w') as f:
		yaml.dump(keys, f)

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#                        FOR DEBUGGING UN-COMMENT THIS
	#               IF EXCEPTION OCCURS, IT'ILL NOT BE SHOWN IN CMD
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# os.system('workon passport_ocr')
	# os.system('python yolo2opencv.py')
	# os.system('python opencv2tesseract.py')
	# ocrResult = json.load(open('./detections/OCR_RESULT.json', 'r'))	
	# ocrResult = {'raw_ocr' : ocrResult}
	# os.system('workon passport_ocr')
	# os.system('python process_ocr.py')
	# processed = json.load(open('./detections/PROCESSED_OCR.json', 'r'))

	# ocrResult['processed_ocr'] = processed

	# return JSONResponse(content=ocrResult)

	try:

		os.system('workon passport_ocr')
	except Exception as e:
		print(e)
		pass


	try:
		os.system('workon passport_ocr')
		os.system('python yolo2opencv.py')
	except Exception as e:
		print(e)
		pass


	try:	
		os.system('source workon passport_ocr')
		os.system('python opencv2tesseract.py')
	except Exception as e:
		pritn(e)
		pass


			
	try:
		# if there is no exception ----> only then OCR_RESULT file will be created
		ocrResult = json.load(open('./detections/OCR_RESULT.json', 'r'))
		# tag as raw results
		# ocrResult = {'raw_ocr' : ocrResult}
		os.system('workon passport_ocr')
		os.system('python process_ocr.py')

	except Exception as e:
		print(e)
		pass
	else:
		ocrResult = {}
		# if no exception---> file will be made by script process_ocr.py
		# open that file
		processed = json.load(open('./detections/PROCESSED_OCR.json', 'r'))
		ocrResult['processed_ocr'] = processed

		ocrResult['processed_ocr']['image'] = cvt2bytes()
		ocrResult['processed_ocr']['title'] = ""

		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		#                 load the boxes coordinates
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		boxes = json.load(open("./detections/boxes.json", "r"))
		ocrResult['boxes'] = boxes

		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		#                 RESPONSE WILL BE GIVEN IF 
		#                      NO ERRORS OCCURED
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		return JSONResponse(content=ocrResult)

	




if __name__ == '__main__':
	uvicorn.run(app, host='127.100.100.1', port=8000)