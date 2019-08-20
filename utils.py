import time

def time_cycle(timeStamp):
    timeArray = time.localtime(timeStamp)
    formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(formatTime)
    return formatTime



if __name__ == '__main__':
    time_cycle(1557244800)