from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

print('=== SUPPRESS WARNING ===')
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

import time
from memory.experiments.step.run import main


if __name__ == "__main__":
    tic = time.time()
    main()
    toc = time.time()
    print(f'[loop] Done in {toc-tic:.4f} seconds')