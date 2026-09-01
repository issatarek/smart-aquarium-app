import flet as ft
# Global physical constants for my specific aquarium
KNOWN_AQUARIUM_HEIGHT = 90.0  # Total tank height in cm
MIN_SAFE_HEIGHT = 50.0         # Minimum water level for fish survival in cm
TDS_MIN_MINERALS = 50.0      # Below this, water lacks essential dissolved minerals
TDS_IDEAL_UPPER = 300.0       # Standard clean, mineral-balanced aquarium water
TDS_WARNING_THRESHOLD = 500.0 # High dissolved solids; plan a water change soon

def evaluate_ph(val: float = 7):
    # Hardware error check
    if val < 0.0 or val > 14.0:
        return "Sensor Error", ft.Colors.GREY_800, ft.Colors.GREY_400
    if 6.5 <= val <= 7.5:
        return "Optimal", ft.Colors.GREEN_700, ft.Colors.GREEN_400
    elif 6.0 <= val < 6.5 or 7.5 < val <= 8.0:
        return "Warning", ft.Colors.AMBER_800, ft.Colors.AMBER_400
    else:
        return "Critical", ft.Colors.RED_700, ft.Colors.RED_400


def evaluate_tds(val: float = 200.0, min_val: float = 0.0, max_val: float = 1000.0):
    # 1. Negative Reading (Physical impossible / Sensor disconnection)
    if val < 0.0:
        return "Sensor Error", ft.Colors.GREY_800, ft.Colors.GREY_400

    # 2. Too Pure / Demineralized Water (Osmotic stress risk for fish)
    elif 0.0 <= val < TDS_MIN_MINERALS:
        return "Too Pure (Low Minerals)", ft.Colors.CYAN_800, ft.Colors.CYAN_400

    # 3. Optimal Mineral Balance (50 ppm - 300 ppm)
    elif TDS_MIN_MINERALS <= val <= TDS_IDEAL_UPPER:
        return "Optimal", ft.Colors.GREEN_700, ft.Colors.GREEN_400

    # 4. Elevated TDS / Accumulating Waste (300 ppm - 500 ppm)
    elif TDS_IDEAL_UPPER < val <= TDS_WARNING_THRESHOLD:
        return "Warning (High TDS)", ft.Colors.AMBER_800, ft.Colors.AMBER_400

    # 5. Heavy Contamination / Waste Accumulation (500 ppm - 1000 ppm)
    elif TDS_WARNING_THRESHOLD < val <= max_val:
        return "High Contamination", ft.Colors.RED_700, ft.Colors.RED_400

    # 6. Extreme Out-of-Range Reading (> 1000 ppm)
    else:
        return "Critical / Probe Error", ft.Colors.PURPLE_800, ft.Colors.PURPLE_400


def evaluate_water_level(val: float = 10.0, min_val: float = 0.0, max_val: float = 90.0):
    # 1. Physical Overflow Check (Water exceeds top rim safety limit)
    if val > (KNOWN_AQUARIUM_HEIGHT - 5.0):
        return "Overflow Risk", ft.Colors.PURPLE_800, ft.Colors.PURPLE_400

    # 2. Optimal Range (e.g., between 50 cm and 80 cm)
    elif MIN_SAFE_HEIGHT <= val <= (KNOWN_AQUARIUM_HEIGHT - 10.0):
        return "Optimal", ft.Colors.GREEN_700, ft.Colors.GREEN_400

    # 3. Low Water Warning (e.g., between 40 cm and 49.9 cm)
    elif (MIN_SAFE_HEIGHT - 10.0) <= val < MIN_SAFE_HEIGHT:
        return "Low", ft.Colors.AMBER_800, ft.Colors.AMBER_400

    # 4. Critical Low Level (Below 40 cm)
    elif 0.0 <= val < (MIN_SAFE_HEIGHT - 10.0):
        return "Critical Low", ft.Colors.RED_700, ft.Colors.RED_400

    # 5. Invalid / Negative Reading (Sensor Error)
    else:
        return "Sensor Error", ft.Colors.GREY_800, ft.Colors.GREY_400


def normalize_value(val: float, min_val: float, max_val: float) -> float:
    """Clamps only for UI progress bar calculation to prevent Flet render crashes."""
    clamped = max(min_val, min(val, max_val))
    return (clamped - min_val) / (max_val - min_val)
