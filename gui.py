import tkinter as tk
from PyQt5 import QtWidgets
import sys
from codesnipper import CodeSnipper

#######Functions########################

def startSnipping():
    app = QtWidgets.QApplication(sys.argv)

    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    window = CodeSnipper(tesseract_path)
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())


########################################
root = tk.Tk()
button = tk.Button(root, text = "Start Snipping", command = startSnipping)
button.pack()
root.mainloop()

