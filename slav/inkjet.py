from printer import Printer


class InkjetPrinter(Printer):
    def __init__(
        self,
        name,
        max_width,
        max_height,
        max_resolution,
        speed,
        tray_capacity,
        color_support,
    ):
        super().__init__(
            name, max_width, max_height, max_resolution, speed, tray_capacity
        )
        self.color_support = color_support

    def can_print(self, job):
        return super().can_print(job) and (not job.color or self.color_support)
