import time

import memory.shared.runner as runner
from algutils import get_state_and_answer

def main():
    function_set=["add", "subtract", "multiply", "divide", "pow", "ripfloatvalue"]
    runner.run(function_set, get_state_and_answer)

if __name__ == "__main__":
    tic = time.time()
    main()
    toc = time.time()
    print(f'[loop] Done in {toc-tic:.4f} seconds')