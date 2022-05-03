#!../../env/bin/python
import requests
from pkglib.Response import Response

# Fetch from internet functions


def fetchRepo(repo):
    main_url = f"https://raw.githubusercontent.com/{str(repo)}/master/lni.yaml"
    r = requests.get(main_url)
    return {"result": r.status_code == 200, "content": r.content}


def fetchImage(repo, imageUrl):
    r = requests.get(f"https://raw.githubusercontent.com/{str(repo)}/master/{imageUrl}")
    return r.status_code == 200, r.content


def fetchContent(url) -> Response:
    r = requests.get(url)
    return Response(r.status_code == 200, r.content)


# Miscellaneous Helper Functions

def buildUrl(repo, relPath):
    return f"https://raw.githubusercontent.com/{str(repo)}/master/{relPath}"

def buildLicenseUrl(repo):
    return f"https://raw.githubusercontent.com/{str(repo)}/master/LICENSE"
