from flask import Flask, request, jsonify
from getSupplies import getSupplies
import concurrent.futures
import IPython
import time

app = Flask(__name__)

@app.route('/printerinfo/<ip>', methods=['GET'])
def printerinfo(ip):
    start_time = time.time()
    ip_list = []
    for address in ip.split(';'):
        ip_list.append(address)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(getSupplies, ip_list))
    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time}")

    return results

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)