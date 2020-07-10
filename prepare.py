import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

def load_model_R34(path_model):
    model = tf.keras.models.load_model(path_model)
    return model

def cropobject(frame):
    # Smooth image
    kernel = np.ones((5,5),np.float32)/25
    Smooth = cv2.filter2D(frame,-1,kernel)

    # Fine Edge 
    # Canny(image, edges, threshold1, threshold2)
    edges = cv2.Canny(Smooth, 20, 50)

    # dilation
    kernel = np.ones((5, 5), np.uint8) 
    dilation = cv2.dilate(edges,kernel,iterations = 1)

    # Opening
    kernel = np.ones((10, 10), np.uint8) 
    opening1 = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((12, 12), np.uint8) 
    opening2 = cv2.morphologyEx(opening1, cv2.MORPH_OPEN, kernel)
    
    # (Height, Width, Channels)
    dimensions = frame.shape
    # print(dimensions)

    h1=float('inf')
    h2=0
    w1=float('inf')
    w2=0


    for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                    if opening2[i,j] == 255:
                            if j < w1:
                                        w1 = j
                                        
                            if j > w2:
                                        w2 = j

                            if i < h1:
                                        h1 = i

                            if i > h2:
                                        h2 = i
    crop_img1 = frame[h1:h2, w1:w2]

    dh = crop_img1.shape[0]
    dw = crop_img1.shape[1]
    d = dh - dw

    img = []
    d = 0

    if dh > dw:
            d = dh - dw
            img = np.arange(dh*dh*3).reshape(dh,dh,3)
            for i in range(dh):
                    for j in range(dh):
                            for k in range(3):
                                        img[i,j,k] = 255
            
    if dw > dh:
            d = dw - dh
            img = np.arange(dw*dw*3).reshape(dw,dw,3)
            for i in range(dw):
                    for j in range(dw):
                            for k in range(3):
                                        img[i,j,k] = 255
                                    
    # Fine Center
    if crop_img1.shape[0] > crop_img1.shape[1]:  # Wide
            C = img.shape[0] - crop_img1.shape[1]
            C = C/2
            for i in range(dh):
                    for j in range(dw):
                            for k in range(3):
                                        img[i,int(j+C),k] = crop_img1[i,j,k]
            
    if crop_img1.shape[0] < crop_img1.shape[1]:  # Height
            C = img.shape[1] - crop_img1.shape[0]
            C = C/2
            for i in range(dh):
                    for j in range(dw):
                            for k in range(3):
                                        img[int(i+C),j,k] = crop_img1[i,j,k]
            
    img = np.array(img, dtype=np.uint8)
    
    return img
                                    
def prepare(img_path):
    IMG_SIZE = 224
    
    # Read image by PLT
    image = Image.open(img_path)
    img_array = np.array(image)
    
    img_array = cropobject(img_array)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    img_array = new_array/255.0
    
    img = img_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
    return img

def prediction(model, img):
    CATEGORIES = ["glass", "metal", "plastic", "trash"]
    prediction = model.predict(img)
    i, = np.where( np.isclose( prediction[0], max( prediction[0] ) ) )

    return CATEGORIES[ int(i)]