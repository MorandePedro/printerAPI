from getSupplies import getSupplies
import concurrent.futures
import sys
import json

def printerinfo(data):
    ips = [item["IP"] for item in data]
    max_threads = min(10, len(ips))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_ip = {executor.submit(getSupplies, ip): ip for ip in ips}
        
        for future in concurrent.futures.as_completed(future_to_ip):
            result = future.result()
            results.append(result)

    return results

if __name__ == '__main__':
    input_json = sys.stdin.read()

    input_data = json.loads(input_json)
    result = printerinfo(input_data)
    print(result)
    with open("python_log.txt", "w") as file:
        file.write(str(result))
    