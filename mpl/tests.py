import multiprocessing as mp
from multiprocessing.managers import BaseManager


def worker_func(obj):
    print(obj)


class EqpCompileManager(BaseManager):
    pass


if __name__ == '__main__':
    # Create a shared instance of the class
    compile_manager = EqpCompileManager()
    compile_manager.start()


    pool = mp.Pool(processes=4)


    compile_manager.shutdown()
    # Print the final value of the shared object
