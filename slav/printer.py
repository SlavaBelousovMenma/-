class Printer:
    def __init__(
        self, name, max_width, max_height, max_resolution, speed, tray_capacity
    ):
        self.name = name
        self.max_width = max_width
        self.max_height = max_height
        self.max_resolution = max_resolution
        self.speed = speed
        self.tray_capacity = tray_capacity
        self.current_job = None
        self.completed_jobs = []

    def can_print(self, job):
        return (
            job.sheets <= self.tray_capacity and job.resolution <= self.max_resolution
        )

    def start_printing(self, job):
        self.current_job = job

    def print_step(self):
        if self.current_job:
            sheets_to_print = min(self.speed, self.current_job.sheets)
            self.current_job.sheets -= sheets_to_print
            if self.current_job.sheets <= 0:
                self.completed_jobs.append(self.current_job)
                self.current_job = None
