import sys

def uso():
    print("Uso:\n  python main.py haar   # esfera-rostro\n  python main.py mesh   # FaceMesh 3D")
    sys.exit(1)

if __name__ == "__main__":
    modo = sys.argv[1].lower() if len(sys.argv) > 1 else "mesh"

    if modo == "haar":
        from gl_renderer import iniciar_opengl; iniciar_opengl()
    elif modo == "mesh":
        from gl_renderer_mesh import iniciar_opengl; iniciar_opengl()
    else:
        uso()
