# gl_renderer_mesh.py  –  FaceMesh 3D sin distorsión
from OpenGL.GL  import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2, numpy as np
from facemesh_tracker import get_facemesh
from triangles_mediapipe import TRIANGLES        # 1 434 índices

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)
verts, normals = [], []

# ───────── util: normales seguras ─────────
def calc_normals(v):
    n = [np.zeros(3, np.float32) for _ in v]
    vlen = len(v)
    for a, b, c in TRIANGLES:
        if a >= vlen or b >= vlen or c >= vlen:
            continue
        va, vb, vc = np.array(v[a]), np.array(v[b]), np.array(v[c])
        cr = np.cross(vb - va, vc - va)
        n[a] += cr; n[b] += cr; n[c] += cr
    for i, vec in enumerate(n):
        l = np.linalg.norm(vec)
        if l: n[i] = vec / l
    return n

# ───────── util: normalizar landmarks ─────────
def process(raw):
    """0-1 landmarks  →  OpenGL coords centradas, con Z normalizado frame a frame."""
    pts = np.array(raw, np.float32)          # 468 ó 478 × 3

    # 1) X,Y → [-1,1]   (OpenGL)
    pts[:, 0] = (pts[:, 0] - .5) *  2.0
    pts[:, 1] = (.5 - pts[:, 1]) *  2.0

    # 2) Z: MediaPipe es negativa cerca de la cámara.  Normalizamos rango por frame.
    zmin, zmax = pts[:, 2].min(), pts[:, 2].max()
    if zmax - zmin < 1e-5:                # evita división por 0
        z_scale = 1.0
    else:
        z_scale = 2.0 / (zmax - zmin)     # rango final ≈ -1 … +1
    pts[:, 2] = (pts[:, 2] - zmax) * -z_scale  # invierte y normaliza

    # 3) centrar X-Y (NO Z)
    pts[:, 0] -= pts[:, 0].mean()
    pts[:, 1] -= pts[:, 1].mean()

    # 4) escala global
    pts[:, :2] *= 1.8
    return pts.tolist()

# ───────── render ─────────
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity(); gluLookAt(0,0,6, 0,0,0, 0,1,0)

    if verts:
        vlen = len(verts)

        # sólido
        glEnable(GL_LIGHTING)
        glBegin(GL_TRIANGLES)
        for a,b,c in TRIANGLES:
            if c >= vlen: continue
            for idx in (a,b,c):
                glNormal3fv(normals[idx]); glVertex3fv(verts[idx])
        glEnd(); glDisable(GL_LIGHTING)

        # wire
        glColor3f(0,.8,1); glLineWidth(1)
        glBegin(GL_LINES)
        for a,b,c in TRIANGLES:
            if c >= vlen: continue
            glVertex3fv(verts[a]); glVertex3fv(verts[b])
            glVertex3fv(verts[b]); glVertex3fv(verts[c])
            glVertex3fv(verts[c]); glVertex3fv(verts[a])
        glEnd()

    glutSwapBuffers()

# ───────── loop ─────────
def tick(_=0):
    global verts, normals
    ok, frame = cap.read()
    if not ok: return

    cv2.imshow("Cámara (FaceMesh)", frame)
    cv2.waitKey(1)

    raw = get_facemesh(frame)
    if raw and len(raw) >= 468:        # 478 con iris, 468 sin iris
        verts   = process(raw)
        normals = calc_normals(verts)
        print(f"🟢 {len(raw)} puntos")
    else:
        verts, normals = [], []
        print("🔴 sin rostro")

    glutPostRedisplay(); glutTimerFunc(16, tick, 0)

# ───────── init ─────────
def iniciar_opengl():
    glutInit(); glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"FaceMesh 3D - OpenGL")

    glEnable(GL_DEPTH_TEST); glDisable(GL_CULL_FACE)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,[0,0,5,1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,[.2,.7,1,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR,[1,1,1,1])

    glMatrixMode(GL_PROJECTION); gluPerspective(45, WIDTH/HEIGHT, .1, 100)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw); tick()
    glutMainLoop()

    cap.release(); cv2.destroyAllWindows()
