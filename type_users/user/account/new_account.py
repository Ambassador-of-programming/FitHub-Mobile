import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

# Профиль
async def profile(page: ft.Page):
    # page.appbar = ft.AppBar(
    #     title=ft.Text('Профіль',
    #         color='#FFFFFF',
    #         font_family='Cutive Mono',
    #         size=20,
    #     ),
    #     center_title=True,
    #     bgcolor='#1C3E7D',
    #     actions=[
    #         ft.IconButton(
    #             icon=ft.icons.EDIT,
    #             on_click=None
    #         )
    #     ]
    # )
    # page.navigation_bar = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationDestination(
    #             icon=ft.icons.HOME,
    #         ),
    #         ft.NavigationDestination(
    #             icon=ft.icons.ACCOUNT_BOX
    #         ),
    #         ft.NavigationDestination(
    #             icon=ft.icons.INFO,
    #         ),
    #     ],
    #     bgcolor='#FFFFFF',
    #     shadow_color=''
    # )

    class User_info:
        def __init__(self) -> None:
            self.none = ft.Text(
                value='Зараз в розкладі нічого немає',
                color='#383C43',
                size=15,
                font_family='Cutive Mono',
                visible=False
            )
            self.name = ft.Text(
                        value='Invalid Username',
                       color='#383C43',
                       size=15,
                       font_family='Cutive Mono',
                    )
            self.time = ft.Text(
                       value='07:00',
                       color='#383C43',
                       size=15,
                       font_family='Cutive Mono',
                       text_align=ft.alignment.center,
                       visible=True
                    )
            self.lesson_type = ft.Text(
                       value='Type Lesson',
                       color='#383C43',
                       size=15,
                       font_family='Cutive Mono',
                       text_align=ft.CrossAxisAlignment.CENTER,
                       visible=True

                    )
            self.trainer = ft.Text(
                       value='Izzy W\n30 хв',
                       color='#383C43',
                       size=15,
                       font_family='Cutive Mono',
                       text_align=ft.CrossAxisAlignment.END,
                       visible=True
                    )
            self.update = ft.IconButton(
                icon=ft.icons.UPDATE,
                on_click=self.user_info
                
            )
        async def user_info(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)

            url = 'http://nexus-hub.pro/user/user/get_account'
            payload = {
                "phone": f"{email}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                    if data.get("user"):
                        self.name.value = data['user'][0][3]
                        self.name.update()

            url = 'http://nexus-hub.pro/user/user/check_lesson'
            payload = {
                "phone": f"{email}",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                    if data.get("data"):
                        self.none.visible = False
                        self.none.update()

                        self.time.visible = True
                        self.time.value = data['data'][-1][3]
                        self.time.update()

                        self.lesson_type.visible = True
                        self.lesson_type.value = data['data'][-1][2]
                        self.lesson_type.update()

                        self.trainer.visible = True
                        self.trainer.value = data['data'][-1][1]
                        self.trainer.update()

    user_info = User_info()
    content = ft.Column(
    controls=[
        ft.Row(alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(ft.Column([
                    ft.Row([
                    ft.Image(
                        src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                        border_radius=3000,
                        width=100,
                        height=100
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER), 

                ft.Row([
                    user_info.name,
                    user_info.update,
                ], alignment=ft.MainAxisAlignment.CENTER),
                ]),
            width=300,
            height=152,
            border_radius=10,
            padding=10,
            bgcolor='#FFFFFF',
            ),
        ]),

        ft.Row([
           ft.Text(
                value='Розклад',
                color='#0A214A',
                size=20,
                font_family='Cutive Mono'
            )
       ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Container(
            content=ft.Column(controls=[
                ft.Text(
                    value='Майбутні',
                    color='#383C43',
                    size=15,
                    font_family='Cutive Mono'
                ),
                ft.Row([
                    user_info.time,
                    user_info.lesson_type,
                    user_info.trainer,
                    user_info.none,
                ]),
            ],
            ),
            width=320,
            height=87,
            border_radius=10,
            padding=10,
            bgcolor='#FFFFFF'   
        ),
        
    ],
)
    return content
