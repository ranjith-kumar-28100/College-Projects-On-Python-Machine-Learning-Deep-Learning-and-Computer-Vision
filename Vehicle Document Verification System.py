import cv2
import numpy as np
import pytesseract
from PIL import *

src_path=r"C:/Users/RAJNISH KUMAR PANDEY/Desktop/project/"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_text(img_path):
    '''img=cv2.imread(img_path)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #apply dilation and erosion to remove some noise
    kernal=np.ones((1,1),np.uint8)
    img=cv2.dilate(img, kernal, iterations=1)
    img = cv2.erode(img, kernal, iterations=1)

    cv2.imwrite(src_path + "removed_noise.jpg", img)
    #apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite(src_path + "thresh.jpg",img)
    '''
    #Recgonise text with 
    result = pytesseract.image_to_string(Image.open(img_path))

    #save the text into the file
    f = open("details.txt", "w")
    f.write(result)
    f.close()
    return result


print("---start recognize text--")
print(get_text(src_path+"4.jpg"))
print("---done--")


print("\n---- Filteration part starts----")

f=open("details.txt","r")
a=f.read()
f.close()
s_name=a.find("Name:")+5
e_name=a.find("D.0.B:")-1
name=a[s_name:e_name]
name=name.strip()
print(name)
s_dob=a.find("D.0.B:")+6
e_dob=a.find("ID No:")-1
dob=a[s_dob:e_dob]
dob=dob.strip()
print(dob)

s_id=a.find("ID No:")+6
e_id=a.find("Issued:")-1
id_no=a[s_id:e_id]
id_no=id_no.strip()
print(id_no)

s_issued=a.find("Issued:")+7
e_issued=a.find("Expires:")-1
issued=a[s_issued:e_issued]
issued=issued.strip()
print(issued)
print("\n---- Filteration part ends----")

#inserting to database
print("-----enter to database starts------")
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="licence_details"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE scanned_details (id_no VARCHAR(20) PRIMARY KEY, name VARCHAR(30), dob VARCHAR(20),issues VARCHAR(20))")
'''#name="Geoff Sample"
#dob="Area manager"
#id_no="1238626AB4"
#issues="January 2011"
'''
#mycursor.execute("INSERT INTO `scanned_details`(`id_no`, `name`, `dob`, `issues`) VALUES (id_no,name,dob,issues)")
sql = "INSERT INTO scanned_details (id_no, name, dob, issues) VALUES (%s, %s, %s, %s)"
val = (id_no, name, dob, issued)
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")
print("----db part ends-----")

#extract data from sample details database
print("-----fetching and verification starts-----")
sql = "SELECT * FROM sample_details WHERE id_no = %s"
adr = (id_no, )

mycursor.execute(sql, adr)
myresult = mycursor.fetchall()

i_name=myresult[0][1]
i_dob=myresult[0][2]
i_issues=myresult[0][3]

if name==i_name and dob==i_dob and issued==i_issues:
    print("verified person")
else:
    print("not in maches check with police record")
print("-----fetching and verification ends-----")

