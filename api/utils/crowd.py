import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('api/utils/humancount-70e1d-firebase-adminsdk-9rxc0-7e3d9e852f.json')

# Initialize the app with a service account
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://humancount-70e1d-default-rtdb.firebaseio.com/'
})

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detectByImage(image_path):
    print('Detecting people...')

    # Load the image
    image = cv2.imread(image_path)

    # Perform detection
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    for x, y, w, h in bounding_box_cordinates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1

    cv2.putText(image, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(image, f'Total Persons : {person - 1}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)

    # Save the annotated image to the same path, replacing the input image
    annotated_image_path = image_path.replace('.jpg', '_annotated.jpg')
    cv2.imwrite(annotated_image_path, image)

    ref = db.reference('/')
    ref.update({'/count': person - 1})

    return annotated_image_path, person - 1



# if __name__ == "__main__":
#
#
#     # Specify the path to the input image
#     image_path = 'faces.jpg'
#
#     detectByImage(image_path)
