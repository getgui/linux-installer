from PySide6.QtCore import QObject, Signal, QThread, QObject, Signal


class Worker(QObject):
    taskCompleteSignal = Signal(dict)

    def __init__(self, callback):
        super(Worker, self).__init__()
        self.asyncTaskCallback = callback

    def runAsyncTask(self):
        result = self.asyncTaskCallback()
        self.taskCompleteSignal.emit(result)


class AsyncTask(object):
    def __init__(self, finishTask, asyncTaskCallback):
        super(AsyncTask, self).__init__()
        self.worker_thread = QThread()
        self.worker = Worker(asyncTaskCallback)
        self.finishTask = finishTask
        self.worker_thread.started.connect(self.worker.runAsyncTask)
        self.worker.taskCompleteSignal.connect(self.taskDone)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def taskDone(self, result):
        try:
            self.finishTask(result)
        except Exception as e:
            raise e
        finally:
            self.worker_thread.quit()
            self.worker_thread.wait()
