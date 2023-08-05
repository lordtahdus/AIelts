import multiprocessing
import os
from scraping import *


def run_script(number):
    while True:
        os.system(f"python auto_gen.py {number}")


if __name__ == "__main__":
    num_processes = 3

    args_list = list(range(1, num_processes + 1))

    processes = []
    for args in args_list:
        process = multiprocessing.Process(target = run_script, args = (args,))
        processes.append(process)
        process.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("Terminating processes...")
        for process in processes:
            process.terminate()
          