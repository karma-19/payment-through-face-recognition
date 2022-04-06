import imp
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupModelSerializer
from .models import UserSignupModel
import cv2
import os
import numpy as np
from PIL import Image
import json


# Create your views here.

#USER SIGNUP 
@api_view(['POST'])
def user_signup(request):
    try:
        obj =  UserSignupModelSerializer(data =  request.data)
        if obj.is_valid():
            obj.save()
            return Response({'Message':'Successfully Signed up'},status = status.HTTP_200_OK)

        return Response(obj.errors,status = status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)



#SAVE PICS
@api_view(['GET'])
def save_pics(request):
    try:
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # For each person, enter one numeric face id
        face_id = input('\n enter user id end press <return> ==>  ')
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0
        while(True):
            ret, img = cam.read()
            #img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite("C:/Users/Praveen/Desktop/clg/payment-through-face-recognition/mysite/myapp/dataset/User." + str(face_id) + '.' +  
                            str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                break
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        return Response({'Message':'Image saved successfully.'},status = status.HTTP_200_OK)
    except Exception as e:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)



#TRAINER
@api_view(['GET'])
def train_model(request):
    try:
        path = 'C:/Users/Praveen/Desktop/clg/payment-through-face-recognition/mysite/myapp/dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # function to get the images and label data
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L') # grayscale
                img_numpy = np.array(PIL_img,'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        # Save the model into trainer/trainer.yml
        recognizer.write('C:/Users/Praveen/Desktop/clg/payment-through-face-recognition/mysite/myapp/trainer/trainer.yml') 
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        return Response({'Message':'Model trained Successfully.'},status = status.HTTP_200_OK)
    except Exception as e:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)

#FACE-RECOGNITION
@api_view(['GET'])
def face_recognition(request):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('C:/Users/Praveen/Desktop/clg/payment-through-face-recognition/mysite/myapp/trainer/trainer.yml')
        #cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        font = cv2.FONT_HERSHEY_SIMPLEX
        #iniciate id counter
        id = 0
        # names related to ids: example ==> Marcelo: id=1,  etc
        names = ['None', 'Praveen', 'Rakesh', 'Rajesh', 'Z', 'W'] 
        emails = {'None':'none', 'Praveen':'praveen@gmail.com', 
                    'Rakesh':'rakesh@gmail.com', 'Rajesh':'rajesh@gmail.com'}
        # names = [['name', 'email'],
        #         ['Praveen', 'praveen@gmail.com'], 
        #         ['Rakesh', 'rakesh@gmail.com'], 
        #         ['Rajesh', 'rajesh@gmail.com'] ]
        # email = 'unknown'
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height
        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        while True:
            ret, img =cam.read()
            #img = cv2.flip(img, -1) # Flip vertically
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                
                # If confidence is less them 100 ==> "0" : perfect match 
                if (confidence < 100):
                    id = names[id]
                    #email = names[id][1]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(
                            img, 
                            str(id), 
                            (x+5,y-5), 
                            font, 
                            1, 
                            (255,255,255), 
                            2
                        )
                cv2.putText(
                            img, 
                            str(confidence), 
                            (x+5,y+h-5), 
                            font, 
                            1, 
                            (255,255,0), 
                            1
                        )  
            
            cv2.imshow('camera',img) 
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        return Response({'user_name':id, 'user_email' : emails[str(id)] }, 200)
    except Exception as e:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)


#PAYMENT FROM ACCOUNT
@api_view(['POST'])
def payment(request):
    try:
        """{"user_email":"", "pay":""}"""
        data = request.data
        #print("data", data)
        try:
            serializer = UserSignupModelSerializer(UserSignupModel.objects.get(user_email=data['user_email']))
        except:
            return Response({'message':'Please Register.'}, 400)
        
        pay = int(data['pay'])
        bal = serializer.data['user_balance']
        if(bal<pay):
            return Response({'message':'Transaction failed due to insufficient balance.'}, 400)
        UserSignupModel.objects.filter(user_email=data['user_email']).update(user_balance=serializer.data['user_balance'] -pay)
         
        # print("serializer is", serializer.data)
        # money = serializer.data['user_balance']
        # print("type : ", type(money), type(pay))
        # money = money-pay
        # if(money<0):
        #     return Response({'message':'Transaction failed due to insufficient balance.'}, 400)
        # serializer.user_balance = money

        # if(obj.is_valid()):
        #     obj.save()
        # else:
        #     return Response({'message':'Something failed during transaction.'}, 400)
        return Response({'message':'Transaction Successful.'}, 200)
    except Exception as e:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)


#RECHARGE ACCOUNT
@api_view(['POST'])
def add_money(request):
    """{"user_email":"", "amount":""}"""
    try:
        data = request.data
        #print("data", data)
        try:
            serializer = UserSignupModelSerializer(UserSignupModel.objects.get(user_email=data['user_email']))
        except:
            return Response({'message':'Please Register.'}, 400)
        
        amt = int(data['amount'])
        bal = serializer.data['user_balance']
        UserSignupModel.objects.filter(user_email=data['user_email']).update(user_balance=serializer.data['user_balance']+amt)
        return Response({'message':'Transaction successfull. Amount added to your account.'}, 200)

    except:
        return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)


