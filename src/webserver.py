#!/bin/env ./.venv/bin/python3

from flask import Flask, render_template, request, Response
import threading, queue, time
from modules.list_interfaces import ListInterfacesModule
from modules.module import Module
from modules.ping import PingModule
from modules.sniff_packets import PacketSnifferModule
from modules.beacon_scanner import BeaconScannerModule
from modules.probe_tracker import ProbeTrackerModule
from modules.wifi_security import SecurityAnalyzerModule
from modules.wifi_teacher import TeacherModule

app = Flask(__name__, template_folder="web/templates", static_folder='web/static')


# TODO: Monitor mode switch for given interface

def stream_module_output(module: Module):
    client_closed = False

    print(f'Starting {str(module)}')
    yield f'data: > Starting {str(module)}\n\n'
    module.start()
    try:
        while module.is_running():
            while not module.output_queue.empty():
                mes = module.output_queue.get(timeout=0.5)
                yield f'data: {mes}\n\n'
    except GeneratorExit:
        module.stop()
        print(f'Client stopped {str(module)}')
        client_closed = True
    finally:
        module.stop()
        while not (client_closed or module.output_queue.empty()):
            mes = module.output_queue.get(timeout=0.5)
            yield f'data: {mes}\n\n'

    print(f'Stopping {str(module)}')


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/list-interfaces")
def list_interfaces():
    return Response(stream_module_output(ListInterfacesModule()), mimetype='text/event-stream')


@app.route("/ping")
def ping():
    target = request.args.get("target", "")

    return Response(stream_module_output(PingModule(target)), mimetype='text/event-stream')


@app.route("/packet-sniffer")
def packet_sniffer():
    iface = request.args.get("iface", "wlan0")

    return Response(stream_module_output(PacketSnifferModule(iface)), mimetype="text/event-stream")


@app.route("/beacon-scanner")
def beacon_scanner():
    iface = request.args.get("iface", "wlan1")

    return Response(stream_module_output(BeaconScannerModule(iface)), mimetype='text/event-stream')


@app.route("/probe-tracker")
def probe_tracker():
    iface = request.args.get("iface", "wlan1")

    return Response(stream_module_output(ProbeTrackerModule(iface)), mimetype="text/event-stream")


@app.route("/wifi-analyzer")
def wifi_analyzer():
    iface = request.args.get("iface", "wlan1")

    return Response(stream_module_output(SecurityAnalyzerModule(iface)), mimetype='text/event-stream')


@app.route("/wifi-teacher")
def wifi_teacher():
    iface = request.args.get("iface", "")

    return Response(stream_module_output(TeacherModule(iface)), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
