import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QHBoxLayout, QLineEdit, QListWidget, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont


# Widget para dibujar la carita de la ranita 
class CabeceraRanita(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ojos (Verde exterior)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(181, 204, 127)))
        painter.drawEllipse(88, 13, 44, 44)
        painter.drawEllipse(228, 13, 44, 44)

        # Pupilas (Negro)
        painter.setBrush(QBrush(QColor(20, 20, 20)))
        painter.drawEllipse(94, 19, 32, 32)
        painter.drawEllipse(234, 19, 32, 32)

        # Brillos de los ojos (Blanco)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(99, 24, 12, 12)
        painter.drawEllipse(239, 24, 12, 12)

        # Mejillas Rosadas
        painter.setBrush(QBrush(QColor(255, 150, 170)))
        painter.drawEllipse(63, 40, 30, 16)
        painter.drawEllipse(267, 40, 30, 16)

        # Boca
        painter.setBrush(QBrush(QColor(20, 20, 20)))
        painter.drawChord(QRectF(145, 28, 70, 40), 0 * 16, -180 * 16)

        # Lengua
        painter.setBrush(QBrush(QColor(255, 140, 160)))
        painter.drawChord(QRectF(155, 40, 50, 26), 0 * 16, -180 * 16)


class CalculadoraRanitaPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora:Brisa Maribel V. (PySide6)")
        self.setFixedSize(380, 580)

        self.historial = []
        self.en_estado_error = False

        self.iniciar_ui()
        self.aplicar_estilos()

    def iniciar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(15, 10, 15, 15)
        layout_principal.setSpacing(6)

        # 1. Cabecera dibujada (Ranita)
        self.cabecera = CabeceraRanita()
        layout_principal.addWidget(self.cabecera)

        # 2. Pantalla de Entrada / Resultado
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout_principal.addWidget(self.display)

        # 3. Etiqueta e Historial (QListWidget)
        lbl_historial = QLabel("Historial (Doble clic para recuperar):")
        lbl_historial.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout_principal.addWidget(lbl_historial)

        self.list_historial = QListWidget()
        self.list_historial.setFixedHeight(65)
        self.list_historial.itemDoubleClicked.connect(self.cargar_desde_historial)
        layout_principal.addWidget(self.list_historial)

        # 4. Layout de Botones
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(6)

        # Grid para botones normales (Columnas 0 a 2)
        grid_izquierda = QGridLayout()
        grid_izquierda.setSpacing(6)

        botones_izquierda = [
            ('C', 0, 0, "amarillo"),  ('CE', 0, 1, "amarillo"), ('/', 0, 2, "amarillo"),
            ('7', 1, 0, "blanco"),    ('8', 1, 1, "blanco"),    ('9', 1, 2, "blanco"),
            ('4', 2, 0, "blanco"),    ('5', 2, 1, "blanco"),    ('6', 2, 2, "blanco"),
            ('1', 3, 0, "blanco"),    ('2', 3, 1, "blanco"),    ('3', 3, 2, "blanco"),
            ('0', 4, 0, "blanco"),    ('.', 4, 1, "blanco"),    ('Info', 4, 2, "blanco")
        ]

        for texto, fila, col, tipo in botones_izquierda:
            btn = QPushButton(texto)
            btn.setObjectName(f"btn_{tipo}")
            btn.setFixedHeight(42)
            btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_izquierda.addWidget(btn, fila, col)

        # Columna Derecha (Operadores + Botón '=' largo)
        grid_derecha = QGridLayout()
        grid_derecha.setSpacing(6)

        btn_mul = QPushButton("*")
        btn_mul.setObjectName("btn_amarillo")
        btn_mul.setFixedHeight(42)
        btn_mul.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.conectar_boton(btn_mul, "*")
        grid_derecha.addWidget(btn_mul, 0, 0)

        btn_sub = QPushButton("-")
        btn_sub.setObjectName("btn_amarillo")
        btn_sub.setFixedHeight(42)
        btn_sub.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.conectar_boton(btn_sub, "-")
        grid_derecha.addWidget(btn_sub, 1, 0)

        btn_sum = QPushButton("+")
        btn_sum.setObjectName("btn_amarillo")
        btn_sum.setFixedHeight(42)
        btn_sum.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.conectar_boton(btn_sum, "+")
        grid_derecha.addWidget(btn_sum, 2, 0)

        # Botón '=' alargado como el de la imagen
        btn_eq = QPushButton("=")
        btn_eq.setObjectName("btn_amarillo")
        btn_eq.setFixedHeight(90)
        btn_eq.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.conectar_boton(btn_eq, "=")
        grid_derecha.addWidget(btn_eq, 3, 0, 2, 1)

        layout_botones.addLayout(grid_izquierda, stretch=3)
        layout_botones.addLayout(grid_derecha, stretch=1)

        layout_principal.addLayout(layout_botones)

    def conectar_boton(self, btn, texto):
        if texto == 'C':
            btn.clicked.connect(self.limpiar)
        elif texto == 'CE':
            btn.clicked.connect(self.borrar_ultimo)
        elif texto == '=':
            btn.clicked.connect(self.calcular)
        elif texto == 'Info':
            btn.clicked.connect(self.abrir_info)
        else:
            btn.clicked.connect(lambda _, t=texto: self.agregar_caracter(t))

    def agregar_caracter(self, char):
        if self.en_estado_error:
            return
        self.display.setText(self.display.text() + char)

    def limpiar(self):
        self.display.setText("")
        self.en_estado_error = False

    def borrar_ultimo(self):
        if self.en_estado_error:
            return
        texto = self.display.text()
        if texto:
            self.display.setText(texto[:-1])

    def calcular(self):
        if self.en_estado_error:
            return

        expr = self.display.text()
        if not expr:
            return

        try:
            res = eval(expr, {"__builtins__": None, "math": math}, {})
            if isinstance(res, float) and res.is_integer():
                res = int(res)

            res_str = str(res)
            self.actualizar_historial(f"{expr} = {res_str}")
            self.display.setText(res_str)
        except Exception:
            self.display.setText("Error")
            self.en_estado_error = True

    def actualizar_historial(self, operacion):
        self.historial.append(operacion)
        if len(self.historial) > 5:
            self.historial.pop(0)

        self.list_historial.clear()
        self.list_historial.addItems(self.historial)

    def cargar_desde_historial(self, item):
        texto = item.text()
        if "=" in texto:
            resultado = texto.split("=")[-1].strip()
            self.display.setText(resultado)
            self.en_estado_error = False

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #b5cc7f;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                background-color: #c8e1e6;
                color: #222222;
                border: none;
                border-radius: 12px;
                padding: 8px 12px;
            }
            QListWidget {
                background-color: #a8c072;
                color: #1a1a1a;
                border: none;
                border-radius: 10px;
                padding: 4px;
                font-size: 11px;
            }
            QListWidget::item:selected {
                background-color: #f4b41a;
                color: #ffffff;
                border-radius: 4px;
            }
            QPushButton#btn_blanco {
                background-color: #f0f0f0;
                color: #333333;
                border: none;
                border-radius: 14px;
            }
            QPushButton#btn_blanco:hover {
                background-color: #ffffff;
            }
            QPushButton#btn_blanco:pressed {
                background-color: #d8d8d8;
            }
            QPushButton#btn_amarillo {
                background-color: #f4b41a;
                color: #ffffff;
                border: none;
                border-radius: 14px;
            }
            QPushButton#btn_amarillo:hover {
                background-color: #ffc52d;
            }
            QPushButton#btn_amarillo:pressed {
                background-color: #dc9f0e;
            }
        """)

    def abrir_info(self):
        QMessageBox.information(
            self,
            "Información",
            "Calculadora Brisa Maribel V.  v5.0\nLibrería: PySide6 (Qt)"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculadoraRanitaPySide6()
    window.show()
    sys.exit(app.exec())