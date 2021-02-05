from flask import Flask,request
import sys
from PIL import Image
from base64 import b64decode,decodestring
from io import BytesIO
# from flask_cors import CORS
import pytesseract

from ocrutils import indentCode


app = Flask(__name__)
# CORS(app)

@app.route("/codeSnipper/getText/",methods=["POST"])
def getText():
    data = request.get_json()
    base64_string = data["base64_image"]
    # base64_string = base64_string[ base64_string.find(",") : ]
    # print(base64_string)

    imgdata = b64decode(base64_string)
    image = Image.open(BytesIO(imgdata))



    custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
    d = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

    print(d)
    
    indented_code_list = indentCode(d)
    indented_code = "".join(indented_code_list)
    # print(f"{indented_code}")

    return indented_code







if(__name__=="__main__"):
    if(len(sys.argv) < 2):
         PORT = 3000
    else:
        PORT = int(sys.argv[1])
    app.run(debug=True,port=PORT)



'''
    Received Data:
    {
        "base64_image":"kdslkdsldklsdkskdlsldksl"
    }
'''