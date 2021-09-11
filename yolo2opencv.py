import cv2
import numpy as np
from pathlib import Path
# from absl import app, flags
from time import time
import sys
import yaml
from rich.console import Console
from imutils import resize 
import json
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                       yolo files
#              .names, .cfg and .weights
#                  should be present in current folder
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# FLAGS = flags.FLAGS
# flags.DEFINE_string('path', './yolo','path to the folder containing .cfg, .weights and .names file')
# flags.DEFINE_string('img','./yolo/images/Screenshot 2021-02-10 at 11.57.53_1.jpg', help='path to image')



def main():

    console = Console()
    console.rule("[bold underline red]Yolo to Opencv")
    console.print(f"Opening [cyan]yaml[/cyan] file")
    params = yaml.load(open('paths.yaml','r'))
    Path(params['savepath']).mkdir(parents=True, exist_ok=True)
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #                               saving print() output to a file
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    original_stdout = sys.stdout # Save a reference to the original standard output
    console.print(f"Opened [cyan]log[/cyan] file")
    with open(params['log_detections_file'], 'a+') as f:
        sys.stdout = f # Change the standard output to the file we created.



        np.random.seed(10)
        # base_pth = Path(FLAGS.path)
        base_pth = Path(params['path'])
        # path to the three required files
        cfg_file = base_pth / 'yolov4.cfg'
        weights_file = base_pth / 'yolov4_best.weights'
        names_file = base_pth / 'obj.names'
        print(35*"%")
        print(35*"%")
        print("%-35s %-s"%("Config file Path",cfg_file))
        print("%-35s %-s"%("Weights file Path",weights_file))
        print("%-35s %-s"%("Names file Path",names_file))
        print(35*"%")
        print(35*"%")
        # net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        LABELS = open(str(names_file)).read().strip().split('\n') # read the class names
        print(f"classes are:\n")
        print([i for i in LABELS])
        COLORS = np.random.randint(0,256,(len(LABELS),3), dtype="uint8") # generating N random RGB colors where N is no. of classes

        # NET = cv2.dnn.readNetFromDarknet(darknetModel=str(weights_file), cfgFile=str(cfg_file))

        NET = cv2.dnn.readNetFromDarknet(str(cfg_file), str(weights_file))

        model = cv2.dnn_DetectionModel(NET)
        model.setInputParams(scale=1/255.0, size=(1024,1024), swapRB=True, crop=False)


        # print(f".... model has been loaded")

        # img = cv2.imread(FLAGS.img)
        print(f"reading image ----->  {params['img']}")
        img = cv2.imread(params['img'])
        H, W = img.shape[:2]
        # print("%-15s %-s"%("HEIGHT--->",H))
        # print("%-15s %-s"%("WIDTH--->",W))
        start = time()
        classes, scores, boxes = model.detect(frame=img, confThreshold=0.5, nmsThreshold=0.5)
        print(f"TOOK {time() - start} seconds to detect")
        COLORS = np.random.choice(range(256), size=(len(LABELS), 3))
        cvt2int = lambda x : [[int(j) for j in i]for i in x ]
        COLORS = cvt2int(COLORS)
        print("PRINTING DETECTIONS\n\n\n")

        _labels = []
        _boxes = []
        for cls_id, score, box in zip(classes, scores, boxes):

                cls_id = cls_id.squeeze()
                print("class id ----> %s"%(cls_id))
                print("score ----> %s"%(score.squeeze().tolist()))
                print("class box ----> %s"%(box.squeeze().tolist()))
                c = COLORS[cls_id]
                img = cv2.rectangle(img, box, color=tuple(c), thickness=2, lineType=cv2.LINE_AA)
                label = f"{LABELS[cls_id]}-->{score.squeeze().tolist():.3f}"
                print(f"label ----> {label}")
                img = cv2.putText(img, label, (box[0], box[1] - 10 ), cv2.FONT_HERSHEY_PLAIN, 0.7, tuple(c), 1, cv2.LINE_AA)
                _labels.append(LABELS[cls_id])
                _boxes.append(box.squeeze().tolist())

        data = {i:j for i,j in zip(_labels, _boxes)}
        with open(params['boxes'], 'w') as f:
            json.dump(data, f, indent=4)

        img = resize(img, width=620)
        Path('./detections/images_bbox').mkdir(parents=True, exist_ok=True) # make a dir. images_bbox inside detections folder to save images 
        name = str(Path(params['img']).stem)
        ext = str(Path(params['img']).suffix)
        console.print(f"Writing image", style="bold red")
        cv2.imwrite('./detections/images_bbox/'+name+ext, img)
        # cv2.imshow("img", img)
        # k = cv2.waitKey() & 0xFF
        # if k == ord('q'):
            # cv2.destroyAllWindows()
        print(f"{'IMAGE WRITEN TO DIR.':<25}{'====>':<25}{'./detections/images_bbox/'+name+ext}")
        sys.stdout = original_stdout  # Reset the standard output to its original value


if __name__ == '__main__':
    main()
