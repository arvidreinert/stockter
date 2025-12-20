import sys
import PySide6.QtWidgets as pysdw
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

#fonts:
titlefont = QFont()
titlefont.setFamily("Bauhaus 93")
titlefont.setPointSize(18)
titlefont.setBold(True)
titlefont.setItalic(True)

#main font:
mainfont = QFont()
mainfont.setFamily("ADLaM Display")
mainfont.setPointSize(12)
mainfont.setBold(False)
mainfont.setItalic(False)

#the app:
app = pysdw.QApplication(sys.argv)

app.setStyle("Fusion")
app.setStyleSheet("""
QWidget {
    background-color: #121212;
    color: #ffffff;
}
QLabel {
    color: #FFD52E;              
}""")

#window:
window = pysdw.QWidget() 
window.setWindowTitle("stockDuck")
window.setWindowIcon(QPixmap("images/icon.webp"))

#stacks:
stack = pysdw.QStackedWidget()

#pages:
homepage = pysdw.QWidget()
homelayout = pysdw.QVBoxLayout()
homepage.setLayout(homelayout)
stack.addWidget(homepage)

testpage = pysdw.QWidget()
testlayout = pysdw.QVBoxLayout()
testpage.setLayout(testlayout)
stack.addWidget(testpage)

#Widgets
#titlelabel:
hometitle = pysdw.QLabel("Welcom to stockDuck!")
hometitle.setAlignment(Qt.AlignHCenter)
hometitle.setFont(titlefont)
homelayout.addWidget(hometitle)

homebutton = pysdw.QPushButton("home")
homebutton.clicked.connect(lambda: stack.setCurrentWidget(homepage))
testlayout.addWidget(homebutton)

testitle = pysdw.QLabel("Wtest")
testlayout.addWidget(testitle)

testbutton = pysdw.QPushButton("test")
testbutton.clicked.connect(lambda: stack.setCurrentWidget(testpage))
homelayout.addWidget(testbutton)

#Layouts
main_layout = pysdw.QVBoxLayout()      

main_layout.addWidget(stack)
stack.setCurrentWidget(homepage)

window.setLayout(main_layout)
window.resize(400, 200)
window.show()

app.exec()