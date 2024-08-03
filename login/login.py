import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

# Авторизация
async def login(page: ft.Page):
    class LoginUser:
        def __init__(self) -> None:
            self.number = ft.TextField(
                            label='+(380)_________',
                            width=300,
                            height=56,
                            bgcolor='#FFFFFF',
                            color='#939EB4',
                            prefix_icon=ft.icons.PHONE,
                            border_color='#F6F6F6'           
                        )
            self.password = ft.TextField(
                                label='Пароль',
                                width=300,
                                height=56,
                                bgcolor='#FFFFFF',
                                color='#939EB4',
                                prefix_icon=ft.icons.LOCK_OUTLINED,
                                border_color='#F6F6F6',
                                can_reveal_password=True,
                                password=True,
                        )
            self.error_text = ft.Text(visible=False, color=ft.colors.RED)
            self.login_button = ft.ElevatedButton( 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)), 
                            bgcolor='#1C3E7D',
                            color=ft.colors.WHITE,
                            width=300,
                            height=52,
                            content=ft.Text(
                                value="Вхід", 
                                size=20,
                                font_family='Cutive Mono'),
                            on_click = self.check_user
                        )

        async def check_user(self, event):
                        # если пользователь ввел все данные для входа
                if all([self.number.value, self.password.value]):
                    url = 'http://nexus-hub.pro/auth/signin'
                    payload = {
                        "phone_number": self.number.value,
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
                                data_to_save = {"email": self.number.value}
                                async with aiofiles.open('login/email.json', mode='w') as file:
                                    await file.write(json.dumps(data_to_save, indent=4))

                                # async def theme_changed(event):
                                #         page.theme_mode = (
                                #             ft.ThemeMode.DARK
                                #             if page.theme_mode == ft.ThemeMode.LIGHT
                                #             else ft.ThemeMode.LIGHT
                                #         )
                                #         page.update()

                                if data['user_type'] == 'trainer':
                                    # page.appbar = ft.AppBar(
                                    #     leading = ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, 
                                    #         on_click=lambda x: page.go('/account')),
                                    #     actions=[
                                    #         ft.Switch(on_change=theme_changed)
                                    #     ],
                                    #     toolbar_height=40
                                    # )

                                    page.bgcolor = ft.colors.BLACK
                                    page.go('/index_trainer')
                                
                                if data['user_type'] == 'admin':
                                    # async def theme_changed(event):
                                    #     page.theme_mode = (
                                    #         ft.ThemeMode.DARK
                                    #         if page.theme_mode == ft.ThemeMode.LIGHT
                                    #         else ft.ThemeMode.LIGHT
                                    #     )
                                    #     page.update()

                                    # page.appbar = ft.AppBar(
                                    #     leading = ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, 
                                    #         on_click=lambda x: page.go('/account')),
                                    #     actions=[
                                    #         ft.Switch(on_change=theme_changed)
                                    #     ],
                                    #     toolbar_height=40
                                    # )
                                    
                                    page.bgcolor = ft.colors.BLACK
                                    page.go('/index_admin')
                                    
                                if data['user_type'] == 'user':
                                    page.bgcolor = '#F6F6F6'

                                    page.appbar = ft.AppBar(
                                        title=ft.Text('Забронювати',
                                            color='#FFFFFF',
                                            font_family='Cutive Mono',
                                            size=20,
                                        ),
                                        center_title=True,
                                        bgcolor='#1C3E7D'
                                    )

                                    # переход в раздел информация
                                    async def info_go(event):
                                        page.appbar = ft.AppBar(
                                            title=ft.Text('Інформація',
                                                color='#FFFFFF',
                                                font_family='Cutive Mono',
                                                size=20,
                                            ),
                                            center_title=True,
                                            bgcolor='#1C3E7D',
                                        )
                                        page.go('/info')

                                    async def save_profile(event):
                                        async with aiofiles.open('login/email.json', mode='r') as file:
                                            data = await file.read()
                                            email =  json.loads(data).get("email", None)
                                            fio =  json.loads(data).get("fio", None)
                                            number =  json.loads(data).get("number", None)

                                        if number != None:
                                            url = 'http://nexus-hub.pro/user/user/edit_account'
                                            payload = {
                                                "phone": f"{email}",
                                                "parametr": "phone_number",
                                                "parametr_value": f"{number}"
                                            }
                                            async with aiohttp.ClientSession() as session:
                                                async with session.post(url, json=payload) as response:
                                                    data = await response.json()

                                        if fio != None:
                                            url = 'http://nexus-hub.pro/user/user/edit_account'
                                            payload = {
                                                "phone": f"{number}",
                                                "parametr": "fio",
                                                "parametr_value": f"{fio}"
                                            }
                                            async with aiohttp.ClientSession() as session:
                                                async with session.post(url, json=payload) as response:
                                                    data = await response.json()

                                    async def edit_profile(event):
                                        page.appbar = ft.AppBar(
                                            title=ft.Text('Редагувати профіль',
                                                color='#FFFFFF',
                                                font_family='Cutive Mono',
                                                size=20,
                                            ),
                                            center_title=True,
                                            bgcolor='#1C3E7D',
                                            actions=[
                                                ft.IconButton(
                                                    icon=ft.icons.SAVE,
                                                    on_click=save_profile
                                                )
                                            ],
                                            leading=ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT,
                                            on_click=profile_go)
                                        )
                                        page.go('/edit_profile')

                                    # переход в профиль
                                    async def profile_go(event):
                                        page.appbar = ft.AppBar(
                                        title=ft.Text('Профіль',
                                            color='#FFFFFF',
                                            font_family='Cutive Mono',
                                            size=20,
                                        ),
                                        center_title=True,
                                        bgcolor='#1C3E7D',
                                        actions=[
                                            ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                on_click=edit_profile,
                                            )
                                        ]
                                    )   
                                        page.update()
                                        page.go('/profile_user')
                                        page.update()

                                    # переход на главное меню
                                    async def index_go(event):
                                        page.appbar = ft.AppBar(
                                            title=ft.Text('Забронювати',
                                                color='#FFFFFF',
                                                font_family='Cutive Mono',
                                                size=20,
                                            ),
                                            center_title=True,
                                            bgcolor='#1C3E7D'
                                            )

                                        page.go('/index_user')

                                    page.bottom_appbar = ft.BottomAppBar(
                                        content=ft.Row(
                                            controls=[
                                                ft.Container(expand=True),
                                                ft.IconButton(icon=ft.icons.HOME, on_click=index_go),
                                                ft.Container(expand=True),
                                                ft.IconButton(icon=ft.icons.ACCOUNT_BOX, on_click=profile_go),
                                                ft.Container(expand=True),
                                                ft.IconButton(icon=ft.icons.INFO, on_click=info_go),
                                                ft.Container(expand=True),
                                            ]
                                        ),
                                        # height=65,
                                        bgcolor='#FFFFFF'
                                    )

                                    #     destinations=[
                                    #         ft.NavigationDestination(
                                    #             icon=ft.icons.HOME,
                                    #             on_click=clickadsf

                                    #         ),
                                    #         ft.NavigationDestination(
                                    #             icon=ft.icons.ACCOUNT_BOX,
                                    #             selected_icon=clickadsf

                                    #         ),
                                    #         ft.NavigationDestination(
                                    #             icon=ft.icons.INFO,
                                    #             selected_icon=clickadsf

                                    #         ),
                                    #     ],
                                    #     bgcolor='#FFFFFF',
                                    #     shadow_color=''
                                    # )

                                    page.go(f"/index_{data['user_type']}")
    enter = LoginUser()
    content = ft.Stack(
    controls=[
        ft.Row([
            ft.Row(height=150),
            ft.Image(
            src=f"assets/image/main.png",
            width=230,
            height=123,
            fit=ft.ImageFit.COVER,
        ),], 
        alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Column(
            controls=[
                ft.Row(height=140),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="Вхід",
                            color='#0A214A',
                            size=32,
                            width=65,
                            height=40,
                            font_family='Cutive Mono',
                            weight=400
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
   
                ft.Row(height=5),          

                # заполнение номера телефона
                ft.Row(
                    controls=[
                        enter.number
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                # заполнение пароля
                ft.Row(
                    controls=[
                        enter.password
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                ft.Row(height=5),

                # ошибка текст
                ft.Row(controls=[
                    enter.error_text
                ],
                alignment=ft.MainAxisAlignment.CENTER),

                # кнопка входа
                ft.Row(
                    controls=[
                        enter.login_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    controls=[
                        ft.Text(
                            value='Ще немає акаунту?',
                            weight=178,
                            height=24,
                            color='#939EB4',
                            font_family='Cutive Mono',
                            size=13,
                            ),
                            
                        ft.TextButton(
                            content=ft.Text(
                                value="Зареєструватися", 
                                weight=178,
                                height=24,
                                color='#1C3E7D',
                                font_family='Cutive Mono',
                                size=13,
                                ),
                            on_click=lambda x: page.go('/register'),
                            
                        ) 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
    ],
)
    return content
