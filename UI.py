import flet as ft
import cards as cd

def main(page: ft.Page):
    page.title = "Smart Aquarium System (Offline)"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # Top bar assembly
    header_title = ft.Text("🏠 Home Aquarium Dashboard", size=22, weight=ft.FontWeight.BOLD)
    header_status = ft.Container(
        content=ft.Text("Status: Active", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.GREEN_800,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=6,
    )
    
    top_bar = ft.Container(
        content=ft.Row(controls=[header_title, header_status],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=10,
        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=8
    )

    # Fetch constructed cards from cards module
    sensor_cards = cd.create_all_sensor_cards()

    # Panel assembly
    dashboard_frame = ft.Container(
        content=ft.Row(controls=sensor_cards, spacing=15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        expand=True,
        padding=10
    )

    # Master structure
    master = ft.Column(controls=[top_bar, dashboard_frame], expand=True, spacing=20)
    page.add(master)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER,
        host="192.168.43.13",  # Accessible to other devices on  local Wi-Fi network(From my hot spot)
        port=60868)
    'IPv4 Address. . . . . . . . . . . : 192.168.43.13'
    'http://192.168.43.13:60868'
