=============================================================================
 Copyright © 2017 FLIR Integrated Imaging Solutions, Inc. All Rights Reserved.

 This software is the confidential and proprietary information of FLIR
 Integrated Imaging Solutions, Inc. ("Confidential Information"). You
 shall not disclose such Confidential Information and shall use it only in
 accordance with the terms of the license agreement you entered into
 with FLIR Integrated Imaging Solutions, Inc. (FLIR).

 FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
 SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
 SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
 THIS SOFTWARE OR ITS DERIVATIVES.
=============================================================================

PySpin is a wrapper for FLIR Integrated Imaging Solutions' Spinnaker library.

FLIR Integrated Imaging Solutions' website is located at https://www.ptgrey.com

The PySpin Python extension provides a common software interface to control and acquire images from FLIR USB 3.0,
GigE, and USB 2.0 cameras using the same API under 32- or 64-bit Windows.

--------------------------------------------------------------------------------------------------------------
Instructions on how to install the PySpin package and run the examples on Windows and Linux

Windows
==============================================================================================================
1. Ensure that Python is installed on the system before installing PySpin using the instructions below.
Note that the default install links on the official python website https://www.python.org/downloads/
is for 32-bit windows. To download the 64 bit version, click into the specific Python release version
to download the x64 installer.

2. To ensure prerequisites such as drivers and Visual Studio redistributables are installed on the system,
run the Spinnaker SDK installer that corresponds with the PySpin version number. For example, if installing
PySpin 1.8.0.0, install Spinnaker 1.8.0.0 beforehand, selecting only the Visual Studio runtimes and drivers.


3. Install numpy (required for Image.GetData()) and the wheel using pip:
    ex. "C:\Python36\python.exe -m pip install numpy spinnaker_python-1.x.x.x-cp36-cp36m-win_amd64.whl" for 64-bit Python 3.6

    Ensure that the wheel downloaded matches the Python version you are installing to!

4. Once installed, the PySpin examples can be ran directly from the command prompt.

    For example if PySpin is installed for Python 3.6 and the python install directory is in C:\Python36\,
    run the following from the unzipped installation package:
        "C:\Python36\python.exe Examples\Python3\Acquisition.py"


Linux
==============================================================================================================

1. Ensure that the corresponding version of the Spinnaker SDK Debian packages and their prerequisites are installed
   beforehand. (ex. install the 1.8.0.45 packages if the wheel version is also 1.8.0.45)

2. Ensure numpy is installed for Python (required for Image.GetData()):
    "python -m pip install numpy" for 2.7
    "python3.6 -m pip install numpy" for 3.6

3. Install wheel for specific Python version:
    ex. "sudo python -m pip install spinnaker_python-1.x.x.x-cp27-cp27mu-linux_x86_64.whl" for 64-bit Python 2.7

4. The examples are located in the Examples folder of the extracted tarball. Run with:
    ex. "python2.7 Examples/Python2/DeviceEvents.py"

--------------------------------------------------------------------------------------------------------------
*** CHANGELOG ***
1.10beta:
    * IMPORTANT *
     This update introduces breaking changes to the SpinnakerException class. All methods of SpinnakerException no
     longer exist, please replace all usages of SpinnakerException with any of the following attributes:
        message: Normal exception message.
        fullmessage: Exception message including line, file, function, build date, and time (from C++ library).
        errorcode: Integer error code of the exception.
     The SpinnakerException instance itself can be printed, as it derives from the BaseException class and has a default
     __str__ representation. See examples for usage.

    - Added support for SpinUpdate
    - Image creation using NumPy arrays (although the int type of the array must be uint8)

*** GENERAL NOTES ***
- This is currently a beta, and bugs may be present. Please report any bugs you encounter!
- Except for the changes listed below, most function names are exactly the same as the C++ API
    - See examples for usage

*** API CHANGES FROM C++ ***
- The majority of headers from the C++ API have been wrapped, with the exception of:
    - Headers with "Adapter" or "Port" in the name
    - NodeMapRef.h, NodeMapFactory.h
    - Synch.h, GCSynch.h, Counter.h, filestream.h

- INode and IValue types (esp. returned from GetNode()) have to be initialized to their respective pointer types
    (ex. CFloatPtr, CEnumerationPtr) to access their functions
    - See examples for usage

- CameraPtr, CameraList, InterfacePtr, InterfaceList, and SystemPtr have to be manually released and/or deleted
    before program exit (use del operator)
    - See EnumerationEvents example

- Image.GetData() returns a 1-D NumPy array of integers, the int type depends on the pixel format of the image

- Image.GetNDArray() returns a 2 or 3-D NumPy array of integers, only for select image formats
    - This can be used in libraries such as PIL and/or opencv

- Node callbacks take in a callback class instead of a function pointer
    - Register is now RegisterNodeCallback, Deregister is now DeregisterNodeCallback
    - See NodeMapCallback example for more details

- IImage.CalculateChannelStatistics(StatisticsChannel channel) returns a ChannelStatistics object representing stats
  for the given channel in the image (these stats are properties within the ChannelStatistics object; see the docstring for details)
  - This replaces ImageStatistics!

- Pass-by-reference functions now return the type and take in void
    - GetFeatures() returns a Python list of IValue, instead of taking in a FeatureList_t reference
    - GetChildren() returns a Python list of INode, instead of taking in a NodeList_t reference
        - Same with GetEntries(), GetNodes()
    - GetPropertyNames() returns a Python list of str, instead of taking in a gcstring_vector reference
    - See DeviceEvents example for usage

- Methods Get() and Set() for IRegister and register nodes use NumPy arrays
    - Get() takes in the length of the register to read and two optional bools, returns a NumPy array
    - Set() takes in a single NumPy array
