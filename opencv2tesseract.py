import pytesseract as tess
import cv2
from pathlib import Path
import yaml
import ast
import json
from multiprocessing.dummy import Pool
from multiprocessing import Pool as proc_pool
import numpy as np
import itertools
from multiprocessing import cpu_count
from imutils import resize
import os
from rich.console import Console
from rich.table import Table



def recognize_text(cropped_image, name):
	"""takes in cropped image region along with corresponding label and returns results of recognition

	Args:
	    cropped_image (np.ndarray): cropped image section
	    name (str): label of text field

	Returns:
	    a list of type [name, results] where name is the text label name and results is the recognition result
	"""
	cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

	# cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
	# cropped_image = cv2.equalizeHist(cropped_image)

	custom_oem_psm_config = r'--oem 3 --psm 6 -l eng'
	results = tess.image_to_string(cropped_image, config=custom_oem_psm_config)

	return [name , results]



def draw_single_rectangle(img:np.ndarray, rect:list, c:list, name:str, face_save:str, ext:str):
	"""draws the rectangle over class `name` defined by `rect` in image **img**. Saves the \
	face_region in directory *./faces* according to the name of the image provided.

	Parameters
	----------
	img : np.ndarray
	    original image on which to draw the boxes
	rect : list
	    [x, y, w, h] where `x` and `y` are top left coordinates of the rectangle
	c : list
	    [R,G,B] color with which to draw the boxes
	name : str
	    Name of the class like "image", "doi", "dob" ......
	face_save : str
	    name with which to save image
	ext : str
	    extension with which to save image

	Returns
	-------
	None

	"""
	if name == 'image': # if image, then crop the face image part
		# rect[0] ==> x
		# rect[1] ==> y
		# rect[2] ==> w
		# rect[3] ==> h
		crop = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
		# crop = cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), tuple(c), 2, cv2.LINE_AA )

		# success, encoded_image = cv2.imencode('.jpg', crop)
		# draw_single_rectangle.bytearray_img =  encoded_image.tobytes()

		cv2.imwrite("./faces/face_"+face_save+ext, crop)

	img = cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), tuple(c), 2, cv2.LINE_AA )
	img = cv2.putText(img, f'{name}', (rect[0], rect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, tuple(c), 2, cv2.LINE_AA)
	return img

def crop_boxes(img:np.ndarray, rect:list, name: str):
	"""will crop a single box given a rect list of form [x, y, w, h]

	Args:
	    img (np.ndarray): image from which to crop the pieces
	    rect (list): [x, y, width, height] of the box
	    name (str): name of the box related to detection

	Returns:
	    out (list): [name, img] where name is name of text label and img is cropped image
 	"""
	x, y, w, h = rect[0], rect[1], rect[2], rect[3]
	img = img[int(y):int(y+h), int(x):int(x+w)] # rows, columns
	# out = [name,img]
	# return out
	return img


def main():

      console = Console()
      console.rule("[bold underline red]Opencv to Tesseract")

      table = Table(title="RAW OCR RESULTS")


      base_path = Path(".")
      # create a faces directory
      faces_dir = base_path / "faces"
      faces_dir.mkdir(parents=True, exist_ok=True)

      paths = base_path / 'paths.yaml'
      console.print(f"Opening the [cyan]yaml[/cyan] file", style="bold")
      paths = yaml.load(open(str(paths)))

      img = paths['img']
      name2save = Path(img).stem
      extension = Path(img).suffix

      boxes = paths['boxes']
      console.print(f"OPENING boxes file from [cyan]{paths['boxes']}[/cyan]")
      boxes = json.load(open(boxes, 'r')) # BOXES IS A DICTIONARY
      names = [j for j,_ in boxes.items()] # labels of classes
      locations = [j for _,j in boxes.items()] # location of boxes [x1, y1, x2, y2]
      img = cv2.imread(img) # numpy array

      COLORS = np.random.choice(range(10,200), (16,3)) # total classes --> 16, R,G,B --> 3
      COLORS = [[int(j) for j in i] for i in COLORS]

      console.print("Calling the function [bold cyan]draw_single_rectangle[/bold cyan] using pool of [red]10[/red] threads")
      # draw using multi-threading
      with Pool(10) as p:
      	results = p.starmap(draw_single_rectangle, zip(itertools.repeat(img), locations, COLORS, names , itertools.repeat(name2save), itertools.repeat(extension)))

      print(f"........completed drawing rectangles")

      show_img = resize(results[-1], width=620)
      name = str(Path(paths['img']).stem)
      ext = str(Path(paths['img']).suffix)
      console.print(f"Writing the image -------> [cyan]{'./detections/images_bbox/'+name+'_cv2tess'+ext}[/cyan]")
      cv2.imwrite('./detections/images_bbox/'+name+'_cv2tess'+ext, show_img)
      # cv2.imshow('detections',show_img)
      # k = cv2.waitKey() & 0xFF

      # if k == ord('q'):
      	# cv2.destroyAllWindows()

      console.print("Calling the function [cyan]crop_boxes[/cyan] using a pool of [red]10[/red] worker threads")
      # detect using multiprocessing
      with Pool(10) as p:
      	results = p.starmap(crop_boxes, zip(itertools.repeat(img), locations, names))

      # results is a list of following structure
      # [[name, cropped_img],[name, cropped_img],[name, cropped_img], .......... ]
      print(f"........completed cropping rectangles")


      console.print("Calling the function [cyan]recognize_text[/cyan] using a pool of [red]4[/red] worker processes")
      # detect using multiprocessing
      # with Pool(2) as p:
      with proc_pool(cpu_count()) as p:
            results = p.starmap(recognize_text, zip(results,names))

      print(f"........completed recognizing rectangles")

      results = {i[0]:i[1].strip() for i in results}

      console.print("Writing the raw ocr results to ------> [cyan]{'./detections/OCR_RESULT.json'}[/cyan]")
      # results['image'] = draw_single_rectangle.bytearray_img


      table.add_column("Text Field", justify="right", style="bold cyan", no_wrap=True)
      table.add_column("Values",justify="left", style="bold yellow")
      for k,v in results.items():
      	table.add_row(k, v)

      console.print(table)
      # print(json.dumps( results, indent=6))
      json.dump(results, open('./detections/OCR_RESULT.json', 'w'), indent = 10)
      console.print("File ===> [bold cyan]./detections/OCR_RESULT.json[/bold cyan] written", style="red")
      print(f"...... PROCESS COMPLETED")

if __name__ == '__main__':
	# os.system('workon passport_ocr')
	main()
