import datetime
import json
import time

from pyngrok import ngrok, conf
from colorama import Fore


conf.set_default(conf.PyngrokConfig(ngrok_path="/snap/bin/ngrok"))


def launch_ngrok():
    http_tunnel = ngrok.connect(addr=8001, bind_tls=True)
    return http_tunnel.public_url


while True:
    try:
        now = datetime.datetime.now()
        tunnel = launch_ngrok()
        print(Fore.GREEN, f"[INFO] {now} was launch Ngrok tunnel. Tunnel:  {tunnel}\n")

        with open("ngrok_tunnel.json", "w", encoding="utf-8") as f:
            data = {
                "tunnel": tunnel
            }
            json.dump(data, f, ensure_ascii=False, indent=4)

        second_tunnel = ngrok.connect(addr=80, bind_tls=True)
        print(Fore.GREEN, f"[INFO] {now} was launch second Ngrok tunnel for test. Tunnel:  {second_tunnel.public_url}\n\n")

        # каждые 10 минут обновляется url ngroks
        time.sleep(6000)
    except Exception as e:
        now = datetime.datetime.now()
        print(Fore.RED, f"[INFO] {now} Raise exception: {e}\n")
        ngrok.kill()
