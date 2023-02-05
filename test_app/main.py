# from PIL import Image
import argparse
# import cv2
import os
import requests


def main():
    print("Test ikamet decapcha API")
    url = 'http://localhost:5000/parse'
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    for filename in ["Generate.gif", "Generate2.gif"]:
        full_name = os.path.join(__location__, filename)
        with open(full_name, "rb") as file:
            files = {'file': ('capcha.gif', file)}
            response = requests.post(url, files=files)
            print(f"Result {filename}: {response.content}")


if __name__ == '__main__':
    main()
