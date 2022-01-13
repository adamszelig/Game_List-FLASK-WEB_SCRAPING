import requests
import lxml
from bs4 import BeautifulSoup
import csv
import pandas as pd


URL = "https://www.gamepressure.com/games/pc/33"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "hu-HU,hu;q=0.9,en;q=0.8"
}

def get_game_data():
    response = requests.get(URL)
    # If Header is needed:
    # response = requests.get(URL, headers=header)
    # print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    # Change parser tye if needed
    # soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify())

    header = ['title', 'image_src', 'genre', 'release_date', 'description', 'link']

    data = []
    # data.append({'title':, 'image_src':, 'genre':, 'release_date':, 'description':, 'link':})

    # < div class ="lista lista-gry" >
    #     <div class="box">
    #         <a class="pic-c" href="/games/lost-ark/zc3f0c#pc" title="Lost Ark">
    #             <img alt="Lost Ark" class="pic" data-src="https://cdn.gracza.pl/i/h/10/513595492.jpg" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3C/svg%3E"/>
    #         </a>
    #         <a href="/games/lost-ark/zc3f0c#pc">
    #             <h5>Lost Ark</h5>
    #         </a>
    #         <p class="opis-b"><b>RPG</b>11 February 2022</p>
    #         <p>A free-to-play online action-RPGin.</p>
    #         <p class="plat"></p>
    #     </div>


    box = soup.select(selector=".lista .box")
    for sub_box in box:

        title = sub_box.find(class_="pic-c").get('title')
        image_src = sub_box.find(class_="pic").get('data-src')
        genre = sub_box.select(selector=".opis-b b")[0].get_text()
        # release_date = sub_box.select(selector=".opis-b")[0].get_text().split(" ", 1)[1]
        release_date = sub_box.select(selector=".opis-b")[0].get_text().replace(genre+" ", "")
        description = sub_box.select(selector="p")[1].get_text()
        link = "https://www.gamepressure.com" + sub_box.find(class_="pic-c").get('href')

        # error handling needed - add "" when there is no data for a key
        data.append({'title': title, 'image_src': image_src, 'genre': genre, 'release_date': release_date, 'description': description, 'link': link})
        # print(data[-1])


    with open('game.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    # df = pd.read_csv("game.csv")
    # print(df)

get_game_data()