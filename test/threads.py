#!/usr/local/bin/python

import threading, time, random
import Queue
import sys

Q = Queue.Queue()

print_lock = threading.Lock()

def Log():
    while True:
        if not Q.empty():
            print Q.get()

def get_name(msg, sec):
    for _ in xrange(msg):
        time.sleep(sec)
        # Q.put("ID " + str(msg))
        # print msg
        sys.stdout.write("ID" + str(msg) + "\n")

class worker ():
    pass

def main():
    ID = 0
    threading.Thread(target=Log).start()
    while True:
        ID += 1
        time.sleep(0.02)
        t1 = threading.Thread(target=get_name, args = (ID,0.01))
        t1.start()
    t2 = threading.Thread(target=get_name, args = ("--T2",0.1))
    t2.start()

if __name__ == '__main__':
    sys.stdout.write('\033[1;92m' + "HELLO ALL" + "\033[0m")
    print 123
    # main()
    # print dict([("1","2"), ("1","4")])
