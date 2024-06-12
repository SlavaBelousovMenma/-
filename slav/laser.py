from printer import Printer


class LaserPrinter(Printer):
    def __init__(
        self,
        name,
        max_width,
        max_height,
        max_resolution,
        speed,
        tray_capacity,
        infinite_tray=False,
    ):
        super().__init__(
            name, max_width, max_height, max_resolution, speed, tray_capacity
        )
        self.infinite_tray = infinite_tray

    def can_print(self, job):
        return super().can_print(job) or self.infinite_tray
