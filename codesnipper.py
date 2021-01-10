import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab , Image
import numpy as np
import pytesseract
import pyperclip
import pandas as pd
from pytesseract import Output

class CodeSnipper(QtWidgets.QWidget):
    is_snipping = False
    background = True
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def __init__(self):
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = CodeSnipper.tesseract_path
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def start(self):
        self.setWindowOpacity(0.3)
        CodeSnipper.background = False
        CodeSnipper.is_snipping = True
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert('RGB')
        # treshold_image = self.__tresholdImage(img)

        custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
        d = pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)
        
        df = pd.DataFrame(d)
        print(df.head(-1))
        words = self.__indentCode(df)
        words = "".join(words)
        pyperclip.copy(words) 
    
    def __indentCode(self,image_dataframe):
        indentedCode = []
        df1 = image_dataframe[(image_dataframe.conf!='-1')&(image_dataframe.text!=' ')&(image_dataframe.text!='')]
        sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
        for block in sorted_blocks:
            curr = df1[df1['block_num']==block]
            sel = curr[curr.text.str.len()>3]
            char_w = (sel.width/sel.text.str.len()).mean()
            prev_par, prev_line, prev_left = 0, 0, 0
            text = ''
            for ix, ln in curr.iterrows():
                # add new line when necessary
                if prev_par != ln['par_num']:
                    text += '\n'
                    prev_par = ln['par_num']
                    prev_line = ln['line_num']
                    prev_left = 0
                elif prev_line != ln['line_num']:
                    text += '\n'
                    prev_line = ln['line_num']
                    prev_left = 0
                added = 0  # num of spaces that should be added
                if ln['left']/char_w > prev_left + 1:
                    added = int((ln['left'])/char_w) - prev_left
                    text += ' ' * added 
                text += ln['text'] + ' '
                prev_left += len(ln['text']) + added + 1
            text += '\n'
            # print(text)
            indentedCode.append(text)
        return(indentedCode)
    
    def __tresholdImage(self, imageObject):
        gray = imageObject.convert('L')
        bw = gray.point(lambda x: 0 if x<128 else 255, '1')
        return bw

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CodeSnipper()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())











