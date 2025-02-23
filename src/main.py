#import setup
from db import get_connection
import counters
import threading
import time

def start_threads(counter, name):
    start = time.time_ns()
    threads = []

    for i in range(10):
        t = threading.Thread(target=counter, args=(get_connection(),))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time_ns()
    print(f"Execution time for {name}: {(end - start)/1_000_000} ms")

start_threads(counters.lost_update, "lost update")
counters.print_counter("lost update")
counters.reset_row()

start_threads(counters.in_place_update, "in place update")
counters.print_counter("in place update")
counters.reset_row()

start_threads(counters.row_level_locking, "row level locking")
counters.print_counter("row level locking")
counters.reset_row()

start_threads(counters.optimistic_concurrency_control, "optimistic concurrency control")
counters.print_counter("optimistic concurrency control")
counters.reset_row()

counters.close_connection()