import json

def log_event(event):

    with open("security_log.json", "a") as f:
        json.dump(event, f)
        f.write("\n")