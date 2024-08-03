import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

# Информация
async def info(page: ft.Page):
    # page.appbar = ft.AppBar(
    #     title=ft.Text('Інформація',
    #         color='#FFFFFF',
    #         font_family='Cutive Mono',
    #         size=20,
    #     ),
    #     center_title=True,
    #     bgcolor='#1C3E7D',
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
            self.name = ft.Text(
                        value='Invalid Username',
                       color='#1C3E7D',
                       size=20,
                       font_family='Cutive Mono'
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

    async def exit_(event):
        page.appbar.visible = False
        page.appbar.update()
        
        page.bottom_appbar.visible = False
        page.bottom_appbar.update()
        
        page.go('/login')

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
            ft.ElevatedButton(
                width=300,
                height=38,
                content=ft.Text(
                    value='Інформація про зал',
                    size=16,
                    font_family='Cutive Mono'
                ),
                color='#0A214A',
                bgcolor='#FFFFFF',
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)), 
                on_click=lambda x: page.go('/info_detail')
            )
            ]),
        ft.Row([
            ft.ElevatedButton(
                width=300,
                height=38,
                content=ft.Text(
                    value='Вийти',
                    size=16,
                    font_family='Cutive Mono',
                ),
                color='#0A214A',
                bgcolor='#FFFFFF',
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)), 
                on_click=exit_
            )
        ]),  
    ],
)
    return content