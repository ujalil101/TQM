import threading
import queue
import time

class TaskQueueManager:
    def __init__(self, num_worker_threads=3):
        # initalize queue
        self.task_queue = queue.Queue()
        # worker threads
        self.threads = []
        # # of threads
        self.num_worker_threads = num_worker_threads
        self.create_worker_threads()

    def create_worker_threads(self):
        # create number of worker threads
        for _ in range(self.num_worker_threads):
            # each thread will execute  worker method
            t = threading.Thread(target=self.worker)
            # start thread
            t.start()
            # add thread to list
            self.threads.append(t)

    def worker(self):
        #  workr method process tasks from queue
        while True:
            # get task from queue
            task = self.task_queue.get()
            # check if no more tasks
            if task is None:
                break
            # get function, arguments, and keyword arguments from task tuple
            func, args, kwargs = task
            # call function with its arguments
            func(*args, **kwargs)
            # task is compelete
            self.task_queue.task_done()

    def enqueue_task(self, func, *args, **kwargs):
        # enque a task into the task queue
        self.task_queue.put((func, args, kwargs))

    def wait_for_completion(self):
        # wait till all tasks to be processed
        self.task_queue.join()
        # stop worker threads by sending None
        for _ in range(self.num_worker_threads):
            self.task_queue.put(None)
        # wait for all threads to complete
        for t in self.threads:
            t.join()
        print("All tasks processed")

# any function to prcoess
def example_function(name):
    # simple print
    print(f"Hello, {name}!")
    # create some processing time
    time.sleep(1)


if __name__ == "__main__":
    # TaskQueueManager instance with 3 worker threads
    task_manager = TaskQueueManager(num_worker_threads=3)

    
    for i in range(10):
        task_manager.enqueue_task(example_function, f"Task {i}")

    # wait till all tasks to be processed
    task_manager.wait_for_completion()
