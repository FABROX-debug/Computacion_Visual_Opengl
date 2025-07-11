# gl_renderer_mesh.py  ───── FaceMesh 3D + OpenGL 100 % blindado ─────
from OpenGL.GL  import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2, numpy as np
from facemesh_tracker import get_facemesh
from triangles_mediapipe import TRIANGLES, TRIANGLES_FLAT

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)

verts, normals = [], []
MAX_TRI_IDX = max(TRIANGLES_FLAT)      # 477 (incluye iris)

# ---------- normales seguras ----------
def calc_normals(v):
    n = [np.zeros(3, np.float32) for _ in v]
    vlen = len(v)
    for a, b, c in TRIANGLES:
        if a >= vlen or b >= vlen or c >= vlen:
            continue                   # ignora triángulos fuera de rango
        va, vb, vc = np.array(v[a]), np.array(v[b]), np.array(v[c])
        cr = np.cross(vb - va, vc - va)
        n[a] += cr; n[b] += cr; n[c] += cr
    # normalizar
    for i, vec in enumerate(n):
        l = np.linalg.norm(vec)
        if l:
            n[i] = vec / l
    return n

# ---------- convertir landmarks ----------
def process(raw):
    a = np.array(raw, np.float32)
    a[:,0] = (a[:,0] - .5)*2
    a[:,1] = (.5 - a[:,1])*2
    a[:,2] =  a[:,2]*2
    a[:,0]-=a[:,0].mean(); a[:,1]-=a[:,1].mean(); a[:,2]-=a[:,2].mean()
    a[:,:2]*=2.5; a[:,2]*=2.0
    return a.tolist()

# ---------- render ----------
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity(); gluLookAt(0,0,8, 0,0,0, 0,1,0)

    if verts:
        # relleno
        glEnable(GL_LIGHTING)
        glBegin(GL_TRIANGLES)
        vlen = len(verts)
        for a,b,c in TRIANGLES:
            if c >= vlen: continue
            for idx in (a,b,c):
                glNormal3fv(normals[idx]); glVertex3fv(verts[idx])
        glEnd()
        glDisable(GL_LIGHTING)

        # wireframe
        glColor3f(0, .8, 1); glLineWidth(1)
        glBegin(GL_LINES)
        vlen = len(verts)
        for a,b,c in TRIANGLES:
            if c >= vlen: continue
            glVertex3fv(verts[a]); glVertex3fv(verts[b])
            glVertex3fv(verts[b]); glVertex3fv(verts[c])
            glVertex3fv(verts[c]); glVertex3fv(verts[a])
        glEnd()

    glutSwapBuffers()

# ---------- bucle ----------
def tick(_=0):
    global verts, normals
    ok, frame = cap.read()
    if not ok:
        return

    cv2.imshow("Camara (FaceMesh)", frame)
    cv2.waitKey(1)
    raw = get_facemesh(frame)

    if raw and len(raw) >= 468:              # acepta 468 (sin iris) o 478
        verts   = process(raw)
        normals = calc_normals(verts)
        print(f"🟢 rostro detectado ({len(raw)} pts)")
    else:
        verts, normals = [], []
        print("🔴 sin rostro")

    glutPostRedisplay()
    glutTimerFunc(16, tick, 0)

# ---------- init ----------
def iniciar_opengl():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"FaceMesh 3D - OpenGL")   # ASCII

    glEnable(GL_DEPTH_TEST);  glDisable(GL_CULL_FACE)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0,0,5,1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [.2,.7,1,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glMatrixMode(GL_PROJECTION); gluPerspective(45, WIDTH/HEIGHT, .1, 100)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw)
    tick()
    glutMainLoop()

    cap.release(); cv2.destroyAllWindows()
