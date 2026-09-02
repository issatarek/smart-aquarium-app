import os
from urllib.parse import parse_qs, urlparse
import flet as ft
import cards as cd

def main(page: ft.Page):
    page.title = "Smart Aquarium System "
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

    # Route change event listener (The Web Listener)
    def handle_route_change(e: ft.RouteChangeEvent):
        # Parse incoming web parameters (e.g., /?ph=8.2&height=65.0&tds=280)
        parsed_url = urlparse(page.route)
        query_params = parse_qs(parsed_url.query)

        if query_params:
          cd.update_all_cards_from_query(query_params)
          page.update()

  # Bind listener and process initial route on connection
    page.on_route_change = handle_route_change
    page.go(page.route)


if __name__ == "__main__":
    # Detect if running in a cloud container (e.g., Render) vs local network
    IS_CLOUD = "PORT" in os.environ
    port = int(os.environ.get("PORT", 60868))

    ft.app(
      target=main,
      view= None if IS_CLOUD else ft.AppView.WEB_BROWSER,
      host="0.0.0.0" if IS_CLOUD else "192.168.43.13",
      port=port,
  )

    'IPv4 Address. . . . . . . . . . . : 192.168.43.13'
    'http://192.168.43.13:60868'
