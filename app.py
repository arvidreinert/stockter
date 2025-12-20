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
window.setWindowTitle("Stockter")
window.setWindowIcon("images/icon.WEBP")

#Widgets
label = pysdw.QLabel("Status: nichts passiert")
#Layouts
main_layout = pysdw.QVBoxLayout()      

main_layout.addWidget(label)

window.setLayout(main_layout)
window.resize(400, 200)
window.show()

app.exec()