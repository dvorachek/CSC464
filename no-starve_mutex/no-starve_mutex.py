import threading

class Locks(object):
    def __init__(self):
        self.mutex = threading.Lock()
        self.t1 = threading.Lock()
        self.t2 = threading.Lock()
        self.room1 = 0
        self.room2 = 0
        self.t2.acquire()


class NoStarveThread(threading.Thread):
    def __init__(self, locks, id):
        threading.Thread.__init__(self)
        self.l = locks
        self.id = id
    
    def run(self):
        print('this is where the magic starts')
        self.l.mutex.acquire()
        self.l.room1 += 1
        self.l.mutex.release()

        self.l.t1.acquire()
        self.l.room2 += 1
        self.l.mutex.acquire()
        self.l.room1 -= 1

        if self.l.room1 == 0:
            self.l.mutex.release()
            self.l.t2.release()
        else:
            self.l.mutex.release()
            self.l.t1.release()

        self.l.t2.acquire()
        self.l.room2 -= 1

        print("Thread {} is in the critical section".format(self.id))

        if self.l.room2 == 0:
            self.l.t1.release()
        else:
            self.l.t2.release()


if __name__=='__main__':
    locks = Locks()
    threads = [NoStarveThread(locks, id) for id in range(10)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    print('\nMain exiting')
