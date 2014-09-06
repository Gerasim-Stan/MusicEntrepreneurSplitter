from PyQt4.QtGui import *
from mainWindow import *


app = QApplication(sys.argv)
playerWindow = MainWindow()
playerWindow.show()
sys.exit(app.exec_())
