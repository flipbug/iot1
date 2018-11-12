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


    File:          RotaryResource.py
    

    Purpose:       Derived class from the
                   sensor class that
                   implements the concrete
                   behaviour of a GrovePi
                   rotary angle sensor.

                   Class is based on
                   the abstract sensor
                   class.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - the GrovePi module has
                     to be installed to 
                     interact with the GrovePi
                     hardware.

                   - A sensor can have atuators.
                     Those can be notified if
                     the state/value of a sensor
                     changes.

                     The idea is based on the
                     observer pattern.

                   - A sensor has a list of
                     actuator uris (coap://...)
                     wich are going
                     to be notified if the
                     state of a sensor value
                     changes.
    

    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          09/2016

'''

import asyncio

import aiocoap
import aiocoap.resource as resource

import grovepi

from Sensor import Sensor

class RotaryResource( Sensor ):
  
  def __init__( self, connector, loop, logger ):
    super( RotaryResource, self ).__init__( connector, loop, logger )
    
	  # set Contenttype to text/plain
    self.ct = int( 0 )
    self.value = False
    self.potentiometer = connector
    self.actuator_uris = [ "coap://localhost:5683/actuators/led0",
                           "coap://172.16.32.81:5683/actuators/led0" ] # sjossi
    self.actuator_uris = [ "coap://localhost:5683/actuators/led0"]

    self.poll_sensor()


  def __enter__( self ):
    pass


  def __exit__( self, exc_type, exc_value, traceback ):
    pass

  
  def read_sensor( self ):
    grovepi.pinMode(self.potentiometer, "INPUT")
    new_value = bool(False)

    try:
      new_value = grovepi.analogRead(self.potentiometer)

      # Reference voltage of ADC is 5v
      adc_ref = 5
      # Vcc of the grove interface is normally 5v
      grove_vcc = 5
      # Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
      full_angle = 300
      # Calculate voltage
      voltage = round((float)(new_value) * adc_ref / 1023, 2)
      # Calculate rotation in degrees (0 to 300)
      degrees = round((voltage * full_angle) / grove_vcc, 2)
      # Calculate LED brightess (0 to 255) from degrees (0 to 300)
      brightness = int(degrees / full_angle * 255)

      new_value = brightness

      #self.logger.debug("DP READ SENSOR ROTARY, value:")
      #self.logger.debug(new_value)

      #self.logger.debug("DP READ SENSOR ROTARY, brightness:")
      #self.logger.debug(brightness)
    except IOError:
      self.logger.debug( "Error in reading sensor at pin " + str( self.connector ) )

    if not self.is_equal( self.value, new_value ):
      self.value = new_value
      self.notify_all_actuators()
      self.updated_state()
      self.logger.debug( "------------------read_sensor called in  instance" )


  def is_equal( self, a, b ):
    return a == b


  def notify_all_actuators( self ):
    for act_uri in self.actuator_uris:
      asyncio.async( self.notify_actuator( act_uri ), loop = self.loop )

  @asyncio.coroutine
  def notify_actuator( self, act_uri ):
    self.logger.debug("------------------notify called----------------------------------")
    payload = str( self.value ).encode( 'ascii' )
    #self.logger.debug("****** DP, payload: [" + str(payload) + "]")
    request = aiocoap.Message( code = aiocoap.PUT, payload = payload )
    actuator_context = yield from aiocoap.Context.create_client_context()
    request.set_request_uri( act_uri )

    response = yield from actuator_context.request( request ).response
