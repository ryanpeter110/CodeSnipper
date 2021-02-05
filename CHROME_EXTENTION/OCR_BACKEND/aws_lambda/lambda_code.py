import pytesseract
from PIL import Image
from base64 import b64decode
from io import BytesIO
import pandas as pd

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


def lambda_handler(event, context):
   
    base64_string = event["base64_image"]
    # base64_string = base64_string[ base64_string.find(",") : ]
    
    imgdata = b64decode(base64_string)
    image = Image.open(BytesIO(imgdata))
    
    custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
    d = pytesseract.image_to_data(image, config=custom_config,output_type=pytesseract.Output.DICT)

    indented_code_list = indentCode(d)
    indented_code = "".join(indented_code_list)
    
    
    return indented_code
