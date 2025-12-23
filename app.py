import sys
from fisims import *
import read_data as rd
import PySide6.QtWidgets as pysdw
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTime,QTimer

class StockLink():
  def __init__(self,stockname="NVDA",linkname="NVDA chart"):
    stock_link = pysdw.QPushButton(linkname)
    stock_link.clicked.connect(
        lambda: QDesktopServices.openUrl(QUrl(f"https://de.finance.yahoo.com/chart/{stockname}"))
    )
    stock_link.setStyleSheet("""
    QPushButton {
        background: transparent;
        color: #ffffff;
        text-align: left;
        border: None                     
    }
    QPushButton:hover {
        text-decoration: underline;
    }
    """)
    stock_link.setSizePolicy(
        QSizePolicy.Maximum,
        QSizePolicy.Fixed
    )
    self.stocklink = stock_link

#the stcok data part:
chunk = rd.data_chunk()
sim = Sim(0)

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

tradingpage = pysdw.QWidget()
tradinglayout = pysdw.QVBoxLayout()
tradingpage.setLayout(tradinglayout)
stack.addWidget(tradingpage)

#Widgets
#sidebar:
sidebar = pysdw.QWidget()
sidebar.setObjectName("sidebar")
sidebar.setStyleSheet("""
#sidebar {
    background-color: #1e1e1e;
}
""")
sidebarlayout = pysdw.QVBoxLayout()

#titlelabel:
hometitle = pysdw.QLabel("Welcom to stockDuck!")
hometitle.setAlignment(Qt.AlignHCenter)
hometitle.setFont(titlefont)
homelayout.addWidget(hometitle)
moneybar = pysdw.QLineEdit()
moneybar.setObjectName("moneybarhomepage")
moneybar.setStyleSheet("""
#moneybarhomepage {
    background-color: #ffd429;
    color: #000000;
}""")
moneybar.setPlaceholderText("Please only digits!")
moneybar.setMinimumWidth(200)
def enter_money():
  sim.cash += int(moneybar.text())
  informationlabelhomepage.setText(f"You currently have {sim.cash} $ (in-game, not exchangable)\n To get more money you can enter any amount into the text-field.\n To take away money, enter a negative amount.")
moneybar.returnPressed.connect(enter_money)
homelayout.addWidget(moneybar,alignment=Qt.AlignRight)
informationlabelhomepage = pysdw.QLabel(f"You currently have {sim.cash} $ (in-game, not exchangable)\n To get more money you can enter any amount into the text-field.\n To take away money, enter a negative amount.")
informationlabelhomepage.setFont(mainfont)
informationlabelhomepage.setObjectName("informationlabelhomepage")
informationlabelhomepage.setStyleSheet("color: #ffffff;")
homelayout.addWidget(informationlabelhomepage)

homebutton = pysdw.QPushButton()
homebutton.setIcon(QPixmap("images/home_icon.png"))
homebutton.clicked.connect(lambda: stack.setCurrentWidget(homepage))
homebutton.setFlat(True) 
homebutton.setToolTip("Home")
sidebarlayout.addWidget(homebutton)


#tradingpage:
topbar = pysdw.QHBoxLayout() 
searchbar = pysdw.QLineEdit()
searchbar.setStyleSheet("""
QWidget {
    background-color: #ffd429;
    color: #000000;
}""")
searchbar.setPlaceholderText("Search stock Symbols here.")
searchbar.setMinimumWidth(200)
topbar.addWidget(searchbar)
tradinglayout.addLayout(topbar)

#the searchbar:
searcharea = pysdw.QWidget()
searcharea.setStyleSheet("""
QWidget {
    background-color: #1e1e1e;
}
""")
searchresults = pysdw.QVBoxLayout()
searcharea.setLayout(searchresults)

scrollarea = pysdw.QScrollArea()
scrollarea.setStyleSheet("""
QWidget {
    border: None;
}
""")
scrollarea.setWidgetResizable(True)
scrollarea.setWidget(searcharea)
scrollarea.setSizePolicy(
    pysdw.QSizePolicy.Expanding,
    pysdw.QSizePolicy.Expanding
)
scrollarea.setMinimumHeight(200)
tradinglayout.addWidget(scrollarea,1)
tradinglayout.addStretch(0)
#the stock design:
stocknamelabel = pysdw.QLabel("")
stocknamelabel.setFont(mainfont)
stocknamelabel.setAlignment(Qt.AlignTop)
searchresults.addWidget(stocknamelabel)
pricelabel = pysdw.QLabel("")
searchresults.addWidget(pricelabel)
resultlabel = StockLink("","").stocklink
searchresults.addWidget(resultlabel,alignment=Qt.AlignLeft | Qt.AlignTop)
loadingstock = pysdw.QLabel("")
loadingstock.setPixmap(QPixmap("images/finished_loading.png").scaled(32,32))
topbar.addWidget(loadingstock)
stockbuyselllayout = pysdw.QHBoxLayout()
stockbuysellwidgetplaceholder = pysdw.QWidget()
stockbuysellwidgetplaceholder.setObjectName("stockBuySell")
stockbuysellwidgetplaceholder.setStyleSheet("""
#stockBuySell {
    background-color: #121212;
    border-radius: 12px;
}
""")
stockbuysellwidgetplaceholder.setLayout(stockbuyselllayout)
searchresults.addWidget(stockbuysellwidgetplaceholder)
buystockbutton = pysdw.QPushButton("Buy")
buystockbutton.setStyleSheet("""
QWidget {
    background-color: #21D12D;
    color: white;
    padding: 4px;
}
""")
buystockbutton.setToolTip("Buy a stock")
amountspin = pysdw.QSpinBox()
amountspin.setRange(1, 1)
# Min / Max
amountspin.setValue(1)
amountspin.setSuffix(" stock(s)")
stockbuyselllayout.addWidget(buystockbutton)
stockbuyselllayout.addWidget(amountspin)
sellstockbutton = pysdw.QPushButton("Sell")
sellstockbutton.setStyleSheet("""
QWidget {
    background-color: #D10A0A;
    color: white;
    padding: 4px;
}
""")
sellstockbutton.setToolTip("Sell a stock")
amountspin1 = pysdw.QSpinBox()
amountspin1.setRange(1, 5)
# Min / Max
amountspin1.setValue(1)
amountspin1.setSuffix(" stock(s)")
ordertype = pysdw.QComboBox()
ordertype.addItems(["Long", "Short"])
stockbuyselllayout.addWidget(ordertype)
stockbuyselllayout.addWidget(amountspin1)
stockbuyselllayout.addWidget(sellstockbutton)

