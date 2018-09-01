import requests
import bs4
from found_trail import FoundTrail


class TrailScraper:
    def getTrailStatusList(self):
        index_url = 'http://www.qcforc.org/content.php'
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        items = soup.findAll("div", {"id": "trailblock"})

        list = []

        for item in items:
            status = item.contents[1].contents[0]
            name = item.contents[0].contents[0]
            list.append(FoundTrail(name, status))

        return list
