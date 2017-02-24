''' Simple leaf classifier using morphological operations
    Aiming for support to increase accuracy of classification.
    Have fun! - Vivek Vasudevan :)'''
#importing the necessary classes.
import cv2               #Debian openCV2 library..you might want to look for a newer release of openCV
import numpy as np       #Every image is a numpy array
import sys		 #For command line arguments
import csv               #For reading and writing into csv spreadsheets 
from matplotlib import pyplot as plt  #Graphical APIs
classification={'m':'monocot ', 'd':'dicot','u':'unknown'}      #Dictionary for classification
with open('leaves.csv','wb') as csvfile:                        #Opening a newly created leaves.csv file
 leafwriter=csv.writer(csvfile)				#A write handle initialized to the csv file
 leafwriter.writerow([' LEAF NAME ','  VEIN DENSITY  ','  CLASSIFICATION  '])  #Column headers
 for leaf in sys.argv[1:]: 	#Passing the images as command line arguments.
  leafID=str(leaf[4:7])         #Might have to change this since the leaf variable has full path.
  leafName=str(leaf)		#Example of a LeafName ~/leaf_m01_corn.jpeg
  img = cv2.imread(leaf,0)      #Reads the image into a numpy array . 0 indicates grayscale
  res = cv2.resize(img,(200,300),fx=0,fy=0)       #Adjust to your requirements to get the best skeleton
  equ = cv2.equalizeHist(res)		#Remove noise through standard openCV function.
  cv2.imshow(leaf,equ)			#Leaf as title .  Equalized image shown in a window
  size = np.size(equ)			#Resolution
  skel = np.zeros(equ.shape,np.uint8)   #Initializes a numpy array of dimensions of equ with zeros
  ret,equ = cv2.threshold(equ,127,255,cv2.THRESH_TOZERO)     #Binary thresholding
  element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))  #Morphological cross structuring element
  done = False				
  while( not done):			#loop invariant
   eroded = cv2.erode(equ,element)      #erosion -> dilation -> image difference -> bitwise_or
   temp = cv2.dilate(eroded,element)    #dilation:using the same structuring element
   temp = cv2.subtract(equ,temp)        #image difference
   skel = cv2.bitwise_or(skel,temp)	
   equ = eroded.copy()			#copy the numpy array
   zeros = size - cv2.countNonZero(equ) #After zero intensity level is completely eliminated in the eroded image.
   if zeros==size:
    done = True 			#loop invariant satisfied
  cv2.imshow("Skeleton leaf",skel)	#Showing the skeleton leaf
  fv=skel[65:125,90:145]		#Capturing an feature vector. Take one of your choice based on the kind of leaf images you have got.
  cv2.imshow("Feature Vector",fv)
  cv2.waitKey(0)
  cv2.destroyAllWindows()  
  #plt.imshow(fv, cmap = 'gray', interpolation = 'bicubic')
  #plt.show()    #....matplotlib demo for feature vector zoom view
  low_energy_count=0                  
  high_energy_count=0                #Statistical entropy variables for nearest neighbour approximation.
  for row in fv:		     #Scanning the pixels row-wise
   for value in row:	             #Scanning each pixel's intensity
    if value<10:low_energy_count=low_energy_count+1		#The values are based on my observations
    if value>127:high_energy_count=high_energy_count+1
  print low_energy_count,high_energy_count
  vein_density=float((80)*high_energy_count/(high_energy_count+low_energy_count))  #Approximation of percentage of leaf area occupied by leaf veins
#Writing the classifications onto the csv file using the csvwriter object  
 if low_energy_count>2400:
   leafwriter.writerow([leafName,vein_density,classification['d']])
  elif high_energy_count>250:
   leafwriter.writerow([leafName,vein_density,classification['m']])
  else:
   leafwriter.writerow([leafName,'?',classification['u']])   
    
  
 
