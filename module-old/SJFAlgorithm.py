from SchedulingAlgorithms import SchedulingAlgorithms

# SJF (Shortest Job First)
class SJFAlgorithm(SchedulingAlgorithms):
    def __init__(self, processes):
        super().__init__(processes)

    # fungsi untuk mendapatkan next process
    def getNextProcess(self):
        for process in self.processes:
            if not process.getIsCompleted() and process.getArriveTime() <= self.current_time:
                return process
        return None

    # method to run process algorithm
    def run(self):
        # Urutkan proses berdasarkan burst time
        self.processes = sorted(self.processes, key=lambda p: p.getBurstTime())

        # Loop untuk menjalankan setiap proses
        for i in range(len(self.processes)):
            # Ambil proses berikutnya yang belum selesai dan belum di-queue
            next_process = self.getNextProcess()

            # Jika tidak ada proses yang siap dijalankan, lanjutkan waktu
            if next_process is None:
                self.current_time += 1
                continue

            # Set start time dari proses
            next_process.setStartTime(self.current_time)

            # Update waktu saat ini dengan menambahkan burst time proses
            self.current_time += next_process.getBurstTime()

            # masukan waktu saat ini menjadi finish time
            next_process.setFinishTime(self.current_time)

            # Hitung turnaround time dari proses
            next_process.setTurnaroundTime()

            # Hitung waiting time dari proses
            next_process.setWaitingTime()

            # Hitung response time dari proses
            next_process.setResponseTime()

            # Set proses menjadi selesai
            next_process.setIsCompleted(True)

            #tambahkan proses yang telah dieksekusi ke list
            self.completed_processes.append(next_process)

    # menampilkan gantt chart
    def printGanttChart(self):

        # Proses diurutkan berdasarkan waktu kedatangan dengan menggunakan fungsi sorted dan lambda function
        self.processes = sorted(self.processes, key=lambda p: p.getStartTime())

        # create border horizontal
        border = ' '
        for process in self.processes:
            border += '__' * (process.getBurstTime()) + ' '

        # create process label
        label = '|'
        for process in self.processes:
            space = '_' * (process.getBurstTime()-1)
            label += space + process.getName() + space + '|'

        print(border)
        print(label)
        # print(border)

        print(self.processes[0].getArriveTime(), end="")
        for process in self.processes:
            print('  ' * (process.getBurstTime()), end='')

            if process.getFinishTime() > 9:
                print("\b", end="")
                
            print(process.getFinishTime(), end="")

        print()