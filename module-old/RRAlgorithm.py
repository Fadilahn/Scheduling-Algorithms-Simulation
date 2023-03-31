from SchedulingAlgorithms import SchedulingAlgorithms

# RR (Round Robin) Algorithm
class RRAlgorithm(SchedulingAlgorithms):
    quantum = None
    queue = []
    exeProgramsCount = 0
    ganttChartInfo = []
    current_time = 0
    n = 0
    processing = True

    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum
        self.queue = []
        self.exeProgramsCount = 0 # waktu saat ini, diupdate setiap menangani proses
        self.ganttChartInfo = []
        self.n = len(processes)

    # mengecek apakah ada proses baru (berdasarkan arrival time)
    def cekProsesBaru(self):
        for i in range(self.n):
            p = self.processes[i]
            c = False
            # jika ditemukan proses dengan waktu datang kurang dari waktu saat ini, belum ada di queue, dan belum selesai
            if p.getArriveTime() <= self.current_time and p.getIsQueued() == False and p.getIsCompleted() == False:
                self.processes[i].setIsQueued(True)
                self.queue.append(i) # push ke queue
                self.exeProgramsCount += 1
                c = True
            if self.exeProgramsCount != self.n and c == False and self.processing == False:
                self.ganttChartInfo.append(["--",1]) # masukan informasi untuk membuat gantt chart
                self.current_time += 1


    # menangani perubahan queue
    def updateQueue(self):
        if len(self.queue)!=0:
            # queue pertama saat ini disimpan ke i (index proses), dan dikeluarkan dari queue
            i = self.queue[0]
            self.queue.pop(0)

            if self.processes[i].getBurstTimeRemaining() == self.processes[i].getBurstTime():
                self.processes[i].setStartTime(self.current_time)
        
            # jika proses saat ini (pada self.queue) akan selesai
            if self.processes[i].getBurstTimeRemaining() <= self.quantum:
                self.processes[i].setIsCompleted(True)
                self.ganttChartInfo.append([self.processes[i].getName(), 
                                            self.processes[i].getBurstTimeRemaining()]) # masukan informasi untuk membuat gantt chart
                self.current_time += self.processes[i].getBurstTimeRemaining()

                self.processes[i].setFinishTime(self.current_time)
                self.processes[i].setTurnaroundTime()
                self.processes[i].setWaitingTime()
                self.processes[i].setBurstTimeRemaining(0)
                self.processes[i].setResponseTime()
        
                # mengecek apakah semua program sudah dijalankan
                if self.exeProgramsCount != self.n:
                    self.cekProsesBaru()
            else:
                # jika proses saat ini tidak akan selesai pada self.quantum saat ini
                self.processes[i].setBurstTimeRemaining(self.processes[i].getBurstTimeRemaining()-self.quantum)
                self.ganttChartInfo.append([self.processes[i].getName(), 
                                            self.quantum]) # masukan informasi untuk membuat gantt chart
                self.current_time += self.quantum
                

                # mengecek apakah semua program sudah dijalankan
                if self.exeProgramsCount != self.n:
                    self.cekProsesBaru()
                
                # karena program belum selesai, maka dikembalikan lagi ke self.queue
                self.queue.append(i)
        else:
            self.cekProsesBaru()
            # return self.current_time

    # fungsi round robin
    def run(self):
        self.processes.sort(key=lambda p: p.getArriveTime())
        self.queue.append(0) # index pertama (index proses) dimasukkan ke queue
        self.processes[0].setIsQueued(True)
        self.current_time = self.processes[0].getArriveTime()
        self.exeProgramsCount = 1
    
        # looping selama masih ada proses di queue
        while len(self.queue)!=0 or self.exeProgramsCount < self.n:
            self.updateQueue()
            if len(self.queue) == 0 :
                self.processing = False
            else:
                self.processing = True
    
    # print gantt chart for RR algorithm
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

        # menentukan waktu start nya
        start = sorted(self.processes, key=lambda p: p.getStartTime())
        time = start[0].getStartTime()

        # create list to store intervals for each process
        print(time, end="")
        for process in self.ganttChartInfo:
            print('  ' * (process[1]), end='')
            time += process[1]

            if time > 9:
                print("\b", end="")
                
            print(time, end="")

        print()