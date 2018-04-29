from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('title', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['body'].drop()
    post_meta.tables['post'].columns['content'].create()
    post_meta.tables['post'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['body'].create()
    post_meta.tables['post'].columns['content'].drop()
    post_meta.tables['post'].columns['title'].drop()
