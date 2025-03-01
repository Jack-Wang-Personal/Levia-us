import os
from metacognitive.stream.stream_provider.base_stream import BaseStream
import requests

ENVIRONMENT=os.getenv("ENVIRONMENT", "local")
LOG_URL=os.getenv("LEVIA_LOG_SERVER", "")
VISUAL = os.getenv("VISUAL", False)
class RemoteLogStream(BaseStream):
    def __init__(self):
        pass

    def output(self, log: str, user_id: str, type: str, ch_id: str):
        if ENVIRONMENT == "local" or (not log or not log.strip() or "Initialized metacognitive stream." in log):
            return

        # replace - to /n
        log = log.replace(" - ", "\n")
        # remove extra \n and space
        log = log.strip()
        # Replace multiple consecutive newlines with a single newline
        while "\n\n" in log or "  " in log:
            log = log.replace("\n\n", "\n")
            log = log.replace("  ", " ")
        log = log.strip()
        
        if log == "":
            return
        
        payload = {
            "user_id": user_id,
            "intent": log,
            "type": type,
            "visual": VISUAL,
            "chid": ch_id
        }
        def send_log():
            try:
                response = requests.post(LOG_URL, json=payload)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"send error: {str(e)}")
                return None
                
        import threading
        thread = threading.Thread(target=send_log)
        thread.daemon = True
        thread.start()
        