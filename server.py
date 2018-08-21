
# coding: utf-8

# # imports

# In[1]:


import sys
import socket
import queue
import threading
import time
import logging

try:
    get_ipython()
    isnotebook = True
except Exception:
    isnotebook = False
    
if isnotebook:
    # convert notebooks
    get_ipython().system('jupyter nbconvert --to script server.ipynb')
    get_ipython().system('jupyter nbconvert --to script server_worker.ipynb')
    
import server_worker


# # settings

# In[2]:


server_address = ("win10-koepke.teco.edu", 1337)
recvbuffsize = 1024
worker_waitseconds = 2.0
sensorthings_address = "http://smartaqnet-dev.teco.edu:8080/FROST-Server/v1.0"


# # logging

# In[3]:


log = logging.getLogger("server")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s(%(name)s): %(message)s")

fh = logging.FileHandler('./log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

sh = logging.StreamHandler(sys.stderr)
sh.setLevel(logging.ERROR)
sh.setFormatter(formatter)
log.addHandler(sh)


# # create socket

# In[4]:


log.info("starting server")
print("starting server")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)


# # init

# In[5]:


threadqueue = queue.Queue()


# # listener (thread)

# In[6]:


def listenerthread(q):
    while True:
        try:
            data, address = sock.recvfrom(recvbuffsize)
        except Exception:
            log.error("cannot receive UDP packet")
            continue
        
        q.put((data, address))


# # worker (thread)

# In[7]:


def workerthread(q):    
    while True:
        if q.empty():
            time.sleep(worker_waitseconds)
            continue
        
        qdata = q.get()
        
        runner = threading.Thread(target=server_worker.run, args=(q, sensorthings_address, qdata))
        runner.setDaemon(True)
        runner.start()


# # start threads

# In[8]:


worker = threading.Thread(target=workerthread, args=(threadqueue,))
worker.setDaemon(True)
worker.start()

listener = threading.Thread(target=listenerthread, args=(threadqueue,))
listener.setDaemon(True)
listener.start()


# # keep alive

# In[9]:


if not isnotebook:
    try:
        while True:
            time.sleep(5.0)
    except:
        log.info("waiting for unfinished tasks")
        print("waiting for unfinished tasks")
        threadqueue.join()
        
        for handler in log.handlers:
            handler.close()
            log.removeFilter(handler)
        
        log.info("closing server")
        print("closing server")
        sock.close()
        quit()

