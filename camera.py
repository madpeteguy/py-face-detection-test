import argparse
import cv2 as cv
from score import appargs, fps, faces, webcam

ap = argparse.ArgumentParser()
ap.add_argument(appargs.P_CAMERA_S, appargs.P_CAMERA_L, type=int, default=0, help="# of camera to get stream from")
args = vars(ap.parse_args())

camNo = args[appargs.P_CAMERA_N]
webCam = webcam.WebCam(camNo, resolution=(1280, 720)).start()
# webCam = webcam.WebCam(camNo).start()
fps = fps.FPS().start()
fcx = faces.Faces()

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
# cv.namedWindow('img', cv.WINDOW_NORMAL)ś
lastFrame = None
lastFaces = 0
while True:
    if not webCam.grabbed:
        print('Can not read frame....')
        break
    gray = cv.cvtColor(webCam.frame, cv.COLOR_BGR2GRAY)
    if lastFrame is not webCam.frame:
        lastFrame = webCam.frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv.rectangle(lastFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv.putText(lastFrame, 'FACE', (x+5, y+20), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1, cv.LINE_AA)
            fcx.verify_face((x, y, w, h))
    fps.update()
    rFrame = lastFrame
    if not lastFaces == fcx.get_faces_count():
        lastFaces = fcx.get_faces_count()
        rFrame = cv.cvtColor(rFrame, cv.COLOR_BGR2HSV)
    cv.putText(rFrame, 'FPS {} {}'.format(fps.fps(), fcx.get_faces_count()), (5, 25), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.imshow('img', rFrame)
    if cv.waitKey(1) == ord('q'):
        break

fps.stop()
webCam.stop()
cv.destroyAllWindows()
