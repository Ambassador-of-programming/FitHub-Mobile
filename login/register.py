import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json

# Регистрация
async def register(page: ft.Page):
    class Registers:
        def __init__(self):
            self.fio = ft.TextField(
                            label='фио',
                            width=300,
                            height=56,
                            bgcolor='#FFFFFF',
                            color='#939EB4',
                            prefix_icon=ft.icons.ACCOUNT_BOX,
                            border_color='#F6F6F6'           
                        )
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
            self.button = ft.ElevatedButton( 
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
                            on_click=self.reg
                        )

        async def reg(self, event):
            if all([self.fio.value, self.password.value, self.number.value]):
                    url = 'http://nexus-hub.pro/auth/signup'
                    payload = {
                      "phone_number": self.number.value,
                      "password": self.password.value,
                      "fio": self.fio.value,
                      "type_user": 'user'
                    }
                    async with aiohttp.ClientSession() as session:
                        async with session.post(url, json=payload) as response:
                            await response.json()


                    page.go('/login')
            else:
                    self.error_text.visible = True
                    self.error_text.value = 'Пожалуйста, заполните все поля'
                    self.error_text.update()
                    await asyncio.sleep(5)
                    self.error_text.visible = False
                    self.error_text.update()

    reg = Registers()
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
                            value="Реєстрація",
                            color='#0A214A',
                            size=32,
                            width=168,
                            height=40,
                            font_family='Cutive Mono',
                            weight=400
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
   
                ft.Row(height=5),          

                ft.Row(
                    controls=[
                        reg.fio
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    controls=[
                        reg.number
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    controls=[
                        reg.password
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                ft.Row(height=5),
                ft.Row(controls=[
                    reg.error_text
                ]),
                

                ft.Row(
                    controls=[
                        reg.button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            value='Вже маєте акаунт? ',
                            weight=178,
                            height=24,
                            color='#939EB4',
                            font_family='Cutive Mono',
                            size=13,
                            ),

                        ft.TextButton(
                            content=ft.Text(
                                value="Увійти", 
                                weight=178,
                                height=24,
                                color='#1C3E7D',
                                font_family='Cutive Mono',
                                size=13,
                                ),
                            on_click=lambda x: page.go('/login'),
                            
                        ) 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
    ],
)
    return content