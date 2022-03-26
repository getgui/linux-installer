#!../../env/bin/python
import requests

def fetchRepo(repo):
    main_url = f"https://raw.githubusercontent.com/{str(repo)}/master/lni.yaml"
    r = requests.get(main_url)
    return {"result": r.status_code == 200}
