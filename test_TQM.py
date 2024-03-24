import unittest
import threading
import time
from TQM import TaskQueueManager

# test function 
def test_function(name):
    print(f"Test function executed: {name}")
    time.sleep(0.5)

class TestTaskQueueManager(unittest.TestCase):
    def test_task_queue_manager(self):
        # TQM instance with 2 worker threads
        task_manager = TaskQueueManager(num_worker_threads=2)

        for i in range(5):
            task_manager.enqueue_task(test_function, f"Task {i}")
            
        # wati till all tasks to be processed
        task_manager.wait_for_completion()

        # assert that all tasks were processed
        self.assertTrue(task_manager.task_queue.empty())

if __name__ == "__main__":
    unittest.main()
