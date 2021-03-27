instruments
===================
![OpenExecLogo](https://github.com/chuckyin/Instruments/blob/master/logo/instrument_logo.PNG)\
Open-source collecttion repository for shared instruments. This includes things controlled over serial directly and visa through gbip, serial, or usb. This also provides the Python serial library, as many instruments require it, and it is often useful in parallel for talking to devices under test. 


Note for OSX/VISA:
-------------------
- Install NI-VISA (http://www.ni.com/download/ni-visa-5.3/3824/en/)
- NI only provides a 32-bit version of the VISA library for OSX.  Python needs to be run in 32bit mode to deal with that.
    Make this happen by setting an environment variable VERSIONER_PYTHON_PREFER_32_BIT to 'yes.'
    "export VERSIONER_PYTHON_PREFER_32_BIT=yes"
- To use GPIB instruments you will need a driver for the usb bridge. NI's is here: http://www.ni.com/download/ni-488.2-3.0.1/2703/en/

RUNNING TESTS/ GUIDELINES:
-------------------
- All code in this repository should be linted BEFORE opening a pull request. Useful information can be found:
    - https://www.pylint.org/
    - git@github.com:PyCQA/pylint.git
    - For example, if the pygiene.cfg and pylint.cfg has been written under test_utils folder. Make Running: <code>python ../test_utils/pygiene.py . -cfg pygiene.cfg -pep8 ../test_utils/pep8.cfg -pylint ../test_utils/pylint.cfg </code> in the root directory of this repository
- If possible, run the tests/ on any files you may have changed. This is a bit wonky. One needs to run the tests as a module to get around python import from above weirdness:
    - e.g. dmm test: python -m tests.e34461_dmm_test TCPIP::176.18.12.213

VISA:
-------------------
- visa_instrument provides a generic base class that wraps pyvisa's Instrument with some convenience functions.
    All drivers for visa instruments should inherit from this.
- Agilent 34461A dmm (Command-compatible with 34460, 34410 and 34411, but ranges/settings may differ.):
    - http://literature.cdn.keysight.com/litweb/pdf/34460-90901.pdf
    - Tested on OSX:
        - TCP/IP
        - USB
    - Tested on Windows:
        - USB
- Agilent e364x Power supplies:
    - http://cp.literature.agilent.com/litweb/pdf/E3646-90001.pdf * only 1 channel.
    - http://cp.literature.agilent.com/litweb/pdf/E3640-90001.pdf
    - Tested on OSX:
        - USB -> GPIB (using NI module)
    - Tested on Windows:
        - USB -> GPIB (using NI Module)
- Agilent 34972 MUX/DMM chassis (command-compatible with 34970)
    - Tested on OSX USB.

Serial:
-------------------
(Library provided with minor fix to make windows work)
- BK8500 dc load (provided my manufacturer)
- KTA Relay
    - Tested on OSX and Windows
- linmotasf(currently not in this repo, fix!)

Note for LitePoint equipments iqNFC and iqXel:
-------------------
- Both support SCPI and communicate with ethernet cable.

Other:
-------------------
- nircmd windows utility (see http://www.nirsoft.net/utils/nircmd.html)
- jlink programmer
- ni_frequency_ctr
- ni_usb_dio
- generic_gpib_driver (to be deprecated)
- iqNFC 
- iqXel 
