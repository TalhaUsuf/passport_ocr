from fastapi import FastAPI
import uvicorn
import json
import os
import yaml
from fastapi.responses import JSONResponse
from face2byte_array import cvt2bytes
import numpy as np
import cv2
from pathlib import Path
import base64
from rich.console import Console
from pathlib import Path
from SMWinservice import SMWinservice

app = FastAPI()


@app.get('/ocr/byte_array/{byte_img:path}')
async def paspport_ocr(byte_img : str):
	Console().rule("run_app_debug")
	Console().print(f"making dir [green]./inputByte2image[/green]", style="bold red")
	# making a dir. to save the image restored from a byte array
	Path('./inputByte2image').mkdir(exist_ok=True, parents=True)

	# read the base64 string from filepath provided by user
	byte_array = open(Path(byte_img), 'rb').read()
	arr = np.fromstring(byte_array, np.uint8)
	img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
	cv2.imwrite('./inputByte2image/byte2img.jpg', img)
	# open('./inputByte2image/byte2img.jpg','wb').write(base64.b64decode(b64stringimg))
	Console().print(f"Converted to image [green]byte2img.jpg[/green] and written to [green]./inputByte2image[/green] dir", style="bold red")


	#  reading the original yaml config file
	Console().print(f"Opening file [cyan]{'./paths.yaml'}[/cyan]")
	with open('./paths.yaml', 'r') as f:
		keys = yaml.load(f)

	keys['img'] = './inputByte2image/byte2img.jpg' # every time it will be replaced.
	#  modifying the yaml file 'img' entry inplace
	with open('./paths.yaml', 'w') as f:
		yaml.dump(keys, f)
	Console().print(f"Finished writing the file [cyan]{'./paths.yaml'}[/cyan]")

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
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		#  					delete files if already exist
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# if already present then delete the file
		if os.path.exists('./detections/OCR_RESULT.json'):
			os.remove('./detections/OCR_RESULT.json')

		if os.path.exists('./detections/PROCESSED_OCR.json'):
			os.remove('./detections/PROCESSED_OCR.json')

		if os.path.exists("./detections/boxes.json"):
			os.remove("./detections/boxes.json")

		# os.system('''workon passport_ocr
		# 		python yolo2opencv.py
		# 		python opencv2tesseract.py
		# 			''')
		# os.system('''
		# python yolo2opencv.py
		# python opencv2tesseract.py
		# 	''')
		# os.system("python yolo2opencv.py && python opencv2tesseract.py && python process_ocr.py")

		os.system("python yolo2opencv.py")
		Console().print("Executed script ====> [green]python yolo2opencv.py[/green]", style="bold red underline")
		os.system("python opencv2tesseract.py")
		Console().print("Executed script ====> [green]python opencv2tesseract.py[/green]", style="bold red underline")
		os.system("python process_ocr.py")
		Console().print("Executed script ====> [green]python process_ocr.py[/green]", style="bold red underline")


		# if no exception then execute this
		# ocrResult = json.load(open('./detections/OCR_RESULT.json', 'r'))
		# os.system('''workon passport_ocr
				# python process_ocr.py''')
		ocrResult = {}
		# if no exception---> file will be made by script process_ocr.py
		# open that file
		processed = json.load(open('./detections/PROCESSED_OCR.json', 'r'))
		ocrResult['processed_ocr'] = processed

		ocrResult['processed_ocr']['image'] = cvt2bytes()
		ocrResult['processed_ocr']['title'] = " "

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

	except Exception as e:
		# if any exception then execute this
		errors = {"error" : str(e)}
		return JSONResponse(content=errors)
		pass


@app.get('/ocr/base64/{base64str_img:path}')
async def paspport_ocr_b64(base64str_img : str):
	Console().rule("run_app_debug")
	Console().print(f"making dir [green]./inputByte2image[/green]", style="bold red")
	# making a dir. to save the image restored from a byte array
	Path('./inputByte2image').mkdir(exist_ok=True, parents=True)


	# read the base64 string from filepath provided by user
	b64stringimg = open(Path(base64str_img), 'rb').read()
	open('./inputByte2image/byte2img.jpg','wb').write(base64.b64decode(b64stringimg))
	Console().print(f"Converted to image [green]byte2img.jpg[/green] and written to [green]./inputByte2image[/green] dir", style="bold red")



	# byte_array = open(Path(byte_img), 'rb').read()
	# arr = np.fromstring(byte_array, np.uint8)
	# img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
	# cv2.imwrite('./inputByte2image/byte2img.jpg', img)
	# # open('./inputByte2image/byte2img.jpg','wb').write(base64.b64decode(b64stringimg))
	# Console().print(f"Converted to image [green]byte2img.jpg[/green] and written to [green]./inputByte2image[/green] dir", style="bold red")


	#  reading the original yaml config file
	Console().print(f"Opening file [cyan]{'./paths.yaml'}[/cyan]")
	with open('./paths.yaml', 'r') as f:
		keys = yaml.load(f)

	keys['img'] = './inputByte2image/byte2img.jpg' # every time it will be replaced.
	#  modifying the yaml file 'img' entry inplace
	with open('./paths.yaml', 'w') as f:
		yaml.dump(keys, f)
	Console().print(f"Finished writing the file [cyan]{'./paths.yaml'}[/cyan]")

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
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		#  					delete files if already exist
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# if already present then delete the file
		if os.path.exists('./detections/OCR_RESULT.json'):
			os.remove('./detections/OCR_RESULT.json')

		if os.path.exists('./detections/PROCESSED_OCR.json'):
			os.remove('./detections/PROCESSED_OCR.json')

		if os.path.exists("./detections/boxes.json"):
			os.remove("./detections/boxes.json")

		# os.system('''workon passport_ocr
		# 		python yolo2opencv.py
		# 		python opencv2tesseract.py
		# 			''')
		# os.system('''
		# python yolo2opencv.py
		# python opencv2tesseract.py
		# 	''')
		os.system("python yolo2opencv.py")
		Console().print("Executed script ====> [green]python yolo2opencv.py[/green]", style="bold red underline")
		os.system("python opencv2tesseract.py")
		Console().print("Executed script ====> [green]python opencv2tesseract.py[/green]", style="bold red underline")
		os.system("python process_ocr.py")
		Console().print("Executed script ====> [green]python process_ocr.py[/green]", style="bold red underline")


		# if no exception then execute this
		# ocrResult = json.load(open('./detections/OCR_RESULT.json', 'r'))
		# os.system('''workon passport_ocr
				# python process_ocr.py''')
		ocrResult = {}
		# if no exception---> file will be made by script process_ocr.py
		# open that file
		processed = json.load(open('./detections/PROCESSED_OCR.json', 'r'))
		ocrResult['processed_ocr'] = processed

		ocrResult['processed_ocr']['image'] = cvt2bytes()
		ocrResult['processed_ocr']['title'] = " "

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

	except Exception as e:
		# if any exception then execute this
		errors = {"error" : str(e)}
		return JSONResponse(content=errors)
		pass
"""
class PythonCornerExample(SMWinservice):
    _svc_name_ = "Passport"
    _svc_display_name_ = "Passport"
    _svc_description_ = "Use to get Passport Information"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        uvicorn.run("run_app_debug:app", host='127.100.100.1', port=8000, debug=True)
"""		
		
if __name__ == '__main__':
    #PythonCornerExample.parse_command_line()
	uvicorn.run("run_app_debug:app", host='127.100.100.1', port=8000, debug=True)



	
