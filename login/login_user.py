import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

async def login_user(page: ft.Page):
    class Auth:
        def __init__(self):
            self.error_text = ft.Text(color=ft.colors.RED, visible=False)
            self.email = ft.TextField(hint_text='Электронная почта', bgcolor=ft.colors.PRIMARY_CONTAINER)
            self.password = ft.TextField(hint_text='Пароль', password=True, bgcolor=ft.colors.PRIMARY_CONTAINER)
            self.enter = ft.ElevatedButton(text='Войти', bgcolor=ft.colors.GREEN, on_click=self.enter_button)
            self.checkbox_choice = ft.Checkbox(label="Входить автоматически", col=6)
            self.access_restoration = ft.TextButton(text='Забыли пароль?', col=6, on_click=self.asscess_rest)
        
        async def asscess_rest(self, event):
            dlg = ft.AlertDialog(
                title=ft.Text(value='Если вы забыли пароль. То больше не забывайте пароль. Его нельзя восстановить :)'),
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
        
        async def enter_button(self, event):
            # если пользователь ввел все данные для входа
            if all([self.email.value, self.password.value]):
                url = 'http://nexus-hub.pro/auth/signin'
                payload = {
                    "email": self.email.value,
                    "password": self.password.value
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        data = await response.json()
                        if data.get('detail'):
                            self.error_text.visible = True
                            self.error_text.value = 'Не верные данные'
                            self.error_text.update()            

                            await asyncio.sleep(5)
                            self.error_text.visible = False
                            self.error_text.update()

                        elif data['message'] == False:
                            self.error_text.visible = True
                            self.error_text.value = 'Не верные данные'
                            self.error_text.update()            

                            await asyncio.sleep(5)
                            self.error_text.visible = False
                            self.error_text.update()
                        
                        elif data['message'] == True:
                            data_to_save = {"email": self.email.value}
                            async with aiofiles.open('login/email.json', mode='w') as file:
                                await file.write(json.dumps(data_to_save, indent=4))

                            class Appbar:
                                def __init__(self, page: ft.Page) -> None:
                                    self.page = page
                                    self.appbar = ft.AppBar(
                                        leading = ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, on_click=lambda e: page.go(f"/account_{data['user_type']}")),
                                        actions=[
                                            ft.Switch(on_change=self.theme_changed)
                                        ],
                                        toolbar_height=40
                                    )
                        
                                async def theme_changed(self, event):
                                    self.page.theme_mode = (
                                        ft.ThemeMode.DARK
                                        if self.page.theme_mode == ft.ThemeMode.LIGHT
                                        else ft.ThemeMode.LIGHT
                                    )
                                    self.page.update()
                        
                                async def content(self) -> ft.AppBar:
                                    return self.appbar
                        
                            appbar = Appbar(page)
                            page.appbar = await appbar.content()
                            page.go(f"/index_{data['user_type']}")

            # если пользователь
            else:
                self.error_text.visible = True
                self.error_text.value = 'Пожалуйста, заполните все поля'
                self.error_text.update()            

                await asyncio.sleep(5)
                self.error_text.visible = False
                self.error_text.update()
                

    class Register:
        def __init__(self):
            self.error_text = ft.Text(color=ft.colors.RED, visible=False)
            self.email = ft.TextField(hint_text='Email', bgcolor=ft.colors.BLACK)
            self.password = ft.TextField(hint_text='Password', password=True, bgcolor=ft.colors.BLACK)
            self.first_name = ft.TextField(hint_text='First Name', bgcolor=ft.colors.BLACK)
            self.last_name = ft.TextField(hint_text='Last Name', bgcolor=ft.colors.BLACK)
            self.phone_number = ft.TextField(hint_text='Phone Number', bgcolor=ft.colors.BLACK)

            self.choice_type_user = ft.RadioGroup(content=ft.Column(controls=[
                ft.Radio(value='trainer', label='Trainer', fill_color=ft.colors.BLACK),
                ft.Radio(value='user', label='Client', fill_color=ft.colors.BLACK),
                ]))
            self.button_register = ft.ElevatedButton(text='Зарегистрироваться', on_click=self.check_register_button)
            self.container = ft.Container(padding=10, bgcolor=ft.colors.BROWN_800, visible=False)

            self.reg_choice_button = ft.ElevatedButton(text='Регистрация', on_click=self.content)
        
        async def content(self, event) -> ft.Container:
            self.reg_choice_button.visible = False
            self.reg_choice_button.update()

            self.container.visible = True
            self.container.update()

            self.container.visible = True
            self.container.content = ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text(value='Регистрация', size=30, color=ft.colors.BLACK)
                    
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(width=15),
                ft.ResponsiveRow(controls=[
                    self.email
                ]),
                ft.ResponsiveRow(controls=[
                    self.password
                ]),
                ft.ResponsiveRow(controls=[
                    self.first_name
                ]),
                ft.ResponsiveRow(controls=[
                    self.last_name
                ]),
                ft.ResponsiveRow(controls=[
                    self.choice_type_user
                ]),
                ft.ResponsiveRow(controls=[
                    self.error_text
                ]),
                ft.ResponsiveRow(controls=[
                    self.button_register
                ]),
            ])
            self.container.update()

        async def check_register_button(self, event):
            if all([self.email.value, self.password.value, self.first_name.value, \
                    self.last_name.value, self.choice_type_user.value]):
                url = 'http://nexus-hub.pro/auth/signup'
                payload = {
                  "email": self.email.value,
                  "password": self.password.value,
                  "first_name": self.first_name.value,
                  "last_name": self.last_name.value,
                  "phone_number": self.phone_number.value,
                  "type_user": self.choice_type_user.value
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        await response.json()

                self.container.visible = False
                self.container.update()

                self.reg_choice_button.visible = True
                self.reg_choice_button.update()
            else:
                self.error_text.visible = True
                self.error_text.value = 'Пожалуйста, заполните все поля'
                self.error_text.update()
                await asyncio.sleep(5)
                self.error_text.visible = False
                self.error_text.update()

    register = Register()
    auth = Auth()

    content = ft.Column(controls=[
        ft.Row(controls=[
            ft.Text(value='Вход', size=30)
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(width=15),

        # Авторизация
        ft.ResponsiveRow(controls=[
            auth.email,
            auth.password,
            auth.error_text,
            auth.enter,
            auth.checkbox_choice,
            auth.access_restoration,
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(width=10),
        ft.Divider(height=3),

        # Кнопка регистрации
        ft.ResponsiveRow(controls=[
            register.reg_choice_button,
            ]),

        # Форма регистрации
        register.container

    ])
    return content