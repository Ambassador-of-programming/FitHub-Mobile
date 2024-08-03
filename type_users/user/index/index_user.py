# import flet as ft
# import aiohttp
# import aiofiles
# import json
# import asyncio

# async def index_user(page: ft.Page):
#     class DataTable:
#         def __init__(self) -> None:
#             self.table = ft.DataTable(
#                 vertical_lines=ft.border.BorderSide(1, "blue"),
#                 horizontal_lines=ft.border.BorderSide(1, "green"),
#                 heading_row_color=ft.colors.BLACK12,
#                 columns=[
#                     ft.DataColumn(ft.Text("№")),
#                     ft.DataColumn(ft.Text("Тип занятий")),
#                     ft.DataColumn(ft.Text("Тренер")),
#                 ],
#             )
#             self.all_battom = ft.Row(controls=[
#                 ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT, on_click=self.next_row),
#                 ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, on_click=self.prev_row),
#                 ft.IconButton(icon=ft.icons.UPDATE, on_click=self.update_bottom),
#                 ], alignment=ft.MainAxisAlignment.END)
            
#             self.current_row = 0
#             self.rows = []
        
#         async def update_bottom(self, event):
#             self.table.clean()
#             self.rows.clear()
            
#             await self.fill_data()
#             self.table.update()

#         async def prev_row(self, e):
#             if self.current_row + 5 < len(self.rows):
#                 self.current_row += 5
#                 await self.update_table()
#             self.table.update()

#         async def next_row(self, e):
#             if self.current_row - 5 >= 0:
#                 # есть данные для предыдущей страницы  
#                 self.current_row -= 5
#                 await self.update_table()
#             self.table.update()

#         async def click_detal_page(self, e):
#             row = e.control  # получаем DataRow

#             await tablelistview.create_row(row.cells[2].content.value)
#             tablelistview.list.update()

#             self.table.visible = False
#             self.table.update()

#             self.all_battom.visible = False
#             self.all_battom.update()

#         async def update_table(self):
#             # берем 2 записи из списка по текущему индексу
#             rows_to_show = self.rows[self.current_row:self.current_row + 5]
#             # устанавливаем их в таблицу 
#             self.table.rows = rows_to_show
        
#         async def fill_data(self):
#             async with aiofiles.open('login/email.json', mode='r') as file:
#                 data = await file.read()
#                 email =  json.loads(data).get("email", None)
#             url = 'http://127.0.0.1/user/user/get_lesson'
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url) as response:
#                     data = await response.json()

#             if data['message'] == True:
#                 colonka = data['data']

#                 for batch in colonka:
#                     row = ft.DataRow(cells=[
#                         ft.DataCell(ft.Text(value=batch[0])),
#                         ft.DataCell(ft.Text(value=batch[2])),
#                         ft.DataCell(ft.Text(value=batch[1])),

#                     ], on_select_changed=self.click_detal_page)
#                     self.rows.append(row)
#                 await self.update_table()
    
#     class TableListView:
#         def __init__(self, table: DataTable) -> None:
#             self.table = table
#             self.error_texts = ft.Text(color=ft.colors.RED_ACCENT)
#             self.list = ft.ListView(adaptive=True, visible=False)
#             self.new_table = []
#             self.new_rows = []
#             self.rows = ft.DataRow()
#             self.trainer_email = ''
#             self.verify_bronirovanie = ft.Checkbox(label='Подтвердить бронирование')
#             self.bronirovanie = ft.ElevatedButton(text='Забронировать', on_click=self.button_bronirovanie)
#             self.back = ft.ElevatedButton(text="Назад", icon=ft.icons.ARROW_LEFT_OUTLINED, on_click=self.back_click)
        
#         async def button_bronirovanie(self, event):
#             if all([self.verify_bronirovanie.value]):
#                 async with aiofiles.open('login/email.json', mode='r') as file:
#                     data = await file.read()
#                     email =  json.loads(data).get("email", None)

#                 url = 'http://127.0.0.1/user/user/connect_lesson'
#                 payload = {
#                   "user_email": email,
#                   "trainer_email": self.trainer_email,
#                 }
#                 async with aiohttp.ClientSession() as session:
#                     async with session.post(url, json=payload) as response:
#                         data = await response.json()
            
