import multiprocessing as mp
from multiprocessing.managers import BaseManager


def worker_func(obj):
    print(obj)


class EqpLogic:
    pass


class EqpCompiles:
    eqp = dict[str, EqpLogic]()
    mp = list[{"name": str, "logic": compile}]()


class EqpCompileManager(BaseManager):
    pass


EqpCompileManager.register('EqpCompile', EqpCompiles)

if __name__ == '__main__':
    # Create a shared instance of the class
    compile_manager = EqpCompileManager()
    compile_manager.start()
    md_: EqpCompiles = compile_manager.EqpCompiles()


    pool = mp.Pool(processes=4)

    pool.map(worker_func, [md_] * 4)

    pool.close()
    pool.join()

    print(f'The final value of the shared object is {md_}.')

    compile_manager.shutdown()
    # Print the final value of the shared object
