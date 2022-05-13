from PySide6.QtCore import QObject, Signal, QThread, QObject, Signal


# Worker thread takes runs an async task and emits a signal
# after the task is done once or multiple times
class Worker(QObject):
    taskCompleteSignal = Signal(object)

    def __init__(self, callback, once=True, endCondition=None):
        super(Worker, self).__init__()
        self.asyncTaskCallback = callback
        self.runOnce = once
        self.endCondition = endCondition
        self.isComplete = False

    def runAsyncTask(self):
        if self.runOnce:
            result = self.asyncTaskCallback()
            self.taskCompleteSignal.emit(result)
        else:
            assert (
                self.endCondition
            ), "endCondition must be present to run multiple times"
            while self.endCondition() and not self.isComplete:
                result = self.asyncTaskCallback()
                self.taskCompleteSignal.emit(result)
        self.isComplete = True
        self.taskCompleteSignal.emit(None)


# AsyncTask runs a long running task and after completion it
# returns with the result and finishTask runs in the main UI thread.
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
            if result:
                self.finishTask(result)
        except Exception as e:
            raise e
        finally:
            self.worker_thread.quit()
            self.worker_thread.wait()


# AsyncTask runs a long running task and after completion it
# returns with the result and finishTask runs in the main UI thread.
class AsyncTaskRepeat(object):
    def __init__(
        self,
        handleResult,
        asyncTaskCallback,
        endCondition,
        finishCallback=None,
        cancelCallback=None,
    ):
        super(AsyncTaskRepeat, self).__init__()
        self.worker_thread = QThread()
        self.worker = Worker(asyncTaskCallback, once=False, endCondition=endCondition)
        self.handleFromThread = handleResult
        self.worker_thread.started.connect(self.worker.runAsyncTask)
        self.worker.taskCompleteSignal.connect(self.processResult)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.cancelCallback = cancelCallback
        self.finishCallback = finishCallback

    def _quitThread(self):
        self.worker.isComplete = True
        self.worker_thread.quit()
        self.worker_thread.wait()

    def quit(self):
        if self.cancelCallback:
            self.cancelCallback()
        self._quitThread()

    def processResult(self, result):
        try:
            if result:
                self.handleFromThread(result)
            if self.worker.isComplete:
                if self.finishCallback:
                    self.finishCallback()
                self._quitThread()
        except Exception as _:  # pylint: disable=broad-except
            self._quitThread()
