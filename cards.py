import flet as ft
import logic as lg

# Dictionary storing component control references for state manipulation
CARD_REFS = {}

# DATA CONFIGURATIONS
PH_CONFIGS = {
    "id": "ph",
    "title": "pH Balance",
    "raw_value": 7.0,
    "unit": "pH",
    "min_val": 0.0,
    "max_val": 14.0,
    "evaluator": lg.evaluate_ph,
}

HEIGHT_CONFIGS = {
    "id": "height",
    "title": "Water Level",
    "raw_value": 70.0,
    "unit": "cm",
    "min_val": 0.0,
    "max_val": 90.0,
    "evaluator": lg.evaluate_water_level,
}

TDS_CONFIGS = {
    "id": "tds",
    "title": "TDS (Water Quality)",
    "raw_value": 450.0,
    "unit": "ppm",
    "min_val": 0.0,
    "max_val": 1000.0,
    "evaluator": lg.evaluate_tds,
}


def create_status_badge(status_label: str, status_color: str):
    section_status = ft.Text(
        status_label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE
    )
    badge_container = ft.Container(
        content=section_status,
        bgcolor=status_color,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        border_radius=6,
    )
    return badge_container, section_status


def create_single_card(config: dict):
    # Evaluate Domain Rules & Calculate Progress (The Bridge) 
    raw_val = config["raw_value"]
    status_label, status_color, progress_color = config["evaluator"](raw_val)
    progress_fraction = lg.normalize_value(raw_val, config["min_val"], config["max_val"])

    # Individual Controls (Your Original Modular Style)
    section_title = ft.Text(config["title"], size=18, weight=ft.FontWeight.BOLD)
    section_value = ft.Text(f"{raw_val} {config['unit']}", size=18, weight=ft.FontWeight.BOLD)
    badge_status, section_status = create_status_badge(status_label, status_color)    
    bar_progress = ft.ProgressBar(value=progress_fraction, color=progress_color, height=8)

    #Row Layouts & Assembly (Unchanged)
    level_layout = ft.Row(
        controls=[ft.Text("Level:", size=14, color=ft.Colors.GREY_400), section_value],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    status_layout = ft.Row(
        controls=[ft.Text("Status:", size=14, color=ft.Colors.GREY_400), badge_status],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    main_card_controls = [section_title,level_layout,status_layout,ft.Container(height=5),bar_progress,]

    card_container = ft.Container(
        content=ft.Column(controls=main_card_controls, spacing=10),
        expand=True, padding=15,
        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    # Store UI references for runtime state updates
    CARD_REFS[config["id"]] = {
        "value": section_value,
        "status_text": section_status,
        "status_badge": badge_status,
        "progress": bar_progress,
    }
    return card_container


def create_all_sensor_cards():
    """Generates a list of constructed card containers from configs."""
    cards_list = []
    for config in [PH_CONFIGS, HEIGHT_CONFIGS,TDS_CONFIGS]:
        card = create_single_card(config)
        cards_list.append(card)
    return cards_list
