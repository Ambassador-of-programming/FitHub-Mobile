import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

# Информация о зале
async def info_detail(page: ft.Page):
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


    content = ft.Column(
    controls=[
        ft.Row(alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(ft.Column([
                    ft.Row([
                        ft.Image(
                            src="assets/image/main.png",
                            width=100,
                            height=54,
                            fit=ft.ImageFit.COVER
                        ),
                        ft.Text(
                           value='проспект Науки, 9A Харків 61166',
                           color='#1C3E7D',
                           size=14,
                           font_family='Cutive Mono',
                           width=140,
                           height=40
                        ),
                        ft.Icon(name=ft.icons.FAVORITE)

                ], alignment=ft.MainAxisAlignment.CENTER), 
                ]),
            width=300,
            height=74,
            border_radius=10,
            padding=10,
            bgcolor='#FFFFFF',
            ),
        ]),
        ft.Row(
            controls=[
                ft.Container(ft.Column([
                    ft.Row([
                        ft.Text(
                           value='Години роботи:',
                           color='#1C3E7D',
                           size=16,
                           font_family='Cutive Mono',
                           width=133,
                           height=25
                        ),
                    ], alignment=ft.MainAxisAlignment.START), 

                    ft.Row([
                        ft.Text(
                           value='''ПНВТСРЧТПТСБНД''',
                           color='#1C3E7D',
                           size=16,
                           font_family='Cutive Mono',
                           width=25,
                           height=117
                        ),
                        ft.Text(
                           value='''07:00-19:00 07:00-19:00 07:00-19:00 07:00-19:00 07:00-19:00 07:00-19:00 07:00-19:00''',
                           color='#1C3E7D',
                           size=14,
                           font_family='Cutive Mono',
                           width=100,
                           height=117
                        ),
                    ], alignment=ft.MainAxisAlignment.START), 

                ]),
            width=300,
            height=170,
            border_radius=10,
            padding=10,
            bgcolor='#FFFFFF',
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.ElevatedButton(
                width=300,
                height=38,
                content=ft.Text(
                    value='Дзвоніть за номером +380983723576',
                    size=14,
                    font_family='Cutive Mono'
                ),
                color='#FFFFFF',
                bgcolor='#1C3E7D',
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)), 
                on_click=None
            )
            ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.ElevatedButton(
                width=300,
                height=38,
                content=ft.Text(
                    value='vladyslav.serhiienko@hneu.net ',
                    size=14,
                    font_family='Cutive Mono',
                ),
                color='#FFFFFF',
                bgcolor='#1C3E7D',
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)), 
                on_click=None
            )
        ], alignment=ft.MainAxisAlignment.CENTER),  
    ],
)
    return content