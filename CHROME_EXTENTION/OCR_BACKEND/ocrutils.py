import pandas as pd
# import numpy as np

def indentCode(image_data):
    image_dataframe = pd.DataFrame(image_data)
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

import colorsys
from PIL import Image
im = Image.open("aa.png")
ld = im.load()
width, height = im.size
for y in range(height):
    for x in range(width):
        r,g,b = ld[x,y]
        h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)

        if s>0.5:                    # <--- here onwards is my attempted Python
           ld[x,y] = (0,0,0)
        else:
           ld[x,y] = (255,255,255)
# im.show()