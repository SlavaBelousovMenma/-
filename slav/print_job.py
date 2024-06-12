class PrintJob:
    def __init__(
        self,
        sheets,
        resolution,
        color=False,
        continuous_feed=False,
        specific_printer=None,
        specific_type=None,
    ):
        self.sheets = sheets
        self.resolution = resolution
        self.color = color
        self.continuous_feed = continuous_feed
        self.specific_printer = specific_printer
        self.specific_type = specific_type
        self.time_added = None