import flet as ft
from navigation.FletRouter import Router
from navigation.bar import Appbar

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = 'HIDDEN'
    page.padding = 10
    page.platform = ft.PagePlatform.ANDROID
    page.window_width = 360
    page.window_height = 640
    page.adaptive = True
    page.fonts = {
        "Cutive Mono": "https://github.com/vernnobile/CutiveFont/blob/master/CutiveMono/in-progress/src/Cutive-Mono-Regular-unhinted.ttf"
    }

    myRouter = Router()
    await myRouter.init(page)

    page.bgcolor = '#F6F6F6'
    page.on_route_change = myRouter.route_change
    page.add(
        myRouter.body
    )
    page.go('/auth')

if __name__ == "__main__":
    ft.app(main)