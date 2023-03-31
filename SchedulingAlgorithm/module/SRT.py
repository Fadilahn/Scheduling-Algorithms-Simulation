from SchedulingAlgorithms import SchedulingAlgorithms

# SRT (Shortest Remaining Time)
class SRT(SchedulingAlgorithms):
    def __init__(self, processes):
        super().__init__(processes)

    def run(self):
        # looping selama proses masih belum semua dieksekusi
        while self.remaining_process:
            
            # set ready_queue dengan proses yang sudah siap berdasarkan waktu kedatangan
            self.setReadyQueues()

            # If the CPU is idle, dispatch the first process in the ready queue
            if not self.ready_queues:
                self.current_time += 1
                self.delay += 1
                continue

            # kunci algoritma SRT (Shortest Remaining Time)
            # sorting ready_queue berdasarkan waktu sisa waktu proses atau remaining rime.
            # ------------------------------------------------------
            self.ready_queues.sort(key=lambda x: x.getBurstTimeRemaining()) 
            # ------------------------------------------------------
            
            # get prosses yang akan di running
            process = self.getRunningProcess()

            # Execute the process
            # karena ini merupakan algoritma preemptive, jadi memanggil method execute preemptive
            self.executePreemptive(process)