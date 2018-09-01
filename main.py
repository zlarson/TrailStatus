import requests
import bs4
from models import FoundTrail
from trail_scraper import TrailScraper
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

    trail_scraper = TrailScraper()

    trails = trail_scraper.getTrailStatusList()

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
            messages.append(create_message(newEvent.trail.name, newEvent.status))

    if len(messages) > 0:
        tell_everyone("\n".join(messages))

    session.commit()


def create_message(trail_name, trail_status):
    if trail_status.lower() == 'open' or trail_status.lower() == 'closed':
        return '{} trails are {}!'.format(trail_name, trail_status)
    else:
        return '{} trail status: {}'.format(trail_name, trail_status)


def tell_everyone(message):
    api = facebook.GraphAPI(config.facebook['access_token'])
    api.put_wall_post(message)


if __name__ == "__main__":
    main()
