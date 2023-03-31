from SchedulingAlgorithms import SchedulingAlgorithms

# Priority Scheduling (Preemtive)
class PriorityAlgorithm(SchedulingAlgorithms):
    tempProcess = None
    tempTime = None
    ganttChartInfo = []

    def __init__(self, processes):
        super().__init__(processes)
        self.tempProcess = None
        self.tempTime = 0
        self.ganttChartInfo = []

    def run(self):
        # sort the processes by priority
        self.processes.sort(key=lambda x: x.getArriveTime())

        # set the current time to the arrival time of the first process
        self.current_time = self.processes[0].getArriveTime()

        # loop until all self.processes are completed
        while any(p.getIsCompleted() is False for p in self.processes):
            # find the highest priority process that has arrived and is not yet completed
            highest_priority_process = None
            for process in self.processes:
                if not process.getIsCompleted() and process.getArriveTime() <= self.current_time:
                    if highest_priority_process is None or process.getPriority() < highest_priority_process.getPriority():
                        highest_priority_process = process

            if highest_priority_process != self.tempProcess:
                # check apakah temp proses merupakan proses saat ini
                if self.tempProcess and not self.tempProcess.getIsCompleted():
                    self.ganttChartInfo.append([self.tempProcess.getName(), 
                                                self.tempTime]) # masukan informasi untuk membuat gantt chart
                    self.tempTime = 0
                self.tempProcess = highest_priority_process

            self.tempTime += 1

            # if no process is found, increment the current time to the arrival time of the next process
            if highest_priority_process is None:
                self.current_time = self.processes[min(range(len(self.processes)), key=lambda i: self.processes[i].getArriveTime())].getArriveTime()
                continue

            # set the start time of the process
            if not highest_priority_process.getIsQueued():
                highest_priority_process.setStartTime(self.current_time)
                highest_priority_process.setIsQueued(True)

            # decrement the remaining burst time of the process
            highest_priority_process.setBurstTimeRemaining(highest_priority_process.getBurstTimeRemaining() - 1)

            # if the process has completed execution
            if highest_priority_process.getBurstTimeRemaining() == 0:
                # set the finish time of the process
                highest_priority_process.setFinishTime(self.current_time + 1)

                self.ganttChartInfo.append([highest_priority_process.getName(), 
                                            self.tempTime]) # masukan informasi untuk membuat gantt chart
                self.tempProcess = highest_priority_process
                self.tempTime = 0

                # set the turnaround time and waiting time of the process
                highest_priority_process.setTurnaroundTime()
                highest_priority_process.setWaitingTime()
                highest_priority_process.setResponseTime()

                # set the completed flag of the process
                highest_priority_process.setIsCompleted(True)

                # add the process to the completed processes list
                self.completed_processes.append(highest_priority_process)

            # increment the current time
            self.current_time += 1

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