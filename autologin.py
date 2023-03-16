#!/usr/bin/env python3
import requests
import getpass


def generate_payload(data: list[str]) -> dict:
    payload = dict()
    for el in data:
        key, val = el.split("=")
        if key == "sessionId" or key == "mgmtBaseUrl":
            payload[key] = val
    payload["MM_Login"] = "OK"
    payload["mode"] = "action"
    payload["action"] = "login"
    payload["accessType"] = "radius"
    payload["username"] = username
    with open("./user.txt", "r") as config:
        lines = config.readlines()
        try:
            password = lines[1]
            payload["password"] = password
        except IndexError:
            payload["password"] = getpass.getpass("Insert password: ", None)
    return payload


def main():
    with requests.Session() as session:
        try:
            url: str = "http://sw-praticelli.unipi.it"
            r = str(session.get(url, allow_redirects=True).content)
            request_url = r[r.find("https://cp-praticelli.unipi.it"):r.find(
                ";", r.find("window.location"))-1:]
            data: list[str] = request_url[request_url.find(
                "cc=1")::].split("&")
            payload = generate_payload(data)
            session.post(request_url, data=payload, verify=False)
            print("Connected... maybe")
            if input("Save the password? (y/n): ") in ["yes", "y"]:
                with open("./user.txt", "a") as config:
                    config.write("\n" + payload["password"])
        except requests.ConnectionError:
            print("Connection Refused, maybe you are already connected.")


if __name__ == "__main__":
    global username
    try:
        with open("./user.txt", "x") as config:
            config.write(input("Insert username: "))
            username = config.readline()
    except:
        with open("./user.txt", "r") as config:
            username = config.readline()
    main()
