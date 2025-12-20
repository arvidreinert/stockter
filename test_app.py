import sys
import PySide6.QtWidgets as pysdw
from PySide6.QtGui import QPixmap

app = pysdw.QApplication(sys.argv)

app.setStyle("Fusion")
app.setStyleSheet("""
QWidget {
    background-color: #121212;
    color: #ffffff;
}""")

window = pysdw.QWidget() 
window.setWindowTitle("Widgets & Layouts")

#Widgets
label = pysdw.QLabel("Status: nichts passiert")
button = pysdw.QPushButton("Klick mich")
checkbox = pysdw.QCheckBox("Option aktiv")
textfield = pysdw.QLineEdit()
textfield.setPlaceholderText("text bide")

image = pysdw.QLabel()
pixmap = QPixmap("images/Screenshot 2025-11-10 202928.png") 
image.setPixmap(pixmap.scaled(300,300))
image.setScaledContents(True)

#functions of widgets
def on_button_clicked():
    label.setText("Button wurde gedrückt")
button.clicked.connect(on_button_clicked)

def on_checkbox_changed(state):
    if state:
        label.setText("Checkbox AN")
    else:
        label.setText("Checkbox AUS")
checkbox.stateChanged.connect(on_checkbox_changed)

def on_text_entered():
    label.setText(textfield.text())
textfield.returnPressed.connect(on_text_entered)

#Layouts
main_layout = pysdw.QVBoxLayout()      
row_layout = pysdw.QHBoxLayout()      

row_layout.addWidget(button)
row_layout.addWidget(checkbox)
row_layout.addWidget(textfield)

main_layout.addWidget(label)
main_layout.addWidget(image)
main_layout.addLayout(row_layout)

window.setLayout(main_layout)
window.resize(400, 200)
window.show()

app.exec()