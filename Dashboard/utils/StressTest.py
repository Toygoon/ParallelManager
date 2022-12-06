from multiprocessing import Pool, cpu_count
from datetime import datetime


class StressTest:
    def stress_test(args):
        cpu, value = args
        start_time = datetime.now()
        for i in range(value):
            value = value * i

    if __name__ == '__main__':
        start_time = datetime.now()
        cpu_count = cpu_count()
        x = 1000
        max, persist = 1000000000, 5
        while x < max:
            for i in range(persist):
                with Pool(cpu_count) as mp_pool:
                    mp_pool.map(stress_test, [(cpu, x) for cpu in range(cpu_count)])
            x *= 10