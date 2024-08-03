import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json


# Редактировать профиль
async def edit_profile(page: ft.Page):
    # page.appbar = ft.AppBar(
    #     title=ft.Text('Редагувати профіль',
    #         color='#FFFFFF',
    #         font_family='Cutive Mono',
    #         size=20,
    #     ),
    #     center_title=True,
    #     bgcolor='#1C3E7D',
    #     actions=[
    #         ft.IconButton(
    #             icon=ft.icons.SAVE,
    #             on_click=None
    #         )
    #     ],
    #     leading=ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT,
    #     on_click=None)
    # )

    class EditProfile:
        def __init__(self):
            self.edit = ft.Column([
                    ft.TextField(
                       label='ФІО',
                       prefix_icon=ft.icons.POWER_OFF_OUTLINED,
                       on_change=self.save_json_fio
                    ),
                    ft.TextField(
                        label='+(380)_________',
                        prefix_icon=ft.icons.PHONE,
                        on_change=self.save_json_number
                    ),
                ]),
        async def save_json_fio(self, event):
            fio = event.control.value
            with open('login/email.json', 'r') as f:
                data = json.load(f)

            # Сохраняем существующее значение email
            email = data.get("email", "")

            # Обновляем или добавляем запись "fio"
            data["fio"] = fio

            # Восстанавливаем существующее значение email
            data["email"] = email

            with open('login/email.json', 'w') as f:
                json.dump(data, f, indent=4)

        async def save_json_number(self, event):
            number = event.control.value
            with open('login/email.json', 'r') as f:
                data = json.load(f)

            # Сохраняем существующее значение email
            email = data.get("email", "")

            # Обновляем или добавляем запись "fio"
            data["number"] = number

            # Восстанавливаем существующее значение email
            data["email"] = email

            with open('login/email.json', 'w') as f:
                json.dump(data, f, indent=4)

    editprofile = EditProfile()
    content = ft.Column(
    controls=[
        ft.Row([
           ft.Text(
                value='Контактна інформація',
                color='#0A214A',
                size=20,
                font_family='Cutive Mono'
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        editprofile.edit[0]
    ],
)
    return content