from typing import Union, List, Dict

from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter

from pymodaq_plugins_nkt.hardware.superk_extreme import Extreme

import pylablib as pll


class DAQ_Move_SuperK_Extreme(DAQ_Move_base):
    """ Instrument plugin class for NKT Photonics lasers, tested on SuperK Extreme EXB-6 model.
    
    This object inherits all functionalities to communicate with PyMoDAQ's DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Should be compatible with all NKT Photonics SuperK Extreme lasers. Tested on SuperK Extreme EXB-6 model
    with PyMoDAQ 4.4.6 on Windows 11 and Python 3.11.10. Installing "CONTROL" software from NKT website
    should provide all necessary drivers → https://www.nktphotonics.com/support/

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
    """

    is_multiaxes = False
    _axis_names: Union[List[str], Dict[str, int]] = ['Power']   # name of the axis
    _controller_units: Union[str, List[str]] = '%'              # units of the axis
    _epsilon: Union[float, List[float]] = 0                     # laser has no moving parts → epsilon = 0
    data_actuator_type = DataActuatorType.DataActuator  # can be DataActuatorType.float for old data style

    _laser_port = None

    ports = pll.list_backend_resources("serial")

    params = [   # TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        {'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports},
        {'title': 'Power', 'name': 'power', 'type': 'slide', 'value': 17, 'default': 17, 'min': 17, 
         'max': 100, 'subtype': 'linear','suffix':'%','siPrefix':True}
    ]

    def ini_attributes(self):

        self.controller: Extreme = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        pos = DataActuator(data=self.controller.your_method_to_get_the_actuator_value())  # when writing your own plugin replace this line
        pos = self.get_position_with_scaling(pos)
        return pos

    # def user_condition_to_reach_target(self) -> bool:
    #     """ Implement a condition for exiting the polling mechanism and specifying that the
    #     target value has been reached

    #    Returns
    #     -------
    #     bool: if True, PyMoDAQ considers the target value has been reached
    #     """
    #     # TODO either delete this method if the usual polling is fine with you, but if need you can
    #     #  add here some other condition to be fullfilled either a completely new one or
    #     #  using or/and operations between the epsilon_bool and some other custom booleans
    #     #  for a usage example see DAQ_Move_brushlessMotor from the Thorlabs plugin
    #     return True

    def close(self):
        """Terminate the communication protocol"""
        self.controller.close_connection()  # when writing your own plugin replace this line

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "com_port":
            self.controller.close_connection()
            self.controller.open_connection(port=self.settings['com_port'])

        elif param.name() == 'power':
            self.set_power(value=int(self.settings['power']))
            # do this only if you can and if the units are not known beforehand, for instance
            # if the motors connected to the controller are of different type (mm, µm, nm, , etc...)
            # see BrushlessDCMotor from the thorlabs plugin for an exemple
        
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        # self.ini_stage_init(slave_controller=controller)  # will be useful when controller is slave

        if self.is_master:  # is needed when controller is master
            self.controller = PythonWrapperOfYourInstrument(arg1, arg2, ...) #  arguments for instantiation!)
            # todo: enter here whatever is needed for your controller initialization and eventual
            #  opening of the communication channel

        info = "Whatever info you want to log"
        initialized = self.controller.a_method_or_atttribute_to_check_if_init()  # todo
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_set_an_absolute_value(value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_set_a_relative_value(value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_home(self):
        """Call the reference method of the controller"""

        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_get_to_a_known_reference()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def stop_motion(self):
      """Stop the actuator and emits move_done signal"""

      ## TODO for your custom plugin
      raise NotImplemented  # when writing your own plugin remove this line
      self.controller.your_method_to_stop_positioning()  # when writing your own plugin replace this line
      self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


if __name__ == '__main__':
    main(__file__)
