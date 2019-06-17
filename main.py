from flask import Flask, render_template, Response
from camera import detection,streaming
from hello2 import streaming


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame =streaming()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(host='192.168.59.181',port=3008, debug=True)