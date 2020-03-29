import _thread
import threading
import time

class basicthread(threading.Thread):
    def __init__(self, cb, continual = False):
        """ DOCS
            this is meant for quick threads
            the cb is a callback to a function
            this function should look like
            def func(running):
                loop: #PUT LOOP HERE IF NECESSARY
                    ... #PUT CODE HERE
                    if !running[0]: # has to be a list for pointer functionality
                        break
        """
        threading.Thread.__init__(self)
        self.cb = cb
        self.deadline = 0
        self.running = [False]
        self.continual = continual
    def run(self):
        self.running[0] = True
        print(self.getName() + " running id: " + str(id(self.running)))
        self.cb(self.running)
        while self.continual and self.running[0]:
            self.cb(self.running)
        self.running[0] = False
    def begin(self, join, deadline = 0.0, name = "BASICTHREAD"):
        self.setName(name)
        self.start()
        self.deadline = deadline
        if join == True and deadline != 0.0:
            self.join(self.deadline)
        elif join == True and deadline == 0.0:
            self.join()    
    def stop(self):
        self.running[0] = False


def example(running):
    for i in range(20):
        print("running: " + str(running[0]) + " id: " + str(id(running)))
        time.sleep(1)
        if not running[0]:
            break;

if __name__ == "__main__":
    bt = basicthread(example)
    bt.begin(True, 10, "PRINT_HI")
    bt.running[0] = False
    print("bt running: " + str(bt.running) + " id: " + str(id(bt.running)))