#             else:
#                 self.error_texts.visible = True
#                 self.error_texts.value = 'Вы должны подтвердить бронирование'
#                 self.error_texts.update()

#                 await asyncio.sleep(2)

#                 self.error_texts.value = ''
#                 self.error_texts.update()


#         async def create_row(self, email):
#             self.new_table.clear()
#             self.new_rows.clear()
#             self.list.visible = True

#             url = 'http://127.0.0.1/trainer/trainer/get_lessons'
#             payload = {
#                 "email": email,
#             }
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(url, json=payload) as response:
#                     data = await response.json()
            
#             # print(email)

#             if data['message'] == True:
#                 # db = Password_Database()
#                 get_all_data_by_id = data['data']
                
#                 for numeric, value in enumerate(get_all_data_by_id[0]):
#                     if numeric == 0:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('ID'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))
                    
#                     if numeric == 1:
#                         self.trainer_email = value
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('Тренер'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))

#                     if numeric == 2:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('тип занятий'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))

#                     if numeric == 3:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('время занятий'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))

                    
#                     if numeric == 4:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('адрес'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))

                    
#                     if numeric == 5:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('Телефон'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))
                    
#                     if numeric == 6:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('дата занятий'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))
                    
#                     if numeric == 7:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('Забронировали'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))
                    
#                     if numeric == 8:
#                         self.new_table.append(
#                             ft.DataTable(
#                             vertical_lines=ft.border.BorderSide(1, "blue"),
#                             horizontal_lines=ft.border.BorderSide(1, "green"),
#                             heading_row_color=ft.colors.BLACK12,
#                             columns=[ft.DataColumn(ft.Text('Подтвердили бронь'))]))
                        
#                         self.new_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value, selectable=True))]))
                    

#                 for index, v in enumerate(self.new_table):
#                     self.new_table[index].rows.append(self.new_rows[index])

#                 self.new_table.append(self.verify_bronirovanie)
#                 self.new_table.append(self.error_texts)
#                 self.new_table.append(self.bronirovanie)
#                 self.new_table.append(ft.Divider(height=15, color=ft.colors.AMBER_ACCENT_200))
#                 self.new_table.append(self.back)

#                 self.list.controls = self.new_table

#         async def back_click(self, event):
#             self.list.visible = False
#             self.list.update()
            
#             self.table.table.visible = True
#             self.table.table.update()
            
#             self.table.all_battom.visible = True
#             self.table.all_battom.update()
    
#     datatable = DataTable()
#     await datatable.fill_data()

#     tablelistview = TableListView(datatable)

#     content = ft.Column(controls=[
#         ft.ResponsiveRow(controls=[
#             ft.Text(value='Пользователь', size=30)
#         ], 
#         run_spacing=0,

#         alignment=ft.MainAxisAlignment.CENTER,
        
#         ),

#         ft.ResponsiveRow(controls=[
#             tablelistview.list,
#             datatable.table
#         ]),
#         # ft.ResponsiveRow(controls=[
#         #     datatable.table
#         # ]),

#         datatable.all_battom,
#     ])

#     return content

import flet as ft 
import asyncio
import aiohttp
import aiofiles
import json


