# pip install opencv-python
# pip install google.generativeai
#pip install pytesseract
#pip install gTTS
#pip install playsound

import cv2
import google.generativeai as genai
import os
from PIL import Image
from gtts import gTTS
import time
#from playsound import playsound
import pygame


GOOGLE_API_KEY="..." ## https://aistudio.google.com/app/apikey
genai.configure(api_key=GOOGLE_API_KEY)
        
cap = cv2.VideoCapture(0) #第一個鏡頭為(0)
while(cap.isOpened()):
    ret, frame = cap.read()
    #print(frame.shape)
    #frame = cv2.flip(frame, 1) # 0: vertical flip, 1: horizontal flip
    cv2.imshow('Camera', frame)
    #cv2.imwrite('cam.jpg',frame)
    # 初始化 pygame
    pygame.mixer.init()
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break        
   
    elif cv2.waitKey(10) & 0xFF == ord(' '): 
       
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)      
        #img = Image.open('cam.jpg')
        prompt = "照片中是什麼東西? 請簡單回答。"
        model = genai.GenerativeModel("gemini-1.5-flash")

        result = model.generate_content( [prompt , img] )
        print(result.text)
                  
        # Text-to-Speech
        tts = gTTS(result.text,lang="zh-TW")
        tts.save('gTTS.mp3')
        time.sleep(3)
        # 加載並播放 MP3 文件
        pygame.mixer.music.load('gTTS.mp3')
        pygame.mixer.music.play()            
       #os.system("cmdmp3 gTTS.jpg") # Windows   
       # playsound("gTTS.mp3")
        # 等待播放結束
        while pygame.mixer.music.get_busy():
          continue  
      # 停止播放
        pygame.quit()
        time.sleep(1)
        os.remove('gTTS.mp3')
     
cap.release()
cv2.destroyAllWindows()




