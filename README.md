Impedance
=========

User Interface for HP4192A LF Impedance Analyzer.

This program requires that you have IPython Notebook and Windows XP (and later) installed on your local machine. The impedance analyzer must be connected via a GPIB connection. Also, the Python Package [PyVISA](https://pyvisa.readthedocs.org/en/latest/) must be installed on the local machine. 

The repo contains:

* The `.py` Python script that holds all necessary methods for running the program.
* The `.js` Javascript file that builds the GUI/frontend for the analyzer/
* The `.ipynb` file that hosts the UI and runs all python code.

Use matplotlib for all plotting of the data and filtering the data. It comes installed with IPython. See the docs [here](http://matplotlib.org/).

If you are having trouble's connecting the machine, try these steps:

1. Open the file `impedanceanalyzer.py` and look at the first 5 lines.
2. Check that the PyVISA library is located where line 3 indicates.
3. Check that the number after 'GPIB' matches the USB port number that the connection from the analyzer is plugged into the computer.
4. Check that the instrument number (default 17) matches the analyzer.