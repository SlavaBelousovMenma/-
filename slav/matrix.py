from printer import Printer


class MatrixPrinter(Printer):
    def can_print(self, job):
        return super().can_print(job) and job.continuous_feed
