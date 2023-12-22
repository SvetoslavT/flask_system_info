from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from datetime import datetime
import platform
import os
import psutil
import socket

app = Flask(__name__)
Bootstrap(app)

def get_os_info():
    return f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"

def get_cpu_info():
    return f"{platform.processor()} (Cores: {psutil.cpu_count(logical=False)}, Threads: {psutil.cpu_count(logical=True)})"

def get_memory_info():
    svmem = psutil.virtual_memory()
    return f"Used: {svmem.used / (1024 ** 3):.2f} GB / Total: {svmem.total / (1024 ** 3):.2f} GB"

def get_storage_info():
    partitions = psutil.disk_partitions()
    storage_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_info.append(f"{partition.device} - {partition.mountpoint}: Used {usage.used / (1024 ** 3):.2f} GB / Total {usage.total / (1024 ** 3):.2f} GB")
    return "\n".join(storage_info)

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}, IP Address: {ip_address}"

def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    return boot_time.strftime("%Y-%m-%d %H:%M:%S")

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"

def get_network_activity():
    net_io = psutil.net_io_counters()
    return f"Network Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB / Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB"

def get_uptime():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    return f"System Uptime: {uptime}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_system_info")
def update_system_info():
    data = {
        'Operating System': get_os_info(),
        'CPU': get_cpu_info(),
        'Memory': get_memory_info(),
        'Storage': get_storage_info(),
        'Network': get_network_info(),
        'Boot Time': get_boot_time(),
        'CPU Usage': get_cpu_usage(),
        'Network Activity': get_network_activity(),
        'System Uptime': get_uptime(),
        'Current Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return jsonify(data)


    return render_template("index.html", os_info=os_info, cpu_info=cpu_info, memory_info=memory_info,
                           storage_info=storage_info, network_info=network_info, boot_time=boot_time,
                           cpu_usage=cpu_usage, network_activity=network_activity, uptime=uptime,
                           current_time=current_time)

if __name__ == "__main__":
    app.run(debug=True, port=8011)
