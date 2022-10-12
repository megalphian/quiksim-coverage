import time

class TimeTracker:

    def __init__(self):
        self.last_recorded_time = None
        self.start_time = None
    
    def start_timer(self):
        self.start_time = time.time()
        self.last_recorded_time = self.start_time

    def get_time_diff(self):
        self.last_recorded_time = time.time()
        time_diff = self.last_recorded_time - self.start_time
        return time_diff
    
    def print_timed_message(self, msg):
        time_diff = self.get_time_diff()
        msg = msg + '\n'
        msg += 'Elapsed time: ' + str(time_diff)
        print(msg)
        return time_diff