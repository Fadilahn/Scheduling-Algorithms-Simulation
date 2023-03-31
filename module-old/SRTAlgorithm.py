from SchedulingAlgorithms import SchedulingAlgorithms

# SRT (Shortes Job First)
class SRTAlgorithm(SchedulingAlgorithms):
    tempProcess = None
    tempTime = None
    ganttChartInfo = []

    def __init__(self, processes):
        super().__init__(processes)
        self.tempProcess = None
        self.tempTime = 0
        self.ganttChartInfo = []

    # proses menghitung fitur
    def calculate(self, process):
        #proses untuk mengurangi nilai remaining time
        if process.getStartTime() is None:
            process.setStartTime(self.current_time)
        process.setBurstTimeRemaining(process.getBurstTimeRemaining()-1)

        #proses untuk menambahkan atribut seperti finish time, turnaround time, waiting time diproses disini
        if process.getBurstTimeRemaining() == 0:
            # Set waktu selesai proses
            process.setFinishTime(self.current_time + 1)

            self.ganttChartInfo.append([process.getName(), 
                                        self.tempTime]) # masukan informasi untuk membuat gantt chart
            self.tempProcess = process
            self.tempTime = 0

            # Hitung turnaround time proses
            process.setTurnaroundTime()

            # Hitung waiting time proses
            process.setWaitingTime()

            # hitung response time
            process.setResponseTime()

            # Set proses menjadi selesai
            process.setIsCompleted(True)
        
        elif self.tempProcess is None or process == self.tempProcess:
            # check apakah temp proses merupakan proses saat ini
            self.ganttChartInfo.append([process.getName(), 
                                        self.tempTime]) # masukan informasi untuk membuat gantt chart
            self.tempProcess = process
            self.tempTime = 0
            

    def run(self):

        # Proses diurutkan berdasarkan waktu kedatangan dengan menggunakan fungsi sorted dan lambda function
        self.processes = sorted(self.processes, key=lambda p: p.getArriveTime())

        while len(self.processes) > 0:
            # membuat list untuk proses yang siap dieksekusi
            ready_processes = []

            # mencari proses mana yang siap untuk di eksekusi pada saat ini
            for process in self.processes:
                if process.getArriveTime() <= self.current_time:
                    ready_processes.append(process)

            # mensorting proses dalam ready proses dengan nilai remaining time
            shortest_process = min(ready_processes, key=lambda x: x.getBurstTimeRemaining())
            self.tempTime += 1
            self.calculate(shortest_process)

            # jika dalam ready proses
            if len(ready_processes) == 0:
                self.current_time += 1
                continue

            if shortest_process.getBurstTimeRemaining() == 0:
                self.completed_processes.append(shortest_process)
                self.processes.remove(shortest_process)

            self.current_time += 1

    # print gantt chart for SRT algorithm
    def printGanttChart(self):
        # create border horizontal
        border = ' '
        for process in self.ganttChartInfo:
            border += '__' * process[1] + ' '

        # create process label
        label = '|'
        for process in self.ganttChartInfo:
            space = '_' * (process[1]-1)
            label += space + process[0] + space + '|'

        # display
        print(border)
        print(label)

        # create list to store intervals for each process
        time = 0
        print(time, end="")
        for process in self.ganttChartInfo:
            print('  ' * (process[1]), end='')
            time += process[1]

            if time > 9:
                print("\b", end="")
                
            print(time, end="")

        print()