import flet as ft
import aiohttp
import asyncio

async def index_admin(page: ft.Page):
    class Container:
        def __init__(self):
            self.error_text = ft.Text(color=ft.colors.RED_ACCENT,visible=False)
            self.stat_all_users = ft.Text(value='Общее количество пользователей: None')
            self.stat_users = ft.Text(value='Всего юзеров: None')
            self.stat_trainers = ft.Text(value='Всего тренеров: None')
            self.stat_lessons = ft.Text(value='Всего активных занятий: None')
            self.update_stats = ft.ElevatedButton(text='Обновить статистику', on_click=self.update_stat)
            self.delete_users_textfield = ft.TextField(hint_text='Email address')
            self.number_trainer = ft.TextField(hint_text='Номер тренера', visible=False)
            self.pass_trainer = ft.TextField(hint_text='пароль тренера', visible=False)
            self.fio_trainer = ft.TextField(hint_text='ФИО тренера', visible=False)
            self.button_trainer = ft.ElevatedButton(text='Зарегистрировать', on_click=self.reg_trainer, visible=False)
            self.add_trainer = ft.ElevatedButton(text='Добавить тренера', on_click=self.add_trainers, )

            self.delete_users_button = ft.ElevatedButton(text='Удалить пользователя', on_click=self.delete_users_buttons) 
            self.delete_lessons_button = ft.ElevatedButton(text='Удалить занятие', on_click=self.delete_lessons_buttons)
            self.delete_user_verify = ft.ElevatedButton(text='Удалить')
            self.containers = ft.Container(padding=15, content=ft.Column(controls=[
                ft.ResponsiveRow([self.stat_users]),
                ft.ResponsiveRow([self.stat_trainers])
            ]))

        async def reg_trainer(self, event):
            url = 'http://nexus-hub.pro/auth/signup'
            payload = {
              "phone_number": f'{self.number_trainer.value}',
              "password": f'{self.pass_trainer.value}',
              "fio": f'{self.fio_trainer.value}',
              "type_user": 'trainer'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    await response.json()
            
            self.number_trainer.visible = False
            self.number_trainer.update()
            self.pass_trainer.visible = False
            self.pass_trainer.update()
            self.fio_trainer.visible = False
            self.fio_trainer.update()
            self.button_trainer.visible = False
            self.button_trainer.update()

            await self.update_stat('update')
            
        async def add_trainers(self, event):
            self.number_trainer.visible = True
            self.number_trainer.update()
            self.pass_trainer.visible = True
            self.pass_trainer.update()
            self.fio_trainer.visible = True
            self.fio_trainer.update()
            self.button_trainer.visible = True
            self.button_trainer.update()
        
        async def delete_users_buttons(self, event):
            if all([self.delete_users_textfield.value]):
                url = 'http://nexus-hub.pro/admin/admin/delete_user'
                payload = {
                  "email": self.delete_users_textfield.value.strip(),
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        data = await response.json()
            else:
                self.error_text.visible = True
                self.error_text.value = 'Введите email'
                self.error_text.update()
                await asyncio.sleep(2)
        
        async def delete_lessons_buttons(self, event):
            if all([self.delete_lessons.value]):
                url = 'http://nexus-hub.pro/trainer/trainer/delete_lessons'
                payload = {
                  "email": self.delete_lessons.value.strip(),
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        data = await response.json()
            else:
                self.error_text.visible = True
                self.error_text.value = 'Введите email'
                self.error_text.update()
                await asyncio.sleep(2)

                self.error_text.visible = False
                self.error_text.update()

        async def update_stat(self, event):
            # Получаем Общее количество пользователей
            url_2 = 'http://nexus-hub.pro/admin/admin/get_all_users'
            async with aiohttp.ClientSession() as session:
                async with session.get(url_2) as response:
                    all_users = await response.json()

            # Полаем пользователей с типом user
            url_3 = 'http://nexus-hub.pro/admin/admin/get_all_type_user'
            async with aiohttp.ClientSession() as session:
                async with session.get(url_3) as response:
                    type_user = await response.json()
            
            # Полаем пользователей с типом trainer
            url_4 = 'http://nexus-hub.pro/admin/admin/get_all_type_trainer'
            async with aiohttp.ClientSession() as session:
                async with session.get(url_4) as response:
                    type_trainer = await response.json()

            # Получаем все активные занятия
            url = 'http://nexus-hub.pro/admin/admin/get_all_lessons'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    lessons = await response.json()

            self.stat_all_users.value = f"Общее количество пользователей: {len(all_users['data'])}"
            self.stat_all_users.update()

            self.stat_users.value = f"Всего юзеров: {len(type_user['data'])}"
            self.stat_users.update()

            self.stat_trainers.value = f"Всего тренеров: {len(type_trainer['data'])}"
            self.stat_trainers.update()
            
            self.stat_lessons.value = f"Всего активных занятий: {lessons['data']}"
            self.stat_lessons.update()

    container = Container()
    content = ft.Column(controls=[
        ft.Row(controls=[
            ft.Text(value='Администрация', size=30)
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(width=15),

        ft.Container(padding=15, content=ft.Column(controls=[
            # Общее количество пользователей
            ft.ResponsiveRow([container.stat_all_users]),

            # Получаем всех пользователей с типом User
            ft.ResponsiveRow([container.stat_users]),

            # Получаем всех пользователей с типом Trainer
            ft.ResponsiveRow([container.stat_trainers]),

            # Получаем все активные занятия
            ft.ResponsiveRow([container.stat_lessons]),

            # Кнопка обновления статистики
            ft.ResponsiveRow([container.update_stats]),
            
            # Кнопка создания тренера
            ft.ResponsiveRow([container.add_trainer]),
            
            # # Кнопка удаления пользователя по емайл
            # ft.ResponsiveRow([container.delete_users_button]),

            # # Кнопка удаления занятия по емайл тренера
            # ft.ResponsiveRow([container.delete_lessons_button]),

            # Разделительная линия
            ft.Divider(color=ft.colors.DEEP_ORANGE_100),
            ft.ResponsiveRow(controls=[
                container.number_trainer,
                container.pass_trainer,
                container.fio_trainer,
                container.button_trainer,
            ])
            # # Удаление пользотеля по email
            # ft.Row([ft.Text('Удаления пользователя по email')], alignment=ft.MainAxisAlignment.CENTER),
            # ft.ResponsiveRow([container.delete_users_textfield]),
            # ft.ResponsiveRow([container.delete_users_button]),

            # ft.ResponsiveRow([container.delete_lessons ]),
            # ft.ResponsiveRow([container.delete_lessons_button]),
        ]))

    ])
    return content