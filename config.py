import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

facebook = {
    "app_secret": 'd6d6fec7e52f533c31090be3f45ff022',
    "app_id": '1124747760929464',
    "page_id"      : "1821645501398664",
    "access_token" : "EAAPZB877AirgBALtkZASEKhiccytjVZArDqOWCCCbCgr1fbi2KbUvzUStpxkxlJhCD1ZC23j78OFs0d3LpGSkMgtDghboOoWqv9WHcwAZAZBgZA2Q952NnvSFk39VFxaZARBmCLAWuI8FdwNMjJNJL2YXKDTj0tDYSltAVLT57dERQZDZD"
    }
