import time

class StopWatch(object):

    def __init__(self):

        self.start_time = 0

    def start(self):
        """
        Record current time to start stopwatch timer
        """

        self.start_time = time.time()

    def stop(self):
        """
        Use start time to calculate elapsed time and print it out
        """

        run_time = time.time() - self.start_time
        print("")
        print("** Time to run: %s sec" % round(run_time, 2))