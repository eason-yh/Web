from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
klass = Table('klass', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR),
)

registrations = Table('registrations', pre_meta,
    Column('student_id', INTEGER),
    Column('klass_id', INTEGER),
)

student = Table('student', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['klass'].drop()
    pre_meta.tables['registrations'].drop()
    pre_meta.tables['student'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['klass'].create()
    pre_meta.tables['registrations'].create()
    pre_meta.tables['student'].create()
