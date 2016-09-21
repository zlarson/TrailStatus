import requests
import bs4
from models import FoundTrail
import time
from datetime import datetime
from db_model import Trail, Event
from sqlalchemy import create_engine, desc
import config
from sqlalchemy.orm import sessionmaker
import facebook

def main():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        trails = scrape_trails()

        messages = []
        
        for trail in trails:
            existing = session.query(Trail).filter(Trail.name == trail.name).all()
            
            if len(existing) == 0:
                newTrail = Trail(name=trail.name)
                session.add(newTrail)
            else:
                newTrail = existing[0]

            trailEvents = newTrail.events.order_by(desc(Event.timestamp))

            if trailEvents.count() == 0 or trailEvents[0].status.lower() != trail.status.lower():
                newEvent = Event(status=trail.status, timestamp=datetime.utcnow(), trail=newTrail)
                session.add(newEvent)
                messages.append(create_pretty_message(newEvent.trail.name, newEvent.status))

        if len(messages) > 0:
            tell_the_world("\n".join(messages))

        session.commit()

        time.sleep(10 * 60) # 10 minutes

def create_pretty_message(trailName, trailStatus):
    if trailStatus.lower() == 'open' or trailStatus.lower() == 'closed':
        return '{} trails are {}!'.format(trailName, trailStatus)
    else:
        return '{} trail status: {}'.format(trailName, trailStatus)


def tell_the_world(message):
    api = facebook.GraphAPI(config.facebook['access_token'])
    status = api.put_wall_post(message)

def scrape_trails():
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

if __name__ == "__main__":
    main()

