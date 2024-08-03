import flet as ft
from type_users.trainer.index.index_trainer import index_trainer
from type_users.trainer.account.account import account_trainer

from type_users.admin.index.index_admin import index_admin
from type_users.admin.account.account import account_admin

# from type_users.user.account.new_account import index_user
from type_users.user.index.index_user import index_user
from type_users.user.account.new_account import profile
from type_users.user.account.edit_account import edit_profile
from type_users.user.account.info import info
from type_users.user.account.info_detail import info_detail


from login.auth import auth
from login.login import login
from login.register import register

# test login_user
# from test import login_test

class Router:
    async def init(self, page: ft.Page):
        self.routes = {
            '/login': await login(page),
            '/auth': await auth(page),
            '/register': await register(page),

            '/index_user': await index_user(page),
            '/profile_user': await profile(page),
            '/edit_profile': await edit_profile(page),
            '/info': await info(page),
            '/info_detail': await info_detail(page),

            '/index_admin': await index_admin(page),

            '/index_trainer': await index_trainer(page),
            
            '/account': await account_trainer(page),

        }
        self.body = ft.Container()

    async def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()