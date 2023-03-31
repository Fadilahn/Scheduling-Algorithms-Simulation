# import liblary yang dibutuhkan
import glob
import time
import sys
sys.path.append("module") # menambahkan Module directory ke path

# import model
from Process import Process
from fitur import print_in_table, print_off_table, printGanttChart
from FCFS import FCFS
from SJF import SJF
from SRT import SRT
from Priority import Priority
from PriorityPreemptive import PriorityPreemptive
from RR import RR

# BREAK PROGRAM
# ====================================================================================================================================

# fungsi untuk menampilkan informasi setelah di proses
def printInfo(processes, ganttChart=None):
    # display information in table
    print_in_table(processes)

    # display information off table
    print_off_table(processes)

    if ganttChart:
        # display gantt chart
        printGanttChart(ganttChart)

# MAIN PROGRAM 
# ========================

# read data file .txt dalam direktori TestCase
txt_files = glob.glob("test-case/*.txt")

# simpan nama algoritma penjadwalan
schedulingAlgorithms = ["FCFS (First Come First Served)",
                        "SJF (Shortest Job First)",
                        "SRT (Shortest Remaining Time)",
                        "Priority Scheduling (Non-Preemptive)",
                        "Priority Scheduling (Preemptive)",
                        "RR (Round Robin)"
                        ]

# Display
print()
print('-' * 35 + " Simulation Scheduling Algorithm " + '-' * 35, end="\n\n")

# SIMULATION
while True:
    
    print("Select input proses:")
    print("1. Manual")
    print("2. Import test case")
    print("0. Exit")
    print('=' * 30)
    print("Enter number:")
    choice = int(input("-> "))
    print('-' * 10, end="\n\n")

    processes = []
    if choice == 1:
        # manual input
        n = int(input("Enter how many process: "))
        for i in range(n):
            arrive_time = int(input("Enter Arrive Time: "))
            burst_time = int(input("Enter Burst Time : "))
            processes.append(Process("P"+str(i), arrive_time, burst_time))

    elif choice == 2:
        # input test case dengan data file .txt
        # contoh format data (
        #                     jumlah_data {1}
        #                     nama_proses burst_time arrive_time priority {jumlah data}
        #                     quantum {1}
        #                     )
        """ data.txt
        2
        P0 3 5 2
        P1 0 4 3
        3
        """

        # menampilkan isi direktori file .txt
        print("Select file .txt:")
        for i, file in enumerate(txt_files):
            print(f"{i+1}. {file}")
        print('=' * 30)
        print("Warning! Pastikan data sesuai dengan format")
        print("Enter number:")
        choice = int(input("-> "))
        print('-' * 10, end="\n\n")

        # menentukan nama file nya
        if choice <= len(txt_files):
            filename = txt_files[choice-1]
        else:
            print("[!]> Invalid choice <[!]", end="\n\n")
            continue

        # import test case (read)
        with open(filename, 'r') as f:
            data = f.readlines()

        # data dimasukan ke variabel processes
        for line in data[0:-1]:
            values = line.strip().split()
            if len(values) == 4:
                name, arrival_time, burst_time, priority = values
                processes.append(Process(name, int(arrival_time), int(burst_time), int(priority)))
            elif len(values) == 3:
                name, arrival_time, burst_time = values
                processes.append(Process(name, int(arrival_time), int(burst_time),))
            else:
                # baris tidak memiliki 3 atau 4 value
                pass

        quantum = int(data[-1].strip())  # quantum
        n = len(processes)  # jumlah data

    elif choice == 0:
        break

    else:
        print("[!]> Invalid choice <[!]", end="\n\n")
        continue

    if processes:

        # menampilkan input prosesnya
        print("Input Process:")
        print_in_table(processes)

        while True:
            print("Scheduling Algorithms:")
            for i, algorithm in enumerate(schedulingAlgorithms):
                print(f"{i+1}. {algorithm}")
            print("0. Exit")
            print('=' * 30)
            print("Enter number:")
            choice = int(input("-> "))
            print('-' * 10, end="\n\n")

            if choice == 4:
                if not processes[0].getPriority():
                    print("Enter Priority:")
                    print("Name Arrive Burst Priority")
                    for process in processes:
                        print(f"{process.getName()}   {process.getArriveTime()}      {process.getBurstTime()}     ", end="")
                        process.setPriority(int(input()))
                
                print()

            elif choice == 6:
                set_quantum = input("Set quantum: ")
                
                if set_quantum:
                    quantum = int(set_quantum)

            # Process
            # ===================================================

            # delay biar statisfying
            if choice != 0 and choice < 7:
                for i in range(4):
                    print('.' * (i+1))
                    time.sleep(0.2)
                print()
            
            # kondisi sesuai pilihan
            if choice == 1:
                # process FCFS (First Come First Served) algorithm
                fcfs = FCFS(processes)
                fcfs.run()
                processes = fcfs.getCompletedProcesses()

                print('-' * 35 + " FCFS (First Come First Served) " + '-' * 35)

                # display information 
                printInfo(processes, fcfs.getGanttChart())

            elif choice == 2:
                # process SJF (Shortest Job First) 
                sjf = SJF(processes)
                sjf.run()
                processes = sjf.getCompletedProcesses()

                print('-' * 35 + " SJF (Shortest Job First) " + '-' * 35)

                # display information 
                printInfo(processes, sjf.getGanttChart())

            elif choice == 3:
                # process SRT (Shortest Remaining Time) 
                srt = SRT(processes)
                srt.run()
                processes = srt.getCompletedProcesses()

                print('-' * 35 + " SRT (Shortest Remaining Time) " + '-' * 35)

                # display information
                printInfo(processes, srt.getGanttChart())

            elif choice == 4:
                if processes[0].getPriority():
                    # process Priority 
                    priority = Priority(processes)
                    priority.run()
                    processes = priority.getCompletedProcesses()

                    print('-' * 35 + " Priority " + '-' * 35)

                    # display information
                    printInfo(processes, priority.getGanttChart())

                else:
                    print("[!]> The input process has no priority <[!]")

            elif choice == 5:
                if processes[0].getPriority():
                    # process Priority Preemtive 
                    priority = PriorityPreemptive(processes)
                    priority.run()
                    processes = priority.getCompletedProcesses()

                    print('-' * 35 + " Priority Preemtive " + '-' * 35)

                    # display information
                    printInfo(processes, priority.getGanttChart())

                else:
                    print("[!]> The input process has no priority <[!]")

            elif choice == 6:
                # process RR (Round Robin) 
                rr = RR(processes, quantum)
                rr.run()
                processes = rr.getCompletedProcesses()

                print('-' * 35 + " RR (Round Robin) " + '-' * 35)

                # display information
                printInfo(processes, rr.getGanttChart())

            elif choice == 0:
                break

            else:
                print("[!]> Invalid choice <[!]")
            
            print()
            print('-' * 100, end="\n\n")

            # ===================================================
            # reset
            for process in processes:
                process.reset()
                
    else:
        print("[!]> No process to run <[!]")


# Input
# -----------
# test case secara hardcode
"""
processes = [
    Process("P0", 5, 3, 2),
    Process("P1", 4, 0, 3),
    Process("P2", 1, 1, 2),
    Process("P3", 3, 5, 4),
    Process("P4", 7, 3, 3),
    Process("P5", 2, 8, 1),
]
quantum = 2
n = len(processes)
"""