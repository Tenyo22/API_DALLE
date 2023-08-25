import os
import openai
import base64
import shutil

from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploader', methods=["POST"])
def uploader():
    if request.method == 'POST':
        f = request.values['text-image']

        res = openai.Image.create(
            prompt=f,
            n=2,
            size="256x256",
            response_format='b64_json'
        )
        # print(res)
        for i in range( 0, len(res['data'])):
            b64 = res['data'][i]['b64_json']
            filename = f'image_{i}.png'
            print('Saving file ' + filename)
            with open(filename, 'wb') as image:
                image.write(base64.urlsafe_b64decode(b64))
            image.close()
            shutil.copyfile(filename, 'static/'+filename)
            
        return render_template('imagen.html', value=f)

if __name__ == '__main__':
    app.run(debug=True)