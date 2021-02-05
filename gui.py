import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import  QMainWindow, QApplication, QPushButton
from codesnipper import CodeSnipper

class CodeSnipperGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.brushSize = 3
        self.brushColor = Qt.red
        self.lastPoint = QPoint()
        self.title = "Code Snipper"
        self.start_position=(50, 150, 250, 50)
        self.setWindowTitle("Code Snipper")

        start_snipping_button = QPushButton(self) 
        # start_snipping_button.resize(100,32)
        start_snipping_button.move(75, 10)        
        start_snipping_button.setText("Start Snipping")
        start_snipping_button.adjustSize() 

        start_snipping_button.clicked.connect(self.start_snipping) 

        self.snippingTool = CodeSnipper()
        self.setGeometry(*self.start_position)

        self.show()

    def start_snipping(self):
        if self.snippingTool.background:
            self.close()
        self.snippingTool.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = CodeSnipperGUI()
    sys.exit(app.exec_())
