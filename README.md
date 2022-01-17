# weatherstnapi
API and forwarder to collect near-realtime data from my weatherstation and send to OpenHAB

There are two parts to this
weatherapi - reads data from pywws weatherstation software and publishes an API via Flask 
weatherfwd - reads data from the API and pushes it to OpenHAB

I chose this route because python_openhab requires Python 3.5+ but pywws is only really supported on python 2.7, 
and also python_openhab had unresolvable dependencies with Python 3.5. Hence i could not publish directly
from the pywws installation to OpenHAB.
