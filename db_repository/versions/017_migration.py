from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
klass = Table('klass', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
)

registrations = Table('registrations', post_meta,
    Column('student_id', Integer),
    Column('klass_id', Integer),
)

student = Table('student', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['klass'].create()
    post_meta.tables['registrations'].create()
    post_meta.tables['student'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['klass'].drop()
    post_meta.tables['registrations'].drop()
    post_meta.tables['student'].drop()
