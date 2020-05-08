import requests

def get_events(ssid):
    rq = requests.get('http://127.0.0.1:1111/getbuttons/' + ssid)
    t = rq.text
    rtrn = []
    if t[0] == '1':
        rtrn.append('K_UP')

    return rtrn

if __name__ == '__main__':
    pass