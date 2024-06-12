class PrintQueueManager:
    def __init__(self):
        self.printers = []
        self.queue = []
        self.time = 0

    def get_queue(self):
        return self.queue

    def add_printer(self, printer):
        self.printers.append(printer)

    def remove_printer(self, name):
        self.printers = [p for p in self.printers if p.name != name]

    def add_job(self, job):
        job.time_added = self.time
        self.queue.append(job)

    def remove_job(self, job):
        self.queue.remove(job)

    def find_printer(self, job):
        for printer in self.printers:
            if job.specific_printer and printer.name == job.specific_printer:
                return printer
            elif job.specific_type and isinstance(printer, job.specific_type):
                return printer
            elif printer.can_print(job):
                return printer
        return None

    def process_queue(self):
        self.time += 1
        new_queue = self.queue.copy()
        for job in self.queue:
            printer = self.find_printer(job)
            if printer and printer.current_job is None:
                printer.start_printing(job)
                new_queue.remove(job)
        self.queue = new_queue
        for printer in self.printers:
            printer.print_step()
            
    def report_text(self):
        return self.printers, self.queue, self.time