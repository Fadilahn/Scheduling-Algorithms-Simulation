from ProcessState import ProcessState

# SchedulingAlgorithms
class SchedulingAlgorithms:
    processes = []
    ready_queues = []
    remaining_process = 0
    completed_processes = []
    current_time = 0
    n = 0
    run_time = 0
    temp_process = None
    gantt_chart = []
    delay = 0

    def __init__(self, processes):
        self.processes = processes
        self.ready_queues = []
        self.completed_processes = []
        self.current_time = 0
        self.n = len(processes)
        self.remaining_process = self.n
        self.run_time = 0
        self.temp_process = None
        self.gantt_chart = []
        self.delay = 0

        # Sorting proses berdasarkan waktu kedatangan
        self.processes.sort(key=lambda x: x.getArriveTime())

    # setter
    def addProcesses(self, process):
        # cek apakah process merupakan list atau bukan
        if isinstance(process, list):
            for p in process:
                self.processes.append(p)
        elif isinstance(process, object):
            self.processes.append(process)

    # getter
    def getN(self):
        return self.n

    def getProcesses(self):
        return self.processes

    def getCompletedProcesses(self):
        if not self.completed_processes:
            return self.processes
        else:
            return self.completed_processes
    
    def getCurrentTime(self):
        return self.current_time

    def getGanttChart(self):
        return self.gantt_chart
    
    # fungsi untuk kelas yang mengimplementasi
    # ========================================================

    # check proses baru untuk dimasukan ke ready queue
    def setReadyQueues(self):
        # Add new processes to the ready queue
        for process in self.processes:
            # jika proses lebih dari current time
            if process.getArriveTime() > self.current_time:
                break

            # jika proses sesuai kondisi
            if not process.getIsQueued() and not process.getIsCompleted() and process.getArriveTime() <= self.current_time:
                # maka proses akan dimasukan ke ready queue dengan status state ready
                process.setState(ProcessState.READY)
                process.setIsQueued(True)
                self.ready_queues.append(process)
            
    # fungsi untuk mendapatakan proses yang running
    def getRunningProcess(self):
        # cek apakah proses didalam queue berstatus READY
        if self.ready_queues[0].getState() == ProcessState.READY:
            # proses pertama yang ada di ready queue
            process = self.ready_queues.pop(0)
            process.setState(ProcessState.RUNNING)

            # cek jika start time belum diisi 
            if process.getStartTime() is None:
                process.setStartTime(self.current_time)

            return process
        
        return None
    
    # set atribut untuk proses yang selesai dieksekusi
    def setCompletedProcess(self, process):

        # Hitung finish time berdasarkan current time
        process.setFinishTime(self.current_time)

        # Hitung turnaround time proses
        process.setTurnaroundTime()

        # Hitung waiting time proses
        process.setWaitingTime()

        # hitung response time
        process.setResponseTime()

        # Set proses menjadi selesai
        process.setState(ProcessState.EXIT)
        process.setIsCompleted(True)
        process.setIsQueued(False)

        #tambahkan proses yang telah dieksekusi ke list
        self.completed_processes.append(process)
        self.processes.remove(process)

        self.remaining_process -= 1

    # check delay
    def checkDelay(self):
        # check nilai delay jika ada
        if self.delay:
            # delay dimasukan untuk gantt chart
            self.gantt_chart.append(['##', self.delay]) 
            self.delay = 0

    # eksekusi proses untuk algoritma non-preemptive
    def executeNonPreemptive(self, process):
        # check delay
        self.checkDelay()

        # Execute the process
        # karena algoritma non-preemtive jadi proses running langsung diselesaikan
        self.current_time += process.getBurstTime() 
        process.setBurstTimeRemaining(0) 

        # If the process has finished, terminate it
        if process.getBurstTimeRemaining() == 0:
            self.gantt_chart.append([process.getName(),
                                    process.getBurstTime()])
            self.setCompletedProcess(process)

    # eksekusi proses untuk algoritma preemptive
    def executePreemptive(self, process):
        # check delay
        self.checkDelay()

        # check apakah temp proses bukan merupakan proses saat ini
        if process != self.temp_process:
            if self.temp_process and not self.temp_process.getIsCompleted():
                self.gantt_chart.append([self.temp_process.getName(), 
                                            self.run_time]) # masukan informasi untuk membuat gantt chart
                self.run_time = 0
            self.temp_process = process
        self.run_time += 1

        # Execute the process
        # karena algoritma preemptive jadi waktu bertambah 1
        self.current_time += 1
        process.setBurstTimeRemaining(process.getBurstTimeRemaining() - 1)

        # If the process has finished, terminate it
        if process.getBurstTimeRemaining() == 0:
            # masukan informasi untk membuat gantt chart
            self.gantt_chart.append([process.getName(),
                                    self.run_time])
            self.temp_process = process
            self.run_time = 0

            # karena proses selesai maka nilai fitur yang ada di proses akan dis set
            self.setCompletedProcess(process)

        # If the process is still running, put it back in the ready queue
        elif process.getState() == ProcessState.RUNNING:
            process.setState(ProcessState.READY)
            self.ready_queues.append(process)
