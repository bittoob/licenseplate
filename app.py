from array import array

import streamlit as st
import cv2
import pytesseract

import numpy as np
from PIL import Image
from PIL import *


#st.set_page_config(layout="wide")



title_container = st.container()
col1, col2 = st.columns([5, 10])

with title_container:
    with col1:
        st.image('./download.png')
    with col2:
        st.title("Vehicle Number Plate Detection")
    




def gray_image(image_file):
    gray = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
    return gray

def blur_image(gray):
    blur = cv2.bilateralFilter(gray, 11, 90, 90)
    return blur

def contours(blur,image_file):
    edges = cv2.Canny(blur, 30, 200)
    cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image_file.copy()
    _ = cv2.drawContours(image_copy, cnts, -1, (255,0,255),2)
    cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:30]
    image_copy = image_file.copy()
    _ = cv2.drawContours(image_copy, cnts, -1, (255,0,255),2)

    plate = None
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(edges_count) == 4:
            x,y,w,h = cv2.boundingRect(c)
            plate = image_file[y:y+h, x:x+w]
            break

    return plate

#Quick sort
def partition(arr,low,high): 
    i = ( low-1 )         
    pivot = arr[high]    
  
    for j in range(low , high): 
        if   arr[j] < pivot: 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

def quickSort(arr,low,high): 
    if low < high: 
        pi = partition(arr,low,high) 
  
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)
        
    return arr


#Binary search   
def binarySearch (arr, l, r, x): 
  
    if r >= l: 
        mid = l + (r - l) // 2
        if arr[mid] == x: 
            return mid 
        elif arr[mid] > x: 
            return binarySearch(arr, l, mid-1, x) 
        else: 
            return binarySearch(arr, mid + 1, r, x) 
    else: 
        return -1
    

def main_loop():
    
    image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
    if not image_file:
        return None

    original_image = Image.open(image_file)
    original_image = np.array(original_image)

   
      
    st.text("Original Image")
    st.image([original_image])

    #convert original image into gray image
    g = gray_image(original_image)
    # st.write("Gray image")
    # st.image([g])

    #convert gray image into blur image
    b = blur_image(g)
    # st.write("Blur image")
    # st.image([b])

    #find contours
    p = contours(b,original_image)
    # st.image([p])
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    txt = pytesseract.image_to_string(p)
    
    st.subheader("Detection of Number Plate from Vehicle Image ")
    st.subheader(txt)

    ar  = ["MH 20 EE 7598","WH20 EJ 0365,", "MH1407T8831,","=MHO2FE8819","TN 87 A 3980","-GJO5JA1 143","KL 26 45009"]
 
    ar=quickSort(ar,0,len(ar)-1)
    result =  binarySearch(ar,0,len(ar)-1,txt)
    
    

    if ar[result]: 
        st.subheader("\n\nThe Vehicle is allowed to visit." ) 
        st.image('./stop (2).jpg')
    else: 
        st.subheader("\n\nThe Vehicle is not allowed to visit.")
        st.image('./stop (1).jpg')
    
    


if __name__ == '__main__':
    main_loop()