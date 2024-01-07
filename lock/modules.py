import cv2
import time
import boto3
from lock.models import Unlockers
import os
def recognize():
    try:
        #get Unlockers count
        unlockers_count = Unlockers.objects.count()
        print("Now matching, Please wait!\n\n")
        targetFile='/path/to/TargetPhoto/main.jpg'
        for i in reversed(range(unlockers_count)):
            start = time.time()

            print("count: ", i)
            print("Comparing image with ", Unlockers.objects.all()[i].name, "...\n\n")
            #get image
            image = Unlockers.objects.all()[i].image
            sourceFile='/path/to/source/'+str(image)
            client=boto3.client('rekognition')
            
            imageSource=open(sourceFile,'rb')
            imageTarget=open(targetFile,'rb')

            response=client.compare_faces(SimilarityThreshold=70,
                                            SourceImage={'Bytes': imageSource.read()},
                                            TargetImage={'Bytes': imageTarget.read()})
            end = time.time()
            print("Time taken: ", end-start)
            if len(response['FaceMatches']) != 0:

                for faceMatch in response['FaceMatches']:
                    confidence = str(faceMatch['Face']['Confidence'])
                    print(confidence)

                imageSource.close()
                imageTarget.close()
                if round(float(confidence),2) > 95.00:
                    #get name
                    name = Unlockers.objects.all()[i].name
                    #return true with name
                    return name
        return False
    except Exception as e:
        print("Error in Matching Image!\n\n")
        return False