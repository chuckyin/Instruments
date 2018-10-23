import PySpin
import time

class pgcamera():
    def __init__(self, verbose=False):
        self._system = PySpin.System.GetInstance()
        self._cam_list = self._system.GetCameras()
        self._cam = self._cam_list[0] # assuming one camera
        self._trigger = 1

    def version(self): 
        response = self._system.GetLibraryVersion()
        ver = '%s.%s.%s.%s'%(response.major, response.minor, response.type, response.build)
	return ver 
	
    def num_cameras(self):
	num_cameras = self._cam_list.GetSize()
	return num_cameras

    def configure_trigger(self):
        result = True
        CHOSEN_TRIGGER = self._trigger # 1 for software trigger and 2 for hardware
        try:
            nodemap = self._cam.GetNodeMap()
            node_trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
            if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
                print 'Unable to disable trigger mode (node retrieval). Aborting...'
                return False

            node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
            if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
                return False
            node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())
            node_trigger_source = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
            if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
                return False

            node_trigger_source_software = node_trigger_source.GetEntryByName('Software')
            if not PySpin.IsAvailable(node_trigger_source_software) or not PySpin.IsReadable(
                    node_trigger_source_software):
                return False
            node_trigger_source.SetIntValue(node_trigger_source_software.GetValue())

            node_trigger_mode_on = node_trigger_mode.GetEntryByName('On')
            if not PySpin.IsAvailable(node_trigger_mode_on) or not PySpin.IsReadable(node_trigger_mode_on):
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_on.GetValue())

        except PySpin.SpinnakerException as ex:
            print 'Error: %s' % ex
            return False
        return result

    def initialize(self):
        self._cam.Init()
        self.nodemap = self._cam.GetNodeMap()
        self.nodemap_tldevice = self._cam.GetTLDeviceNodeMap() 
        if self.nodemap != None and self.nodemap_tldevice != None:
            return True
        else:
            return False

    def configure_trigger(self):
        result = True
        CHOSEN_TRIGGER = 1
        
        try:
            node_trigger_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerMode'))
            if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
                print 'Unable to disable trigger mode (node retrieval). Aborting...'
                return False

            node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
            if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
                print 'Unable to disable trigger mode (enum entry retrieval). Aborting...'
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())
            # Select trigger source
            # The trigger source must be set to hardware or software while trigger
            # mode is off.
            node_trigger_source = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerSource'))
            if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
                print 'Unable to get trigger source (node retrieval). Aborting...'
                return False


            node_trigger_source_software = node_trigger_source.GetEntryByName('Software')
            if not PySpin.IsAvailable(node_trigger_source_software) or not PySpin.IsReadable(
                    node_trigger_source_software):
                print 'Unable to set trigger source (enum entry retrieval). Aborting...'
                return False
            node_trigger_source.SetIntValue(node_trigger_source_software.GetValue())

            # Turn trigger mode on
            # Once the appropriate trigger source has been set, turn trigger mode
            # on in order to retrieve images using the trigger.
            node_trigger_mode_on = node_trigger_mode.GetEntryByName('On')
            if not PySpin.IsAvailable(node_trigger_mode_on) or not PySpin.IsReadable(node_trigger_mode_on):
                print 'Unable to enable trigger mode (enum entry retrieval). Aborting...'
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_on.GetValue())
#            print 'Trigger mode turned back on...'

        except PySpin.SpinnakerException as ex:
            print 'Error: %s' % ex
            return False

        return result


    def _grab_next_image_by_trigger(self):
        try:
            result = True
            CHOSEN_TRIGGER = self._trigger # 1 for software trigger and 2 for hardware trigger 
            node_softwaretrigger_cmd = PySpin.CCommandPtr(self.nodemap.GetNode('TriggerSoftware'))
            if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
                print 'Unable to execute trigger. Aborting...'
                return False
            node_softwaretrigger_cmd.Execute()
        except PySpin.SpinnakerException as ex:
            #print 'Error: %s' % ex
            return False
        return result

    def serialnumber(self):
            device_serial_number = ''
            node_device_serial_number = PySpin.CStringPtr(self.nodemap_tldevice.GetNode('DeviceSerialNumber'))
            if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
                device_serial_number = node_device_serial_number.GetValue()
                return device_serial_number
            else:
                return "NoSerial"       
        
    def acquire_images(self, filename):
        try:
            result = True
            node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
            if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
                return False
            node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                    node_acquisition_mode_continuous):
                return False

            acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
            node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
            self._cam.BeginAcquisition()

            try:
                result &= self._grab_next_image_by_trigger()
                image_result = self._cam.GetNextImage()
                if image_result.IsIncomplete():
                    print 'Image incomplete with image status %d ...' % image_result.GetImageStatus()
                else:
                    width = image_result.GetWidth()
                    height = image_result.GetHeight()
                    image_converted = image_result.Convert(PySpin.PixelFormat_Mono8, PySpin.HQ_LINEAR)
                    image_converted.Save(filename)
                    image_result.Release()

            except PySpin.SpinnakerException as ex:
#                print 'Error: %s' % ex
                return False

            self._cam.EndAcquisition()

        except PySpin.SpinnakerException as ex:
#            print 'Error: %s' % ex
            return False

        return result


######### clean up ##########

    def reset_trigger(self):
        try:
            result = True
            node_trigger_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerMode'))
            if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
                return False

            node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
            if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
                return False
            node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())
        except PySpin.SpinnakerException as ex:
#            print 'Error: %s' % ex
            result = False
        return result

    def cleanup(self):
        result = True
        try:
            del self._cam
            self._cam_list.Clear()
            self._system.ReleaseInstance()
        except PySpin.SpinnakerException as ex:
            result = False
        return result
        
if __name__ == "__main__":
    verbose=True
    the_instrument = pgcamera(verbose)
    version = the_instrument.version()
    num_cameras = the_instrument.num_cameras()
    flag = the_instrument.initialize()
    sn = the_instrument.serialnumber()
    conf_flag = the_instrument.configure_trigger()
    time.sleep(2) 
    filename = "test.jpg"
    acq_flag = the_instrument.acquire_images(filename)
    reset_trigger_flag = the_instrument.reset_trigger()
    cleanup_flag = the_instrument.cleanup()
    
    print version
    print num_cameras
    print flag
    print sn
    print conf_flag
    print acq_flag
    print reset_trigger_flag
    print cleanup_flag





