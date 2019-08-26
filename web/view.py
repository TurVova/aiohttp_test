import sqlalchemy as sa
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp.web_routedef import RouteTableDef

from web.models import users, addresses

routes = RouteTableDef()


@routes.post('/user')
class UserCreateView(web.View):

    async def post(self):
        db = self.request.app['db']
        body = await self.request.json()

        async with db.acquire() as conn:
            user = await conn.scalar(
                users.insert().values(
                    first_name=body.get('first_name'),
                    email=body.get('email'),
                    gender=body.get('gender'),
                    married=body.get('married'),
                    address_id=await conn.scalar(
                        addresses.select().where(
                            addresses.c.city == body.get('address').get('city')
                        ).where(
                            addresses.c.street == body.get('address').get('street')
                        )
                    )
                ))
        return json_response({'id': user})


@routes.view(r'/user/{id:\d+}')
class UserDetailUpdateDeleteView(web.View):

    async def get(self):
        user_id = self.request.match_info['id']
        db = self.request.app['db']

        try:
            async with db.acquire() as conn:
                user_obj = await conn.execute(
                    sa.select([users, addresses], use_labels=True).select_from(
                        sa.join(
                            users, addresses, users.c.address_id == addresses.c.id
                        )
                    ).where(users.c.id == user_id)
                )
                data = await user_obj.first()
                result = {
                    'id': data.users_id,
                    'email': data.users_email,
                    'first_name': data.users_first_name,
                    'address': {
                        'city': data.addresses_city,
                        'street': data.addresses_street
                    },
                    'gender': data.users_gender,
                    'married': data.users_married,
                }
            return json_response(result)
        except AttributeError:
            return json_response({"Error": f"User with id {user_id} does not exist"})

    async def patch(self):
        user_id = self.request.match_info['id']
        db = self.request.app['db']
        body = await self.request.json()

        try:
            async with db.acquire() as conn:
                await conn.execute(
                    sa.update(users).where(users.c.id == user_id).values(**body)
                )
            return json_response({"Success": f"User with id {user_id} has been updated"})
        except AttributeError:
            return json_response({"Error": f"User with id {user_id} does not exist"})

    async def delete(self):
        user_id = self.request.match_info['id']
        db = self.request.app['db']

        try:
            async with db.acquire() as conn:
                await conn.execute(
                    sa.delete(users).where(users.c.id == user_id)
                )
            return json_response({"Success": f"User with id {user_id} has been deleted"})
        except AttributeError:
            return json_response({"Error": f"User with id {user_id} does not exist"})


@routes.view('/user')
class UserListView(web.View):

    async def get(self):
        db = self.request.app['db']

        async with db.acquire() as conn:
            users_list = await conn.execute(
                sa.select([users, addresses], use_labels=True).select_from(
                    sa.join(
                        users, addresses, users.c.address_id == addresses.c.id
                    )
                )
            )
            result = [{
                'id': user.users_id,
                'email': user.users_email,
                'first_name': user.users_first_name,
                'address': {
                    'city': user.addresses_city,
                    'street': user.addresses_street
                },
                'gender': user.users_gender,
                'married': user.users_married,
            } for user in await users_list.fetchall()]
        return json_response(result)
