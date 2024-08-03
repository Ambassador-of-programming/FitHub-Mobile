import flet as ft
import aiohttp
import aiofiles
import json
from navigation.bar import Appbar

async def account_admin(page: ft.Page):
    class Container:
        def __init__(self):
            self.photo = ft.Image(
                src='https://picsum.photos/200/200?0',
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            )
            
            self.email = ft.Text(value='Ваша почта: None')
            self.first_name = ft.Text(value='Ваше имя: None')
            self.last_name = ft.Text(value='Ваше фамилия: None')
            self.phone_number = ft.Text(value='Ваш номер телефона: None')
            self.date_register = ft.Text(value='Дата регистрации: None')
            self.verify_email = ft.Text(value='Верификация почты: None')

            self.edit_dropdown = ft.Dropdown(width=100,
                options=[
                    ft.dropdown.Option("first_name"),
                    ft.dropdown.Option("last_name"),
                    ft.dropdown.Option("phone_number"),

                ], visible=False)
            self.edit_textfield = ft.TextField(hint_text='Номер телефона', visible=False)
            self.edit_button = ft.ElevatedButton(text='Редактировать', on_click=self.edit_buttond, visible=False)

            self.update_account = ft.ElevatedButton(text='Обновить', col=6, on_click=self.updates_account)
            self.edit_account = ft.ElevatedButton(text='Редактировать данные', col=6, on_click=self.edit_account_b)
            self.delete_account = ft.ElevatedButton(text='Удалить аккаунт', col=6, on_click=self.delete_account_button)
            self.verify_emails = ft.ElevatedButton(text='Подтвердить почту', col=6, on_click=self.verify_email_button)
            self.back_index_page = ft.ElevatedButton(text='Вернуться в главное меню', on_click=self.back_index_page_button)
            self.back_login = ft.ElevatedButton(text='Выйти', on_click=self.back_login_button)

        
        async def back_login_button(self, event):
            page.go("/login")

        async def back_index_page_button(self, event):
            page.go("/index_admin")

        async def verify_email_button(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)

            url = 'http://nexus-hub.pro/user/user/verifi_email'
            payload = {
                "email": email,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
            
            await self.updates_account(email)

        async def updates_account(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)

            url = 'http://nexus-hub.pro/user/user/get_account'
            payload = {
                "email": email,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                        
            self.email.value = f"Ваша почта: {data['user'][0][0]}"
            self.email.update()

            self.first_name.value = f"Ваше имя: {data['user'][0][1]}"
            self.first_name.update()
            
            self.last_name.value = f"Ваше фамилия: {data['user'][0][2]}"
            self.last_name.update()

            self.phone_number.value = f"Ваш номер телефон: {data['user'][0][3]}"
            self.phone_number.update()

            self.date_register.value = f"Дата регистрации: {data['user'][0][6]}"
            self.date_register.update()

            self.verify_email.value = f"Верификация почты: {data['user'][0][5]}"
            self.verify_email.update()

        async def delete_account_button(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)

            url = 'http://nexus-hub.pro/admin/admin/delete_user'
            payload = {
                "email": email,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()

            appbar = Appbar(page)
            page.appbar = await appbar.content()

            page.go('/login')

        async def edit_account_b(self, event):
            self.edit_dropdown.visible = True
            self.edit_dropdown.update()
            self.edit_textfield.visible = True
            self.edit_textfield.update()
            self.edit_button.visible = True
            self.edit_button.update()
        
        async def edit_buttond(self, event):
            if all([self.edit_dropdown.value, self.edit_textfield.value]):
                async with aiofiles.open('login/email.json', mode='r') as file:
                    data = await file.read()
                    email =  json.loads(data).get("email", None)

                url = 'http://nexus-hub.pro/user/user/edit_account'
                payload = {
                    "email": email,
                    "parametr": self.edit_dropdown.value,
                    "parametr_value": self.edit_textfield.value
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        data = await response.json()

                self.edit_dropdown.visible = False
                self.edit_dropdown.update()
                self.edit_textfield.visible = False
                self.edit_textfield.update()
                self.edit_button.visible = False
                self.edit_button.update()

                await self.updates_account('events')
            
    container = Container()
    content = ft.Column(controls=[
        ft.Row(controls=[
            ft.Text(value='Аккаунт', size=30)
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(width=15),

        ft.Container(padding=15, content=ft.Column(controls=[
            # Фотография
            ft.ResponsiveRow([container.photo]),

            ft.ResponsiveRow([container.email]),

            ft.ResponsiveRow([container.first_name]),

            ft.ResponsiveRow([container.last_name]),

            ft.ResponsiveRow([container.phone_number]),

            ft.ResponsiveRow([container.date_register]),

            ft.ResponsiveRow([container.verify_email]),

            ft.ResponsiveRow([container.update_account, 
                container.edit_account, container.delete_account,
                container.verify_emails, container.back_index_page,
                container.back_login]),

            # Разделительная линия
            ft.Divider(color=ft.colors.DEEP_ORANGE_100),
            
            ft.ResponsiveRow([container.edit_dropdown]),
            ft.ResponsiveRow([container.edit_textfield]),
            ft.ResponsiveRow([container.edit_button]),
                     

        ]))
    ])
    return content