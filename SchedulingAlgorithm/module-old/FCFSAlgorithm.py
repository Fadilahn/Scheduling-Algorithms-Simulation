from SchedulingAlgorithms import SchedulingAlgorithms

# FCFS (First Come First Serve)
class FCFSAlgorithm(SchedulingAlgorithms):
    def __init__(self, processes):
        super().__init__(processes)

    def run(self):
        # kunci algoritma FCFS (First Come First Served)
        # sorting ready_queue berdasarkan waktu kedatangan atau arrive time.
        # ------------------------------------------------------
        # sudah dilakukan dalam constuctor Asheduling Algorithms
        # ------------------------------------------------------

        # looping selama proses masih belum semua dieksekusi
        while self.remaining_process:
            
            # set ready_queue dengan proses yang sudah siap berdasarkan waktu kedatangan
            self.setReadyQueues()

            # If the CPU is idle, dispatch the first process in the ready queue
            if not self.ready_queues:
                self.current_time += 1
                self.delay += 1
                continue

            # get prosses yang akan di running
            process = self.getRunningProcess()
 
            # Execute the process
            self.executeNonPreemptive(process)
    