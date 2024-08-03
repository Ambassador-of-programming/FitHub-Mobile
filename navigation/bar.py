import flet as ft

class Appbar:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.appbar = ft.AppBar(
            leading = ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, disabled=True, 
                on_click=lambda x: page.go('/account')),
            actions=[
                ft.Switch(on_change=self.theme_changed)
            ],
            toolbar_height=40
        )

    async def theme_changed(self, event):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.page.update()

    async def content(self) -> ft.AppBar:
        return self.appbar