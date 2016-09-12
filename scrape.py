import requests
import bs4
from trail import FoundTrail
import time
from datetime import datetime
from db_model import Trail, Event
from sqlalchemy import create_engine, desc
import config
from sqlalchemy.orm import sessionmaker

def main():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        trails = scrape_trails()
        
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
                print('{} status changed to: {}'.format(newEvent.trail.name, newEvent.status))

        session.commit()

        # for trail in session.query(Trail).all():
        #     print(trail.name)
        #     for event in trail.events:
        #         print '{} as of {}'.format(event.status, event.timestamp)

        time.sleep(10)

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

