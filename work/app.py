from flask import Flask, render_template, request
import friend_on_map
import twitter2

app = Flask(__name__)


@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('index.html')

@app.route('/data_send', methods = ['POST'])
def get_data():
    global pay
    pay = request.form['pay']
    print("user:" + pay)
    return render_template('index.html')

@app.route('/data_send/Friends_locations', methods= ['POST'])
def show_map():
    mapa = twitter2.main(pay)
    mapa_1 = friend_on_map.main()
    ip = request.remote_addr
    return render_template('Friends_locations.html', user_ip=ip)

if __name__ == '__main__':
    app.run(debug = True, host = '127.0.0.1', port = 8080)
    