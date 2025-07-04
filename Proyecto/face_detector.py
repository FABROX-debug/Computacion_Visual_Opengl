import cv2, os

CASCADE_PATH = os.path.join(
    os.path.dirname(__file__), "assets", "haarcascade_frontalface_default.xml"
)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detectar_faces(frame, w, h):
    """Devuelve [(cx, cy, size)] en rango OpenGL [-1,1]."""
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    out   = []
    for (x, y, w0, h0) in faces:
        cx = (x + w0/2) / w * 2 - 1
        cy = 1 - (y + h0/2) / h * 2
        out.append((cx, cy, w0 / w))
    return out
