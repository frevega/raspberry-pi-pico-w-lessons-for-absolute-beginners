import utime # access internal clock of raspberry Pi Pico
import _thread # to access threading function

# declaring led object
spLock = _thread.allocate_lock() # creating semaphore lock

def core1_task():
    while True:
        spLock.acquire() # acquiring semaphore lock
        print("\tCORE_1")
        utime.sleep(0.5) # 0.5 sec or 500us delay
        spLock.release()

_thread.start_new_thread(core1_task, ())
while True:
    spLock.acquire()
    print("CORE_0")
    utime.sleep(0.5)
    spLock.release()
