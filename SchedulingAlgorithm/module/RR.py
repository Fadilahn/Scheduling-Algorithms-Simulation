from ProcessState import ProcessState
from SchedulingAlgorithms import SchedulingAlgorithms

# RR (Round Robin)
class RR(SchedulingAlgorithms):
    quantum = 0

    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum

    # execute program untuk round robin
    def execute(self, process):

        # If the process has finished, terminate it
        if process.getBurstTimeRemaining() <= self.quantum:

            self.gantt_chart.append([process.getName(), 
                                    process.getBurstTimeRemaining()]) # masukan informasi untuk membuat gantt chart
            self.current_time += process.getBurstTimeRemaining()

            # karena proses selesai maka nilai fitur yang ada di proses akan dis set
            self.setCompletedProcess(process)

        # If the process is still running, put it back in the ready queue
        elif process.getState() == ProcessState.RUNNING:

            # jika proses saat ini tidak akan selesai pada self.quantum saat ini
            process.setBurstTimeRemaining(process.getBurstTimeRemaining() - self.quantum)
            self.gantt_chart.append([process.getName(), 
                                    self.quantum]) # masukan informasi untuk membuat gantt chart
            # Execute the process
            self.current_time += self.quantum

            # mengecek apakah semua program sudah dijalankan
            if self.remaining_process != 0:
                self.setReadyQueues()

            process.setState(ProcessState.READY)
            self.ready_queues.append(process)

    def run(self):
        # set ready_queue dengan proses yang sudah siap berdasarkan waktu kedatangan
        self.setReadyQueues()

        # looping selama proses masih belum semua dieksekusi
        while self.remaining_process:

            # If the CPU is idle, dispatch the first process in the ready queue
            if not self.ready_queues:
                # set ready_queue dengan proses yang sudah siap berdasarkan waktu kedatangan
                self.setReadyQueues()

                if not self.ready_queues:
                    self.current_time += 1
                    self.delay += 1
                    continue
            
            # get prosses yang akan di running
            process = self.getRunningProcess()

            # Execute the process
            # karena ini merupakan algoritma preemptive, jadi memanggil method execute preemptive
            self.execute(process)