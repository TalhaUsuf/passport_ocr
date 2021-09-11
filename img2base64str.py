import cv2
import io
import numpy as np
import base64
from absl import flags, app
from absl.flags import FLAGS
from pathlib import Path 


flags.DEFINE_string('path', "", 'path of the image to be converted to b64 string')
flags.DEFINE_string('out', 'bytesimg.bin', 'bytes image write file name like imagestring.bin')

# ###################################################
#                   converting image to b64 string
# ###################################################

def main(argv):

	print(f"{'READING FILE':<25}{'======>':<25}{FLAGS.path}")
	b64string = base64.b64encode(open(FLAGS.path, 'rb').read())
	parent = Path(FLAGS.path).parent
	to_save = str(parent) + "/" + FLAGS.out
	with open(to_save, 'wb') as f:
		f.write(b64string) 





if __name__ == '__main__':
	app.run(main)