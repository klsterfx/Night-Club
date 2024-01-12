"""
This script is used to send a request to the local server to stop the coverage tracking.
It makes a GET request to the 'stopcoverage' endpoint of the server running on localhost at port 5000.
This is typically used to signal the server to stop coverage measurement and save the coverage data.
"""

import requests

if __name__ == '__main__':
    requests.get("http://localhost:5000/stopcoverage")
