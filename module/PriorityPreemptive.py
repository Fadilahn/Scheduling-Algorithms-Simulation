from SchedulingAlgorithms import SchedulingAlgorithms

# Priority (Preemptive)
class PriorityPreemptive(SchedulingAlgorithms):
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

            # kunci algoritma Priority
            # sorting ready_queue berdasarkan Priority.
            # ------------------------------------------------------
            self.ready_queues.sort(key=lambda x: (x.getPriority(), x.getArriveTime()))
            # ------------------------------------------------------
            
            # get prosses yang akan di running
            process = self.getRunningProcess()

            # Execute the process
            # karena ini merupakan algoritma preemptive, jadi memanggil method execute preemptive
            self.executePreemptive(process)