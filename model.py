class ScanResult:
    def __init__(self):
        self.data_integrity = None
        self.cropped_page = None
        self.table = None

class Box:
    def __init__(self):
        self.left = 40
        # With headers 175
        # Without headers 200
        self.top = 200
        self.right_crop = 360
        self.bottom_crop = 500

    def __str__(self):
        return f'Box(left={self.left}, top={self.top}, right_crop={self.right_crop}, bottom_crop={self.bottom_crop})'

class DataIntegrity:
    def __init__(self):
        self.top_found = False
        self.date_found = False
        self.bottom_found = False
        self.right_crop_found = False
        self.there_is_another_page = False