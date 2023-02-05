from flask import Flask, request
import os
import processor

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def hello_world():
    return 'ikamet decapcha API © 2023 by Alezhu'

@app.post('/parse')
def parse():
    file = request.files['file']
    # os.makedirs("/var/www/uploads")
    # file.save(f"/var/www/uploads/{file.filename}")
    result = processor.process(file)
    return result


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)