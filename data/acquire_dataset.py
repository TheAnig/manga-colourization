# Original author https://github.com/kvfrans

import urllib.request
import json
import numpy as np
import cv2
import untangle


maxsize = 512

count = 1

for i in range(3000):
    stringreturn = urllib.request.urlopen(f"https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=1girl%20solo&pid={str(i+84)}").read()
    xmlreturn = untangle.parse(stringreturn.decode())
    print(f"{i}, {count}")
    for post in xmlreturn.posts.post:
        imgurl = "https:" + post["sample_url"]
        print(imgurl)
        if ("png" in imgurl) or ("jpg" in imgurl):

            resp = urllib.request.urlopen(imgurl)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = image.shape[:2]
            cropped = None
            if height > width:
                scalefactor = (maxsize*1.0) / width
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                cropped = res[0:maxsize,0:maxsize]
            if width > height:
                scalefactor = (maxsize*1.0) / height
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                center_x = int(round(width*scalefactor*0.5))
                print(center_x)
                cropped = res[0:maxsize,center_x - int(maxsize/2):center_x + int(maxsize/2)]

            count += 1
            cv2.imwrite("./manga_dataset/"+str(count)+".jpg",cropped)
