from Table import Table

# fungsi untuk menampilkan informasi/fitur didalam table
def print_in_table(processes):
    if processes[0].getStartTime():
        # sorting sesuai start time nya
        processes = sorted(processes, key=lambda p: p.getStartTime())
    # else:
    #     # sorting sesuai waktu kedatangan nya
    #     processes = sorted(processes, key=lambda p: p.getArriveTime())

    # set data to list of dictionary
    dictProcesses = []
    for process in processes:
        dictProcesses.append(process.getDict())

    # create and display process with table
    table = Table()
    table.addData(dictProcesses)
    table.display()

# fungsi untuk menampilkan informasi/fitur diluar tabel
def print_off_table(processes):
    # menentukan banyaknya data
    n = len(processes)

    # menentukan waktu terakhir dieksekusi
    total_time = 0
    for process in processes:
        if total_time < process.getFinishTime():
            total_time = process.getFinishTime()

    # menentukan troughput
    throughput = total_time / n

    # Calculate average metrics
    avg_start_time = sum(p.getStartTime() for p in processes) / n
    avg_turnaround_time = sum(p.getTurnaroundTime() for p in processes) / n
    avg_waiting_time = sum(p.getWaitingTime() for p in processes) / n
    avg_response_time = sum(p.getResponseTime() for p in processes) / n
    
    # output
    print("Average Start Time        : {:.2f}".format(avg_start_time))
    print("Average Turnaround Time   : {:.2f}".format(avg_turnaround_time))
    print("Average Waiting Time      : {:.2f}".format(avg_waiting_time))
    print("Average Response Time     : {:.2f}".format(avg_response_time))
    print("Throughput                : {:.2f} second\n".format(throughput))

    # # gantt chart
    # gantt_chart()

# print gantt chart
def printGanttChart(ganttChart):
    
    # check jika gantt chart kosong
    if ganttChart is None:
        print("Gantt chart is empty")
        return

    print("Gantt Chart:")

    # create border horizontal
    border = ' '
    for process in ganttChart:
        border += '__' * process[1] + ' '

    # create process label
    label = '|'
    for process in ganttChart:
        space = '_' * (process[1]-1)
        label += space + process[0] + space + '|'

    # display
    print(border)
    print(label)

    time = 0
    # create list to store intervals for each process
    print(time, end="")
    for process in ganttChart:
        print('  ' * (process[1]), end='')
        time += process[1]

        if time > 9:
            print("\b", end="")
            
        print(time, end="")

    print()

"""
Gantt chart
 ____ __ ____ ____ ____ ____ ____ ____ ____ __ __ ____ __
|_P1_|P2|_P1_|_P0_|_P4_|_P3_|_P0_|_P5_|_P4_|P3|P0|_P4_|P4|
0    2  3    5    7    9   11   13   15   17 18 19   21 22

"""