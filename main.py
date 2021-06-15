'''
Usage: 

1.Only print the text from image
python3 main.py --image './images/aadhar_demo2.jpg'

2.Print the each word from image with its confidence
python3 main.py --image './images/aadhar_demo2.jpg' --confidence True

'''

# importing packages
import argparse
from text_detection_recognition import TextDetectionRecognition

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path of the image file")
ap.add_argument("-c", "--confidence", default="True",
	help="print the confidence of each word from image")
args = vars(ap.parse_args())


tr = TextDetectionRecognition(args["image"])

# check the image is blur or not
blur_value = tr.img_blur_check()
if blur_value :
    # check the rotation of image and align accordingly
    rotated_img = tr.img_orientation()
    # pass the image for preprocessing
    preprocessed_img = tr.img_preprocess()
    # pass image for OCR 
    if args["confidence"]:
        recognized_text, confidence = tr.text_confidence()
        print(recognized_text,confidence)
    else:
        recognized_text = tr.text_recognition()
        print(recognized_text)
    
else:
    print("Image is Blur...")