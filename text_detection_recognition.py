
import cv2
import numpy as np
from PIL import Image
from tesserocr import PyTessBaseAPI,PSM, OEM,image_to_text


class TextDetectionRecognition:
    def __init__(self,image):
        self.image = cv2.imread(image)
        self.new_height = 320
        self.new_width = 320
        self.original = self.image.copy()
        self.size = 60
        self.height,self.width = self.image.shape[:2]
        # define tesseract prefix
        self.tessdata_directory = "./model_files"
        self.language = 'eng'
        self.psm_flag = PSM.AUTO
        

    def img_blur_check(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # grab the dimensions of the image and use the dimensions to
        # derive the center (x, y)-coordinates
        (h, w) = self.gray.shape
        (cX, cY) = (int(w / 2.0), int(h / 2.0))

        # compute the FFT to find the frequency transform, then shift
        # the zero frequency component (i.e., DC component located at
        # the top-left corner) to the center where it will be more
        # easy to analyze
        fft = np.fft.fft2(self.gray)
        fftShift = np.fft.fftshift(fft)

        # zero-out the center of the FFT shift (i.e., remove low
        # frequencies), apply the inverse shift such that the DC
        # component once again becomes the top-left, and then apply
        # the inverse FFT
        fftShift[cY - self.size:cY + self.size, cX - self.size:cX + self.size] = 0
        fftShift = np.fft.ifftshift(fftShift)
        recon = np.fft.ifft2(fftShift)

        # compute the magnitude spectrum of the reconstructed image,
        # then compute the mean of the magnitude values
        magnitude = 20 * np.log(np.abs(recon))
        mean = np.mean(magnitude)
        print(mean)
        # the image will be considered "blurry" if the mean value of the
        # magnitudes is less than the threshold value
        if mean <= 10 :
            # print("blur image")  
            return False
        else:
            return True

    def img_orientation(self):        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        
        # threshold the image, setting all foreground pixels to
        # 255 and all background pixels to 0
        self.thresh = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # grab the (x, y) coordinates of all pixel values that
        # are greater than zero, then use these coordinates to
        # compute a rotated bounding box that contains all
        # coordinates
        coords = np.column_stack(np.where(self.thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        # the `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle

        # rotate the image to deskew it
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.rotated = cv2.warpAffine(self.image, M, (w, h),
            flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        # cv2.imwrite('./final_img.jpg',self.rotated)   
        # show the output image
        print("[INFO] angle: {:.3f}".format(angle))
        return self.rotated
        # cv2.imshow("Input", self.image)
        # cv2.imshow("Rotated1", self.rotated)

    def img_preprocess(self):
        # remove noise
        self.dst = cv2.fastNlMeansDenoisingColored(self.rotated,None,10,10,7,21)
        # grayscale
        self.gray = cv2.cvtColor(self.rotated, cv2.COLOR_BGR2GRAY) 
        return self.gray      
        # thresholding
        #self.thresholded_img = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
    
    def text_recognition(self):
        with PyTessBaseAPI(path=self.tessdata_directory, psm = self.psm_flag, lang=self.language) as api:
            # read the image
            cv2.imwrite("./images/sample.jpg",self.gray)
            image = Image.open('./images/sample.jpg')            
            detected_text = image_to_text(image,lang=self.language, path=self.tessdata_directory)
        return detected_text


    def text_confidence(self):
        # read the image
        cv2.imwrite("./images/sample.jpg",self.gray)
        with PyTessBaseAPI(path=self.tessdata_directory,psm=self.psm_flag, lang=self.language) as api:
            # read the image
            api.SetImageFile("./images/sample.jpg")
            api.SetVariable("save_blob_choices", "T")
            detected_text = api.GetUTF8Text()
            confidence = api.AllWordConfidences()            
        return detected_text, confidence

                