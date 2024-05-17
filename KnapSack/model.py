import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QOpenGLWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QMatrix4x4
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

class BackpackWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertices = np.array([
            # Front face
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            # Back face
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0, -1.0, -1.0,
            # Top face
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0, -1.0,
            # Bottom face
            -1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,
            # Right face
             1.0, -1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0,  1.0,  1.0,
             1.0, -1.0,  1.0,
            # Left face
            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,
        ], dtype=np.float32)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # Update approximately 60 times per second

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        vertex_shader_source = """
        #version 450 core
        layout(location = 0) in vec3 position;
        uniform mat4 projection;
        uniform mat4 view;
        uniform mat4 model;
        void main()
        {
            gl_Position = projection * view * model * vec4(position, 1.0);
        }
        """

        fragment_shader_source = """
        #version 460 core
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(0.0, 0.8, 0.2, 1.0); // Green color
        }
        """

        self.shader_program = QOpenGLShaderProgram()
        if not self.shader_program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertex_shader_source):
            print("Vertex Shader Error:", self.shader_program.log())
        if not self.shader_program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragment_shader_source):
            print("Fragment Shader Error:", self.shader_program.log())
        if not self.shader_program.link():
            print("Shader Program Link Error:", self.shader_program.log())
        self.shader_program.bind()

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        position = self.shader_program.attributeLocation('position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = self.create_projection_matrix(45, self.width() / self.height(), 0.1, 50.0)
        view = self.create_view_matrix()
        model = self.create_model_matrix()

        self.shader_program.setUniformValue('projection', projection)
        self.shader_program.setUniformValue('view', view)
        self.shader_program.setUniformValue('model', model)

        glDrawArrays(GL_QUADS, 0, 24)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def create_projection_matrix(self, fov, aspect, near, far):
        f = 1.0 / np.tan(np.radians(fov) / 2)
        values = [
            f / aspect, 0, 0, 0,
            0, f, 0, 0,
            0, 0, (far + near) / (near - far), -1,
            0, 0, (2 * far * near) / (near - far), 0
        ]
        return QMatrix4x4(*values)

    def create_view_matrix(self):
        eye = np.array([0.0, 0.0, 5.0], dtype=np.float32)
        center = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        f = (center - eye)
        f /= np.linalg.norm(f)
        s = np.cross(f, up)
        s /= np.linalg.norm(s)
        u = np.cross(s, f)
        view_matrix = np.array([
            [s[0], u[0], -f[0], 0],
            [s[1], u[1], -f[1], 0],
            [s[2], u[2], -f[2], 0],
            [-np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye), 1]
        ], dtype=np.float32)
        return QMatrix4x4(*view_matrix.flatten())

    def create_model_matrix(self):
        return QMatrix4x4(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Backpack")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.backpack_widget = BackpackWidget()
        self.layout.addWidget(self.backpack_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
