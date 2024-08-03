import flet as ft
import asyncio
import aiohttp
import aiofiles
import json

# main login
async def auth(page: ft.Page):
    content = ft.Stack(
    controls=[
        ft.Row([
            ft.Row(height=300),
            ft.Image(
            src=f"assets/image/main.png",
            width=306,
            height=165,
            fit=ft.ImageFit.COVER,
        ),], 
        alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Column(
            controls=[
                ft.Row(height=250),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="Вітаємо !",
                            color='#0A214A',
                            size=40,
                            width=176,
                            height=48,
                            font_family='Cutive Mono',
                            weight=400
                            # text_align=ft.TextAlign.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    value="Оберіть свої заняття та розвивайтесь\n разом з нами.",
                    color='#383C43',
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    width=306,
                    height=40,
                    font_family='Cutive Mono'
                ),

                ft.Row(height=45),
                ft.Row(
                    controls=[
                        ft.ElevatedButton( 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)), 
                            bgcolor='#1C3E7D',
                            color=ft.colors.WHITE,
                            width=300,
                            height=52,
                            content=ft.Text(
                                value="Зареєструватися", 
                                size=20,
                                font_family='Cutive Mono'),
                            on_click=lambda x: page.go('/register'),

                            ),
                            
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ), 
                            bgcolor='#939EB4',
                            color='#0A214A',
                            width=300,
                            height=52,
                            content=ft.Text(
                                value="Вхід", 
                                size=20,
                                font_family='Cutive Mono',
                            ),
                            on_click=lambda x: page.go('/login'),
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
    ],
)
    return content