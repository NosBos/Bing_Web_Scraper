from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os


def searchFor():
    print("Welcome to the Bing web scraper.\nThis will allow you to easy collect bing data\n1. Links\n2. Images\n"
          "What would you like to scrape: ")

    while True:
        choice = int(input("Enter:"))
        if choice in [1, 2]:
            break
        else:
            print("That is not a valid input")

    search = input("What term would you like to search for: ")

    if choice == 1:

        params = {"q": search}
        r = requests.get("https://www.bing.com/search", params=params)

        soup = BeautifulSoup(r.text, "html.parser")

        results = soup.find("ol", {"id": "b_results"})  # find ol(orderedlist) with id b_results
        links = results.findAllNext("li", {"class": "b_algo"})  # find all li(listitems) with class b_algo

        for item in links:
            item_text = item.find("a").text
            item_href = item.find("a").attrs["href"]

            if item_text and item_href:
                print(item_text)
                print(item_href)
                print("Summary:", item.find("a").parent.parent.find("p").text)
                print("\n")

    if choice == 2:
        param = {"q": search}
        dir_name = search.replace(" ", "_").lower()

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

        r = requests.get("http://www.bing.com/images/search", params=param)

        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.findAll("a", {"class": "thumb"})

        for item in links:
            try:
                img_obj = requests.get(item.attrs["href"])
                print("Getting ", item.attrs["href"])
                title = item.attrs["href"].split("/")[-1]
            except:
                print("Image Failure")
            try:
                img = Image.open(BytesIO(img_obj.content))
            except IOError:
                print("Image cannot be downloaded")
                continue

            print("Title: " + title)
            print("Format: " + img.format + "\n")

            if (title.endswith(("jpg", "png", "gif"))):
                img.save("./" + dir_name + "/" + title, img.format)
            else:
                print("Image file corrupted, could not download")

    searchFor()


searchFor()