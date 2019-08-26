import sqlalchemy as sa

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
    engine = sa.create_engine(
        'postgresql://dev:developer@localhost:5432/aiohttp_test'
    )
    metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
