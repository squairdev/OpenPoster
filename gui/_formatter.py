class Format():
    def __init__(self):
        pass

    def formatFloat(self, value, decimal_places=2):
        try:
            float_val = float(value)
            return f"{float_val:.{decimal_places}f}"
        except (ValueError, TypeError):
            return value

    def formatPoint(self, point_str, decimal_places=2):
        try:
            parts = point_str.split()
            formatted_parts = [self.formatFloat(part, decimal_places) for part in parts]
            return " ".join(formatted_parts)
        except:
            return point_str