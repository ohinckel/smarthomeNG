#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2016       Christian Strassburg      c.strassburg(a)gmx.de
#  Copyright 2017-      Martin Sinn                       m.sinn@gmx.de
# 
#########################################################################
#  This file is part of SmartHomeNG
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG  If not, see <http://www.gnu.org/licenses/>.
#########################################################################

from lib.model.smartobject import SmartObject
from lib.utils import Utils

import logging
import os

class SmartPlugin(SmartObject, Utils):
    """
    The class SmartPlugin implements the base class of call smart-plugins.
    The implemented methods are described below.

    In adition the methods implemented in lib.utils.Utils are inhereted.
    """
    
    __instance = ''     #: Name of this instance of the plugin
    _sh = None          #: Variable containing a pointer to the main SmartHomeNG object; is initialized during loading of the plugin; :Warning: Don't change it
    _shortname = ''     #: Shortname of the plugin; is initialized during loading of the plugin; :Warning: Don't change it
    _classname = ''     #: Classname of the plugin; is initialized during loading of the plugin; :Warning: Don't change it

    logger = logging.getLogger(__name__)
        
    
    def get_shortname(self):
        """
        return the shortname of the plugin (name of it's directory)
        
        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :return: shortname of the plugin
        :rtype: str
        """
        return self._shortname
                
        
    def _set_shortname(self, shortname):
        """
        ...
                
        :Note: Usually **you don't need to call this method**, since it is called during loading of the plugin

        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :param shortname: short name of the plugin (name of it's directory)
        :type shortname: str
        """
        self._shortname = shortname
        
        
    def get_classname(self):
        """
        return the classname of the plugin
        
        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :return: classname of the plugin
        :rtype: str
        """
        return self._classname
                
        
    def _set_classname(self, classname):
        """
        ...
                
        :Note: Usually **you don't need to call this method**, since it is called during loading of the plugin

        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :param classname: name of the plugin's class
        :type classname: str
        """
        self._classname = classname
        
        
    def get_version(self):
        """
        Return plugin version
        
        :return: plugin version
        :rtype: str
        """
        return self.PLUGIN_VERSION
        
    
    def _set_instance_name(self, instance):
        """
        set instance name of the plugin
        
        :Note: Usually **you don't need to call this method**, since the instance name is set during startup from the plugin configuration in etc/plugin.yaml
        
        :param instance: Name of this instance of the plugin
        :type instance: str
        """
        if self.ALLOW_MULTIINSTANCE:
            self.__instance = instance
        else: 
