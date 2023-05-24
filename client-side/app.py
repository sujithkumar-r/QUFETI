from flask import Flask, request, jsonify, render_template
from PIL import Image
import requests
from io import BytesIO
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/preds", methods=['POST'])
def submit():
    cloth = request.files['cloth']
    model = request.files['model']

    # Start Ngrok tunnel
    ngrok_url = ngrok.connect(5000)  # Replace 5000 with the port number of your server
    # Get the Ngrok URL
    url = ngrok_url + "/api/transform"
    print("Sending request to:", url)
    response = requests.post(url=url, files={"cloth":cloth.stream, "model":model.stream})
    op = Image.open(BytesIO(response.content))

    buffer = BytesIO()
    op.save(buffer, 'png')
    buffer.seek(0)

    data = buffer.read()
    data = base64.b64encode(data).decode()


    return render_template('index.html', op=data)
    # return render_template('index.html', test=True)

if __name__ == '__main__':
    app.run(debug=True)
