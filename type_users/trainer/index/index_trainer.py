import flet as ft
import aiohttp
import aiofiles
import json

async def index_trainer(page: ft.Page):
    class DataTable:
        def __init__(self) -> None:
            self.table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("")),
                    ft.DataColumn(ft.Text("")),
                    ft.DataColumn(ft.Text("")),
                ],
                data_row_color='#FFFFFF',
            )

            self.all_battom = ft.Row(controls=[
                ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT, on_click=self.next_row),
                ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, on_click=self.prev_row),
                ft.IconButton(icon=ft.icons.UPDATE, on_click=self.update_bottom),
                ], alignment=ft.MainAxisAlignment.END)
            
            self.current_row = 0
            self.rows = []
        
        # async def click_detal_page(self, e):
        #     row = e.control  # получаем DataRow
        #     # print(row.cells[3].content.value)
        #     await tablelistview.create_row(row.cells[3].content.value)
        #     tablelistview.list.update()

        #     self.table.visible = False
        #     self.table.update()

        #     self.all_battom.visible = False
        #     self.all_battom.update()

        async def update_bottom(self, event):
            self.table.clean()
            self.rows.clear()
            
            await self.fill_data()
            self.table.update()

        async def prev_row(self, e):
            if self.current_row + 5 < len(self.rows):
                self.current_row += 5
                await self.update_table()
            self.table.update()

        async def next_row(self, e):
            if self.current_row - 5 >= 0:
                # есть данные для предыдущей страницы  
                self.current_row -= 5
                await self.update_table()
            self.table.update()

        async def update_table(self):
            # берем 2 записи из списка по текущему индексу
            rows_to_show = self.rows[self.current_row:self.current_row + 5]
            # устанавливаем их в таблицу 
            self.table.rows = rows_to_show

        async def fill_data(self):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)
        
            url = 'http://nexus-hub.pro/trainer/trainer/check_all_lesson_phone'
            payload = {
                "phone_number": f"{email}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
            
            if data['message'] == True:
                colonka = data['data']

                for colon in colonka:
                    # if colon[6] == None:
                    row = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(
                            value=f'{colon[0]}/{colon[2]}', 
                            size=10,
                            font_family='Cutive Mono',
                            color='#0A214A',
                            no_wrap=False, width=52, selectable=True
                        )),

                        ft.DataCell(ft.Text(
                            value=f'{colon[3]}/{colon[4]}',
                            size=10,
                            font_family='Cutive Mono',
                            color='#383C43',
                            no_wrap=False, width=52, selectable=True
                        )),

                        ft.DataCell(ft.Text(
                            value=f'{colon[5]}/{colon[6]}',
                            size=10,
                            font_family='Cutive Mono',
                            color='#383C43',
                            no_wrap=False, width=52, selectable=True
                        )),
            
                    ])
                    self.rows.append(row)
                await self.update_table()

    class Container:
        def __init__(self):
            self.update_stats = ft.ElevatedButton(text='Обновить статистику', on_click=self.update_stat)

            self.create_lessons = ft.ElevatedButton(text='Создать занятие', col=6, on_click=self.button_create_lessons)
            self.delete_lessons = ft.ElevatedButton(text='Удалить занятие', col=6, on_click=self.button_delete_lessons)

            self.container_create_lessons = ft.Container(padding=15, visible=False)

        async def button_delete_lessons(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)

            url = 'http://nexus-hub.pro/trainer/trainer/delete_lessons'
            payload = {
                "email": email,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
        
        async def button_create_lessons(self, event):
            async def save_create_lessons(event):
                if all([lesson_type.value, lesson_time.value, 
                        lesson_date.value, desc_lesson.value]):
                    async with aiofiles.open('login/email.json', mode='r') as file:
                        data = await file.read()
                        email =  json.loads(data).get("email", None)

                    url = 'http://nexus-hub.pro/trainer/trainer/add_lessons'
                    payload = {
                      "phone_number": email,
                      "lesson_type": lesson_type.value,
                      "lesson_time": lesson_time.value,
                      "lesson_date": lesson_date.value,
                      "lesson_duration": desc_lesson.value,
                    }

                    async with aiohttp.ClientSession() as session:
                        async with session.post(url, json=payload) as response:
                            data = await response.json()
                    
                    # обновляем таблицу
                    await datatable.update_bottom('update')

                    # отключаем видимость таблицы
                    self.container_create_lessons.visible = False
                    self.container_create_lessons.update()
                else:
                    print('не все заполнено')

            lesson_type = ft.TextField(hint_text='Тип занятий')
            lesson_time = ft.TextField(hint_text='Время занятий')
            lesson_date = ft.TextField(hint_text='Дата занятий')
            desc_lesson = ft.TextField(hint_text='Описание занятий')

            button_create_less = ft.ElevatedButton(text='Создать', on_click=save_create_lessons)
            self.container_create_lessons.visible = True
            self.container_create_lessons.content = ft.Column(controls=[
                ft.ResponsiveRow([lesson_type]),
                ft.ResponsiveRow([lesson_time]),
                ft.ResponsiveRow([lesson_date]),
                ft.ResponsiveRow([desc_lesson]),
                ft.ResponsiveRow([button_create_less])
            ])
            self.container_create_lessons.update()

        async def update_stat(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)
            url = 'http://nexus-hub.pro/trainer/trainer/get_lessons'
            payload = {
                "email": email,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                    
            if data['message'] == True:
                # обновить тип занятий
                self.stat_lesson_type.value = f"Тип занятий: {data['data'][0][2]}"
                self.stat_lesson_type.update()

                # обновить время занятий
                self.stat_lesson_time.value = f"Время занятий: {data['data'][0][3]}"
                self.stat_lesson_time.update()

                # обновить локацию
                self.stat_location.value = f"Локация: {data['data'][0][4]}"
                self.stat_location.update()

                # обновить телефон
                self.stat_phone.value = f"Телефон: {data['data'][0][5]}"
                self.stat_phone.update()

                # обновить дату занятия
                self.stat_lesson_date.value = f"Дата занятий: {data['data'][0][6]}"
                self.stat_lesson_date.update()

                # обновить забронировали
                self.stat_user_bron.value = f"Пользователи забронировали: {data['data'][0][7]}"
                self.stat_user_bron.update()

                # обновить подтвердили бронь
                self.stat_user_verify_bron.value = f"Пользователи подтвердили бронь: {data['data'][0][8]}"
                self.stat_user_verify_bron.update()
            else:
                # вернуть тип занятий в none
                self.stat_lesson_type.value = f"Тип занятий: None"
                self.stat_lesson_type.update()

                # вернуть время занятий в none
                self.stat_lesson_time.value = f"Время занятий: None"
                self.stat_lesson_time.update()

                # вернуть локацию в none
                self.stat_location.value = f"Локация: None"
                self.stat_location.update()

                # вернуть телефон в none
                self.stat_phone.value = f"Телефон: None"
                self.stat_phone.update()

                # вернуть дату занятия в none
                self.stat_lesson_date.value = f"Дата занятий: None"
                self.stat_lesson_date.update()

                # вернуть забронировали в none
                self.stat_user_bron.value = f"Пользователи забронировали: None"
                self.stat_user_bron.update()

                # вернуть подтвердили бронь в none
                self.stat_user_verify_bron.value = f"Пользователи подтвердили бронь: None"
                self.stat_user_verify_bron.update()    
    datatable = DataTable()
    await datatable.fill_data()

    container = Container()
    content = ft.Column(controls=[
        ft.Row(controls=[
            ft.Text(value='Тренер', size=30)
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(width=15),

        ft.Container(padding=15, content=ft.Column(controls=[
            datatable.table,
            datatable.all_battom,

            # Кнопка обновления статистики
            # ft.ResponsiveRow([container.update_stats]),

            # Кнопка создания занятия
            ft.ResponsiveRow([container.create_lessons]),
            # ft.ResponsiveRow([container.delete_lessons]),

            # Разделительная линия
            ft.Divider(color=ft.colors.DEEP_ORANGE_100),

            # Форма создание занятия
            ft.ResponsiveRow([container.container_create_lessons]),

        ]))
    ])
    return content