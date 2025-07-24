from flask import Flask, render_template, request, Response
import threading, queue, time
from list_interfaces import get_interfaces
from ping import ping_host
from sniff_packets import sniff_packets
from beacon_scanner import beacon_scan
from probe_tracker import probe_track
from wifi_analyzer import wifi_analyze

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    input_text = ""
    input_id = ""
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        input_id = request.form.get("input_id", "")
        # Do something with the values here
        print(f"Received: Text = {input_text}, ID = {input_id}")
    return render_template("index.html", input_text=input_text, input_id=input_id)


def test_stream(label):
    for i in range(0, 100):
        yield f'data: "{label}"\n\n'
        time.sleep(0.1)


class StopFlag:
    def __init__(self):
        self.stop = False


@app.route("/list-interfaces")
def list_interfaces():
    print('Listing interfaces')

    def stream():
        interfaces = get_interfaces()
        for ifa in interfaces:
            yield f"data: {ifa}\n\n"

    return Response(stream(), mimetype='text/event-stream')


@app.route("/ping")
def ping():
    target = request.args.get("target", "")
    iface = request.args.get("iface", "")

    def stream():
        if not target:
            yield f"data: Error: No target provided\n\n"
            return

        yield f"data: Pinging {target} using interface {iface}...\n\n"
        results = ping_host(target)
        for line in results:
            yield f"data: {line}\n\n"

    return Response(stream(), mimetype='text/event-stream')


@app.route("/packet-sniffer")
def packet_sniffer():
    print('Sniffing packets')
    iface = request.args.get("iface", "wlan0")
    q = queue.Queue()
    stop_flag = StopFlag()

    def stream():
        thread = threading.Thread(target=sniff_packets, args=(iface, q, stop_flag), daemon=True)
        thread.start()
        try:
            while True:
                packet_summary = q.get()
                yield f"data: {packet_summary}\n\n"
        except GeneratorExit:
            stop_flag.stop = True

    return Response(stream(), mimetype="text/event-stream")


@app.route("/beacon-scanner")
def beacon_scanner():
    q = queue.Queue(maxsize=100)
    stop_flag = type("StopFlag", (), {"stop": False})()

    iface = request.args.get("iface", "wlan1")

    def stream():
        thread = threading.Thread(target=beacon_scan, args=(iface, q, stop_flag), daemon=True)
        thread.start()
        try:
            while True:
                msg = q.get()
                yield f"data: {msg}\n\n"
        except GeneratorExit:
            stop_flag.stop = True

    return Response(stream(), mimetype='text/event-stream')


@app.route("/probe-tracker")
def probe_tracker():
    q = queue.Queue(maxsize=100)
    stop_flag = type("StopFlag", (), {"stop": False})()

    iface = request.args.get("iface", "wlan1")

    def stream():
        thread = threading.Thread(target=probe_track, args=(iface, q, stop_flag), daemon=True)
        thread.start()
        try:
            while True:
                msg = q.get()
                yield f"data: {msg}\n\n"
        except GeneratorExit:
            stop_flag.stop = True

    return Response(stream(), mimetype="text/event-stream")


@app.route("/wifi-analyzer")
def wifi_analyzer():
    q = queue.Queue(maxsize=100)
    stop_flag = type("StopFlag", (), {"stop": False})()

    iface = request.args.get("iface", "wlan1")

    def stream():
        thread = threading.Thread(target=wifi_analyze, args=(iface, q, stop_flag), daemon=True)
        thread.start()
        try:
            while True:
                msg = q.get()
                yield f"data: {msg}\n\n"
        except GeneratorExit:
            stop_flag.stop = True

    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
