from pathlib import Path
import yaml
from absl import app, flags
from absl.flags import FLAGS
import json
import io
import os 
import cv2
import PIL.Image as Image

flags.DEFINE_string("path", "./paths.yaml", help="path to the 'paths.yaml' file")



def main(argv):

	os.system('workon passport_ocr')
	paths = yaml.load(open(FLAGS.path))
	print(json.dumps(paths, indent=4))

	img = Path(paths['img'])
	name = img.stem
	ext = img.suffix

	print(f"{'path is':<25}{'=====>':<25}{name+ext}")

	img = cv2.imread(str(img))
	success, encoded_image = cv2.imencode(ext, img)


		# write as bytes array
	with open("./byte_arr.txt" , 'rb') as f:
		data = f.read()

	img = Image.open(io.BytesIO(data))
	img.save("./check.jpg")

	print(img)



if __name__=='__main__':
	app.run(main)