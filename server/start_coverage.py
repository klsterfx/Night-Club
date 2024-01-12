"""
This script is designed to start the server with coverage tracking. It initializes a coverage object 
to monitor the code coverage of the server, specifically targeting the 'server/' directory while omitting 
certain specified files. The coverage data is associated with the process ID to uniquely identify it. 
After setting up the coverage tracker, the script imports and executes the main function from the 'server' module, 
passing the coverage object to it for tracking.
"""

import coverage
import os

# coverage object
cov = coverage.Coverage(data_file=".coverage.{0}".format(os.getpid()),
                        source=["server/"], omit=["coverage_start.py", "coverage_stop_restapi_call.py"])
cov.start()

from server import main

if __name__ == '__main__':
    main(cov)