# index меню (главное меню)
async def index_user(page: ft.Page):
    class DataTable:
        def __init__(self) -> None:
            self.table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("")),
                    ft.DataColumn(ft.Text("")),
                    ft.DataColumn(ft.Text("")),
                ],
                data_row_color='#FFFFFF'
            )

            self.all_battom = ft.Row(controls=[
                ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT, on_click=self.next_row),
                ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, on_click=self.prev_row),
                ft.IconButton(icon=ft.icons.UPDATE, on_click=self.update_bottom),
                ], alignment=ft.MainAxisAlignment.END)
            
            self.current_row = 0
            self.rows = []
        
        async def click_detal_page(self, e):
            row = e.control  # получаем DataRow
            # print(row.cells[3].content.value)
            await tablelistview.create_row(row.cells[3].content.value)
            tablelistview.list.update()

            self.table.visible = False
            self.table.update()

            self.all_battom.visible = False
            self.all_battom.update()

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
        
            url = 'http://nexus-hub.pro/user/user/get_lesson'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
            
            if data['message'] == True:
                colonka = data['data']

                for colon in colonka:
                    if colon[6] == None:
                        row = ft.DataRow(cells=[
                            ft.DataCell(ft.Text(
                                value=colon[3], 
                                size=16,
                                font_family='Cutive Mono',
                                color='#0A214A'
                            )),

                            ft.DataCell(ft.Text(
                                value=colon[2],
                                size=16,
                                font_family='Cutive Mono',
                                color='#0A214A'
                                )),

                            ft.DataCell(ft.Text(
                                value=colon[1],
                                size=14,
                                font_family='Cutive Mono',
                                color='#383C43'
                            )),
                            ft.DataCell(ft.Text(
                                value=colon[0],
                                size=14,
                                font_family='Cutive Mono',
                                color='#383C43'
                            )),

                        ], on_select_changed=self.click_detal_page)
                        self.rows.append(row)
                await self.update_table()
    
    class TableListView:
        def __init__(self, table: DataTable) -> None:
            self.table = table
            self.list = ft.Column(adaptive=True, visible=False)
            self.new_table = []
            self.trainer_phone = ''

            self.alert = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Ви впевнені, що хочете забронювати заняття?", 
                        color='#000000',
                        font_family='Cutive Mono',
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    actions=[
                        ft.Row([
                            ft.ElevatedButton(
                                text="Забронировать",
                                bgcolor='#1C3E7D',
                                width=120,
                                height=40,
                                on_click=self.alert_click
                            ),
                            ft.ElevatedButton(
                                text="Назад",
                                bgcolor='#1C3E7D',
                                height=40,
                                on_click=self.close_dlg
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    bgcolor='#FFFFFF'
                    )
            
        async def close_dlg(self, e):
            self.alert.open = False
            page.update()
            
            self.list.visible = False
            self.list.update()
            
            datatable.table.visible = True
            datatable.table.update()

            datatable.all_battom.visible = True
            datatable.all_battom.update()

            self.new_table.clear()
            self.list.controls.clear()

        async def finish_brony(self, event):
            async with aiofiles.open('login/email.json', mode='r') as file:
                data = await file.read()
                email =  json.loads(data).get("email", None)
            url = 'http://nexus-hub.pro/user/user/connect_lesson'
            payload = {
              "user_phone": f"{email}",
              "lesson_id": f"{self.trainer_phone}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
            await self.close_dlg(1)

            await datatable.update_bottom(0)

            self.list.visible = False
            self.list.update()
            
            datatable.table.visible = True
            datatable.table.update()

            datatable.all_battom.visible = True
            datatable.all_battom.update()


        async def alert_click(self, event):
            self.alert.title = ft.Text("Вітаємо з успішним бронюванням!", 
                    color='#000000',
                    font_family='Cutive Mono',
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                )
            self.alert.actions = [
                ft.Row([
                    ft.ElevatedButton(
                        text="Завершити",
                        bgcolor='#1C3E7D',
                        on_click=self.finish_brony,
                    )
                    ], alignment=ft.MainAxisAlignment.CENTER),
            ]
            self.alert.update()

        async def open_dlg(self, event):
            dlg = self.alert
            page.dialog = dlg
            dlg.open = True
            page.update()
        
        async def create_row(self, id_lesson: str):
            url = 'http://nexus-hub.pro/trainer/trainer/get_lessons'
            payload = {
                "phone_number": f"{id_lesson}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()

            # дата занятий
            self.new_table.append(
                ft.Row([
                   ft.Text(
                       value=data['data'][0][5],
                       color='#939EB4',
                       size=13
                    )
               ], alignment=ft.MainAxisAlignment.CENTER))
            
            # тип занятий 
            self.new_table.append(
                ft.Row([
                   ft.Text(
                       value=data['data'][0][2],
                       color='#0A214A',
                       size=32
                    )
                ], alignment=ft.MainAxisAlignment.CENTER))
            
            # время занятий 
            self.new_table.append(
                ft.Row([
                   ft.Text(
                        value=data['data'][0][3],
                        color='#939EB4',
                        size=16,
                        font_family='Cutive Mono'
                    )
                ], alignment=ft.MainAxisAlignment.CENTER))
            self.trainer_phone = f"{data['data'][0][0]}"

            # тренер информация
            self.new_table.append(
                ft.Container(
                    content=ft.Column(controls=[
                        ft.Text(
                            value='Тренер',
                            color='#383C43',
                            size=15,
                            font_family='Cutive Mono'

                        ),
                        ft.Row([
                            ft.CircleAvatar(
                            foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                            ),
                            ft.Text(
                               value=data['data'][0][1],
                               color='#383C43',
                               size=15,
                               font_family='Cutive Mono'
                            ),
                        ]),  
                    ],
                    ),
                    width=320,
                    height=87,
                    border_radius=10,
                    padding=10,
                    bgcolor='#FFFFFF'   
                ))
            
            self.new_table.append(
                ft.Container(
            content=ft.Column(controls=[
                ft.Text(
                    value='Детальніше',
                    color='#383C43',
                    size=15,
                    font_family='Cutive Mono'

                ),
                ft.Row([
                    ft.Text(
                       value=data['data'][0][4],
                       color='#383C43',
                       size=14,
                       font_family='Cutive Mono',
                       width=320,
                       max_lines=3
                    ),
                ]),  
            ],
            ),
            width=320,
            height=87,
            border_radius=10,
            padding=10,
            bgcolor='#FFFFFF'   
        ),
            )
            self.new_table.append(
                ft.Row(height=50),

            )
            self.new_table.append(
                
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
                                    value="Забронировать", 
                                    size=20,
                                    font_family='Cutive Mono'),
                                on_click=self.open_dlg
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
            )
            self.list.visible = True
            self.list.controls = self.new_table
            
            # content = ft.Column(
            # controls=[
            #     ft.Container(
            #         content=ft.Column(controls=[

            #             ft.Row([
            #                 ft.CircleAvatar(
            #                 foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
            #                 ),
            #                 ft.Text(
            #                    value='Izzy W',
            #                    color='#383C43',
            #                    size=15,
            #                    font_family='Cutive Mono'
            #                 ),
            #             ]),  
            #         ],
            #         ),
            #         width=320,
            #         height=87,
            #         border_radius=10,
            #         padding=10,
            #         bgcolor='#FFFFFF'   
            #     ),

            #     ft.Container(
            #         content=ft.Column(controls=[
            #             ft.Text(
            #                 value='Детальніше',
            #                 color='#383C43',
            #                 size=15,
            #                 font_family='Cutive Mono'

            #             ),
            #             ft.Row([
            #                 ft.Text(
            #                    value='Тренер у спортивному клубі - це фахівець, який керує тренуваннями та розвитком спортсменів. Він не лише навчає техніці, а й мотивує, виховує дисципліну та допомагає досягти високих результатів. Тренер важлива ланка в спортивному житті, допомагаючи своїм підопічним розвивати фізичні та психологічні якості.',
            #                    color='#383C43',
            #                    size=14,
            #                    font_family='Cutive Mono',
            #                    width=320,
            #                    max_lines=3
            #                 ),
            #             ]),  
            #         ],
            #         ),
            #         width=320,
            #         height=87,
            #         border_radius=10,
            #         padding=10,
            #         bgcolor='#FFFFFF'   
            #     ),
            #     ft.Row(height=50),
            #     ft.Row(
            #         controls=[
            #             ft.ElevatedButton( 
            #                 style=ft.ButtonStyle(
            #                     shape=ft.RoundedRectangleBorder(radius=10)), 
            #                 bgcolor='#1C3E7D',
            #                 color=ft.colors.WHITE,
            #                 width=300,
            #                 height=52,
            #                 content=ft.Text(
            #                     value="Забронировать", 
            #                     size=20,
            #                     font_family='Cutive Mono'),
            #                 on_click=self.open_dlg
            #             )
            #         ],
            #         alignment=ft.MainAxisAlignment.CENTER,
            #     ),
            # ],
        # )

    datatable = DataTable()
    await datatable.fill_data()

    tablelistview = TableListView(datatable)


    content = ft.Column(
    controls=[
        ft.ResponsiveRow(controls=[
            tablelistview.list,
            datatable.table,
            ]),
        ft.ResponsiveRow(controls=[
            datatable.all_battom
        ]),
    ],
)
    return content