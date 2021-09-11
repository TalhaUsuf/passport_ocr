import cv2
import yaml 
from pathlib import Path 
import json
import io 
import base64

def cvt2bytes():
	# load the image path given by user
	image = yaml.load(open('./paths.yaml','r'))['img']
	# get the stem and suffic with which to find the face in faces dir. by matching name
	stem = Path(image).stem
	ext = Path(image).suffix

	# get all the *.jpg faces in /faces/  dir.
	faces = list(Path("./faces/").glob('*.jpg')) 
	faces = [str(i) for i in faces if "face_"+stem in str(i)]

	print(str(image))
	print(faces)

	face = cv2.imread(faces[0])
	# added by talha
	red_imag = open(faces[0],"rb")
	encoded = base64.b64encode(red_imag.read())


	success, encoded_image = cv2.imencode(ext, face)
	
		
	# write as bytes array
	with open("./byte_arr.txt" , 'wb') as f:
		f.write(encoded_image.tobytes())

	# return str(encoded_image.tobytes())
	return str(encoded.tobytes())


# # load the image path given by user
# image = yaml.load(open('./paths.yaml','r'))['img']
# # get the stem and suffic with which to find the face in faces dir. by matching name
# stem = Path(image).stem
# ext = Path(image).suffix

# # get all the *.jpg faces in /faces/  dir.
# faces = list(Path("./faces/").glob('*.jpg')) 
# faces = [str(i) for i in faces if "face_"+stem in str(i)]


# face = cv2.imread(faces[0])
# success, encoded_image = cv2.imencode(ext, face)

# # write as bytes array
# with open("./byte_arr.txt" , 'wb') as f:
# 	f.write(encoded_image.tobytes())

# # read bytes 
# with open("./byte_arr.txt" , 'rb') as f:
# 	face2byte = f.read()

# # face2byte = face2byte.replace(b"'", b'"')
# # print(json.dumps(io.BytesIO(face2byte), indent=4))
# print(str(encoded_image.tobytes()))
# print(str(image))
# print(faces)