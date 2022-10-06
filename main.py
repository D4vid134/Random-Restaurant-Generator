from ui import *
from webscr_maps import *
import sys

# GUI Application 
class WebScr_Project(Ui_MainWindow):
    
    def __init__(self,window):
        self.setupUi(window)
        self.pushButton.clicked.connect(self.click)
        
    def click(self):
        if self.lineEdit_2.text() == '':
            address = self.lineEdit.text()
        else:  address = self.lineEdit_2.text() + ", " + self.lineEdit.text() 
        
        res, rating, dir = WebScrape.pickFood(
            self.lineEdit_2.text() + " " + self.lineEdit.text() ,WebScrape.driver)
        self.setup_popup(address, res, rating, dir)
    
    
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

ui = WebScr_Project(MainWindow)

MainWindow.show()
app.exec_()
