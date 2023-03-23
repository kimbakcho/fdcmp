import environ
from pathlib import Path

from bFdcAPI.MP.UseCase import FdcMpUseCase

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env('.env.local')

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

if __name__ == '__main__':
    case = FdcMpUseCase()
    cases = case.getMLB(1)
    print(cases)