def on_search_trading_layout0():
  loadingstock.setPixmap(QPixmap("images/loading_icon.png").scaled(32,32))
  QApplication.processEvents()
  text = searchbar.text().strip()
  if not text:
    return
  resultlabel.setText(f"view {text} chart (extern)")
  resultlabel.clicked.connect(
        lambda: QDesktopServices.openUrl(QUrl(f"https://de.finance.yahoo.com/chart/{text}"))
    )
  stocknamelabel.setText(searchbar.text()+":"+f" ({datetime.now().strftime("%Y_%m_%d %H:%M:%S")})")
  pri = chunk.up_to_date_price(searchbar.text())
  amountspin.setRange(1, int(sim.cash/pri))
  try:
    amountspin1.setRange(1, int(sim.stocks[text][ordertype.currentText().lower()]))
  except KeyError:
     amountspin1.setRange(0, 0)
  if pri != -1:
    pricelabel.setText(f"{pri} $")
  else:
    pricelabel.setText("Stock/Symbol could not be found")
    stocknamelabel.setText("")
    resultlabel.setText("")
  loadingstock.setPixmap(QPixmap("images/finished_loading.png").scaled(32,32))
searchbar.returnPressed.connect(on_search_trading_layout0)

def on_sell():
   sim.sell_order(stocknamelabel.text(),int(amountspin1.text().replace(" stock(s)","")),ordertype.currentText().lower())
def on_buy():
   sim.buy_order(stocknamelabel.text(),int(amountspin1.text().replace(" stock(s)","")),ordertype.currentText().lower())
sellstockbutton.clicked.connect(on_sell)
buystockbutton.clicked.connect(on_buy)


#automatically updating the stock price
stockupdatetimer = QTimer()
stockupdatetimer.timeout.connect(on_search_trading_layout0)
stockupdatetimer.start(10000)

#deletebutton
deletbutton = pysdw.QPushButton()
deletbutton.setIcon(QPixmap("images/delete_icon.png"))
deletbutton.setToolTip("Delete search-bar content")
deletbutton.setStyleSheet("""
QToolTip {
    background-color: #2a2a2a;
    color: white;
    border: 1px solid #444;
    padding: 4px;
}
""")
topbar.addWidget(deletbutton)

def on_delete():
   searchbar.setText("")
deletbutton.clicked.connect(on_delete)

#sidebar button
tradingbutton = pysdw.QPushButton("")
tradingbutton.setIcon(QPixmap("images/trading_icon.webp"))
tradingbutton.clicked.connect(lambda: stack.setCurrentWidget(tradingpage))
tradingbutton.setFlat(True)
tradingbutton.setToolTip("Trading page")
tradingbutton.setStyleSheet("""
QToolTip {
    background-color: #2a2a2a;
    color: white;
    border: 1px solid #444;
    padding: 4px;
}
""")
sidebarlayout.addWidget(tradingbutton)

#sidebar clock:
clockfont = QFont()
mainfont.setFamily("Bauhaus 93")
mainfont.setPointSize(15)
mainfont.setBold(True)
mainfont.setItalic(False)
clocklabel = pysdw.QLabel("")
clocklabel.setStyleSheet("""
QWidget {
    background-color: #1e1e1e;
}
"""
)
clocklabel.setFont(clockfont)
def update_time():
    if ":" in clocklabel.text():
        clocklabel.setText(QTime.currentTime().toString("HH|m|ss"))
    else:
       clocklabel.setText(QTime.currentTime().toString("HH:mm:ss"))
timer = QTimer()
timer.timeout.connect(update_time)
fm = clocklabel.fontMetrics()
clocklabel.setFixedWidth(fm.horizontalAdvance("88:88:88"))
timer.start(500)
#update every 500 ms for a smooth blinking of the ":"
update_time() 
sidebarlayout.addStretch(9)
sidebarlayout.addWidget(clocklabel,alignment=Qt.AlignHCenter)

#Layouts
main_layout = pysdw.QHBoxLayout()  
sidebarlayout.addStretch(2)
sidebar.setLayout(sidebarlayout)    

stack.setCurrentWidget(homepage)
main_layout.addWidget(sidebar,1)
main_layout.addWidget(stack,9)

window.setLayout(main_layout)
window.resize(400, 200)
window.show()

app.exec()