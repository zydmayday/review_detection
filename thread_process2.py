from threading import Thread, Lock

queue = []
lock = Lock()

class FileReaderThread(Thread):
	