#!/usr/bin/env python3

'''
                    ___           ___           ___     
        ___        /\__\         /\  \         /\  \    
       /\  \      /::|  |       /::\  \       /::\  \   
       \:\  \    /:|:|  |      /:/\:\  \     /:/\ \  \  
       /::\__\  /:/|:|  |__   /::\~\:\  \   _\:\~\ \  \ 
    __/:/\/__/ /:/ |:| /\__\ /:/\:\ \:\__\ /\ \:\ \ \__\
   /\/:/  /    \/__|:|/:/  / \:\~\:\ \/__/ \:\ \:\ \/__/
   \::/__/         |:/:/  /   \:\ \:\__\    \:\ \:\__\  
    \:\__\         |::/  /     \:\ \/__/     \:\/:/  /  
     \/__/         /:/  /       \:\__\        \::/  /   
                   \/__/         \/__/         \/__/    


    File:          Sensor.py
    

    Purpose:       Base class for all the
                   sensors that are going
                   to be attached to the
                   device ("thing").

                   To observe the state
                   of a sensors value, 
                   a sensor IS A 
                   observable resource.
                   
                   Class is based on
                   observable resource
                   of the aiocoap package.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - Some functions are just
                     abstract in this base
                     class and have to be
                     overridden in the derived
                     class.
    

    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          09/2016

'''

import aiocoap
import aiocoap.resource as resource
import asyncio

import grovepi

class Sensor( resource.ObservableResource ):


  def __init__( self, connector, loop, logger, \
                polling_interval = float( 1.0 ), \
                sampling_resolution = int( 2 ) ):
    
    super( Sensor, self ).__init__()

    self.connector = connector
    self.polling_interval = polling_interval
    self.loop = loop
    self.logger = logger
    self.sampling_resolution = sampling_resolution
		
    grovepi.pinMode( connector, "INPUT" )


  # Function has to be overridden in derived class.
  def __enter__( self ):
    pass


  # Function has to be overridden in derived class.
  def __exit__( self, exc_type, exc_value, traceback ):
    pass


  def poll_sensor( self ):
    self.read_sensor()
    self.loop.call_later( self.polling_interval, self.poll_sensor )


  # Function has to be overridden in derived class.
  def read_sensor( self ):
    pass


  # Function has to be overridden in derived class.
  def is_equal( self, a, b ):
    pass

