
# pip install flask-sock
from flask import Flask, request, jsonify, Response, render_template
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json
from pathlib import Path

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

data = []
metadata = {}

xscale = 12
title = 'Weight vs Time'
xlabel = "Time (ms)"
ylabel = "Weight (0.1lb)"
# url = 'https://hyeh.pythonanywhere.com/data'
url = 'http://127.0.0.1:5000/data'
path = '/data'
THIS_FOLDER = Path(__file__).parent.resolve()
datafile = THIS_FOLDER / "uploads/sample.json"
# datafile = "./uploads/sample.json"


def getvalleys1(data, threshold, width):
  valleys = []
  numval = width

  for i in range(len(data)):
    if (data[i] < threshold):
      if (numval > 0):
        numval -= 1
        if (numval <=0):
          valleys.append(i)
    else:
      numval = width
  return valleys

#{"metadata":{...}, "data":[]}

def get_data(payload):
    global xscale, metadata, data

    if payload['type'] == 'command':
        if payload['command'] == 'save':
            content = {"metadata":metadata, "data":data}
            with open(datafile, "w") as outfile:
                json.dump(content, outfile)
            return "saved"
        return "unknown command"
    elif payload['type'] == 'metadata':
        metadata = payload['metadata'];
        data = []
        return "metadata received"
    elif payload['type'] == 'data':
        data.append(payload['data'])
        return "data added"
    else:
        return "unknown type"

app = Flask(__name__)

### REMOVE THIS FOR pythonanywhere
# from flask_sock import Sock
# sock = Sock(app)
# @sock.route('/echo')
# def echo(sock):
#     while True:
#         data = sock.receive()
#         sock.send(data)

@app.route('/')
def hello_world():
#     return 'Data Graphing'
    return render_template('index.html')    



@app.route('/data', methods=['GET','POST'])
def receive_data():
    if request.method == 'POST':
        content = request.get_json()
        ret = get_data(content)
        return jsonify({ret: True})

    if request.method == 'GET':
        with open(datafile, "r") as infile:
          content = json.load(infile)
        return jsonify(content)
    # except Exception as e:
        # print(f"Error receiving data: {str(e)}")
        # return jsonify({'success': False, 'error': str(e)})


@app.route('/valleys')
def valleys():
    with open(datafile, "r") as infile:
        content = json.load(infile)

    xscale = content['metadata']['T_sample']
    data = content['data']

    dtasum = [0] * len(data[0]['data'])
    for pkg in data:
        dtasum = [dtasum[i] + pkg['data'][i] for i in range(len(dtasum))]

    valleys = getvalleys1(dtasum, sum(dtasum)/len(dtasum), 10)

    return jsonify(valleys)


@app.route('/linecv')
def canvas():
    return render_template('linecv.html', title=title, xlabel=xlabel, ylabel=ylabel, url=url)

@app.route('/linepl')
def plotly():
    return render_template('linepl.html', title=title, xlabel=xlabel, ylabel=ylabel, url=url)

@app.route('/linepl1')
def plotly1():
    return render_template('linepl1.html', title=title, xlabel=xlabel, ylabel=ylabel, path=path)


@app.route('/linect')
def chartjs():
    return render_template('linect.html', title=title, xlabel=xlabel, ylabel=ylabel, url=url)

@app.route('/linegl')
def googlechart():
    return render_template('linegl.html', title=title, xlabel=xlabel, ylabel=ylabel, url=url)

@app.route('/linemt')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    with open(datafile, "r") as infile:
        content = json.load(infile)

    xscale = content['metadata']['T_sample']
    data = content['data']

    dtasum = [0] * len(data[0]['data'])
    for pkg in data:
        axis.plot([i*xscale for i in range(len(pkg['data']))], pkg['data'], label=pkg['label'])
        dtasum = [dtasum[i] + pkg['data'][i] for i in range(len(dtasum))]
    axis.plot([i*xscale for i in range(len(pkg['data']))], dtasum, label='total')

    valleys = getvalleys1(dtasum, sum(dtasum)/len(dtasum), 10)
    valtime = [i*xscale for i in valleys]
    axis.scatter(valtime, [sum(dtasum)/len(dtasum)] * len(valleys))


    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.set_title(title)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the flask app
# sock = Sock(app)

