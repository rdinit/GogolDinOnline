from flask import Flask, send_file

app = Flask('mywebapp')

sessions = dict()

@app.route('/')
def index():
    return send_file('gamepad-home.html')

@app.route('/get-ssid')
def getssid():
    ss = open('data/sessions.txt', 'r')
    mx = int(ss.read())
    ss.close()

    ssid = str(mx + 1)

    ss = open('data/sessions.txt', 'w')
    ss.write(ssid)
    ss.close()

    f = open('get_ssid.html', 'r', encoding='utf-8')
    t = f.read()
    f.close()

    t = t.replace('ss_id', ssid)
    return t

@app.route('/gamepad/<ss_id>')
def play(ss_id):
    f = open('button.html', 'r', encoding='utf-8')
    t = f.read()
    f.close()

    t = t.replace('ss_id', ss_id)
    return t

@app.route('/gamepad/<ssid>/k_up_pressed', methods=['POST'])
def button_pressed(ssid):
    sessions[ssid] = '1'
    return 'written'


@app.route('/getbuttons/<ssid>')
def get_buttons(ssid):
    t = sessions[ssid]
    sessions[ssid] = '0'
    return t


app.run(port=1111, host='127.0.0.1')