#            self.logger.warning("Plugin does not allow more than one instance")
            self.logger.warning("Plugin '{}': Only multi-instance capable plugins allow setting a name for an instance".format(self.get_shortname()))


    def get_instance_name(self):
        """
        Returns the name of this instance of the plugin
        
        :return: instance name
        :rtype: str
        """
        return self.__instance


    def is_multi_instance_capable(self):
        """
        Returns information if plugin is capable of multi instance handling
        
        :return: True: If multiinstance capable
        :rtype: bool
        """
        if self.ALLOW_MULTIINSTANCE:
            return True
        else:
            return False
  
  
    def get_plugin_dir(self):
        """
        return the directory where the pluing files are stored in
        
        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :return: name of the directory
        :rtype: str
        """
        return self._plugin_dir 
                
        
    def _set_plugin_dir(self, dir):
        """
        Set the object's local variable `_sh` to the main smarthomeNG object.
        You can reference the main object of SmartHmeNG by using self._sh.
        
        :Note: Usually **you don't need to call this method**, since it is called during loading of the plugin

        :note: Only available in SmartHomeNG versions **beyond** v1.3
        
        :param dir: name of the directory where the plugin resides in
        :type dir: str
        """
        self._plugin_dir = dir
        
        
    def get_info(self):
        """ 
        Returns a small plugin info like: class, version and instance name
        
        :return: plugin Info
        :rtype: str
        """
        return "Plugin: '{0}.{1}', Version: '{2}', Instance: '{3}'".format(self.__module__, self.__class__.__name__,  self.get_version(),self.get_instance_name())


    def __get_iattr(self, attr):
        """
        Returns item attribute for this plugin instance
            
        :param attr: name of attribute
        :type attr: str
        
        :return: attributr
        :rtype: str
        """
        if self.__instance == '':
            return attr
        else:
           return "%s@%s"%(attr, self.__instance)


    def __get_iattr_conf(self, conf, attr):
        """
        returns item attribute name including instance if required and found
        in item configuration

        :param conf: item configuration
        :param attr: attribute name
        :type conf: str
        :type attr: str
        
        :return: name of item attribute (including instance) or None (if not found)
        :rtype: str
        """
        __attr = self.__get_iattr(attr)
        if __attr in conf:
            return __attr
        elif "%s@*"%attr in conf:
            return "%s@*"%attr
        return None


    def has_iattr(self, conf, attr):
        """
        checks item configuration for an attribute
        
        :param conf: item configuration
        :param attr: attribute name
        :type conf: str
        :type attr: str

        :return: True, if attribute is in item configuration
        :rtype: Boolean 
        """
        __attr = self.__get_iattr_conf(conf, attr)
        return __attr is not None
    
    
    def get_iattr_value(self, conf, attr):
        """
        Returns value for an attribute from item config
        
        :param conf: item configuration
        :param attr: attribute name
        :type conf: str
        :type attr: str
        
        :return: value of an attribute
        :rtype: str
        """
        __attr = self.__get_iattr_conf(conf, attr)
        return None if __attr is None else conf[__attr]


    def set_attr_value(self, conf, attr, value):
        """
        Set value for an attribute in item configuration

        :param conf: item configuration
        :param attr: attribute name
        :param value: value to set the atteibute to
        :type conf: str
        :type attr: str
        :type value: str
        """
        __attr = self.__get_iattr_conf(conf, attr)
        if __attr is not None:
            conf[self.__get_iattr(attr)] = value


    def __new__(cls, *args, **kargs):
        """
        This method ic called during the creation of an object of the class SmartPlugin.

        It tests, if PLUGIN_VERSION is defined.
        """
        if not hasattr(cls,'PLUGIN_VERSION'):
            raise NotImplementedError("'Plugin' subclasses should have a 'PLUGIN_VERSION' attribute")
        return SmartObject.__new__(cls,*args,**kargs)


    def get_sh(self):
        """
        Return the main object of smarthomeNG (usually refered to as **smarthome** or **sh**)
        You can reference the main object of SmartHomeNG by using self.get_sh() in your plugin
        
        :note: Only available in SmartHomeNG versions **beyond** v1.3

        :return: the main object of smarthomeNG (usually refered to as **smarthome** or **sh**)
        :rtype: object
        """
        return self._sh


    def _set_sh(self, smarthome):
        """
        Set the object's local variable `_sh` to the main smarthomeNG object.
        You can reference the main object of SmartHomeNG by using self._sh.
        
        :Note: **Usually you don't need to call this method**, since it is called during loading of the plugin
        
        :param smarthome: the main object of smarthomeNG
        :type smarthome: object
        """
        self._sh = smarthome


    def get_module(self, modulename):
        """
        Test if module http is loaded and if loaded, return a handle to the module
        """
        try:
            mymod = self.get_sh().get_module(modulename)
        except:
             mymod = None
        if mymod == None:
            self.logger.error("Plugin '{}': Module '{}' not loaded".format(self.get_shortname(), modulename))
        else:
            self.logger.warning("Plugin '{}': Using module '{}'".format(self.get_shortname(), str( mymod.shortname ) ) )
        return mymod
        

    def path_join(self, path, dir):
        """
        Join an existing path and a directory
        """
        return os.path.join( path, dir )


    def parse_logic(self, logic):
        """
        This method is used to parse the configuration of a logic for this plugin. It is
        called for all plugins before the plugins are started (calling all run methods).
        
        :note: This method should to be overwritten by the plugin implementation.
        """
        pass


    def parse_item(self, item):
        """
        This method is used to parse the configuration of an item for this plugin. It is
        called for all plugins before the plugins are started (calling all run methods).
        
        :note: This method should to be overwritten by the plugin implementation.
        """
        pass


    def run(self):
        """
        This method of the plugin is called to start the plugin
        
        :note: This method needs to be overwritten by the plugin implementation. Otherwise an error will be raised
        """
        raise NotImplementedError("'Plugin' subclasses should have a 'run()' method")


    def stop(self):
        """
        This method of the plugin is called to stop the plugin when SmartHomeNG shuts down
        
        :note: This method needs to be overwritten by the plugin implementation. Otherwise an error will be raised
        """
        raise NotImplementedError("'Plugin' subclasses should have a 'stop()' method")
        
