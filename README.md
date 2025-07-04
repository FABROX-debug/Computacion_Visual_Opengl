markdown
# 🧠 FaceMesh 3D con OpenGL

Este proyecto implementa un sistema de **detección facial en 3D en tiempo real** utilizando **MediaPipe FaceMesh** y visualización con **OpenGL**. La detección se realiza con una webcam, y los puntos clave del rostro son renderizados en una malla 3D con iluminación básica.

---

## 📸 Demo

<img src="docs/demo_1.png" width="400"/> <img src="docs/demo_2.png" width="400"/>

---

## 🚀 Tecnologías utilizadas

- 🐍 Python 3.12
- 🎥 OpenCV (`cv2`)
- 📦 MediaPipe (FaceMesh)
- 🔺 PyOpenGL (OpenGL + GLUT)
- 🧠 NumPy
- 💡 Iluminación y renderizado 3D

---

## 📁 Estructura del Proyecto

```

Proyecto/
│
├── facemesh\_tracker.py         # Detección de puntos faciales con MediaPipe
├── gl\_renderer\_mesh.py         # Renderizado 3D con OpenGL
├── triangles\_mediapipe.py      # Índices de triangulación de FaceMesh
├── main.py                     # Punto de entrada principal
└── README.md                   # Este archivo

````

---

## ⚙️ Cómo ejecutar

1. **Instala las dependencias**:

```bash
pip install opencv-python mediapipe PyOpenGL
````

2. **Ejecuta el programa**:

```bash
python main.py mesh
```

🔹 También puedes usar el modo `haar` si implementas la detección con cascadas Haar.

---

## 🧠 ¿Qué hace este proyecto?

✔ Captura en tiempo real desde la webcam
✔ Detecta 468 puntos faciales usando **MediaPipe FaceMesh**
✔ Convierte los puntos a coordenadas 3D para **OpenGL**
✔ Renderiza una malla facial 3D con iluminación, normales y líneas
✔ Usa triangulación para visualizar el rostro como una superficie en 3D

---

## 📝 Mejoras futuras

* Agregar sombreado más realista (Phong / Gouraud)
* Implementar texturas sobre la malla facial
* Soporte para múltiples rostros
* Exportar la malla como archivo `.obj`
* Agregar control de cámara (rotación interactiva)

---

## 👨‍💻 Autor

**Fabrizio (FABROX-debug)**
Estudiante de Ingeniería de Software - UNMSM
GitHub: [FABROX-debug](FABROX-debug)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

