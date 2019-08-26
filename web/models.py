import sqlalchemy as sa

from utils.config import load_config

metadata = sa.MetaData()

addresses = sa.Table(
    'addresses', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('city', sa.String(255)),
    sa.Column('street', sa.String(255))
)

users = sa.Table(
    'users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('first_name', sa.String(255)),
    sa.Column('email', sa.String(255), unique=True),
    sa.Column('gender', sa.String(1)),
    sa.Column('married', sa.Boolean()),
    sa.Column('address_id', None, sa.ForeignKey('addresses.id')),
)


def create_db():
    config = load_config()
    engine = sa.create_engine(
        f'postgresql://{config["db"]["user"]}:{config["db"]["password"]}'
        f'@{config["db"]["host"]}:{config["db"]["port"]}/{config["db"]["database"]}'
    )
    metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
