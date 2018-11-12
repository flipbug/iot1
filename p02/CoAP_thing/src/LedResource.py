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


    File:          LedResource.py
    

    Purpose:       Concrete implementation
                   class for a GrovePi
                   LED with digital output.

                   Class is based on
                   the abstract actuator
                   class.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - Actuators get notified
                     from sensors. Therefore
                     the input from the sensors
                     has to be parsed and verified,
                     according the needs
                     of the required parameters
                     between concrete sensors
                     and actuators.

                   - If the main program terminates
                     (Exception / Key stroke / ...)
                     an actuator has to be brought
                     into a save off state
                     e.g. all outputs to low, ...

                     Therefore the __exit__
                     function MUST be implemented
                     in each concrete actuator
                     implementation.
    

    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          09/2016

'''

import aiocoap
import aiocoap.resource as resource
import asyncio

import grovepi

from Actuator import Actuator

class LedResource( Actuator ):

  def __init__( self, connector, logger, nuances_resolution ):
    super( LedResource, self ).__init__( connector, logger, nuances_resolution )
		
    #set Contenttype to text/plain
    self.ct = 0
    self.value = 0
    self.button_pressed = False

    try:
      grovepi.analogWrite( self.connector, int( self.value ) )
    except IOError:
      self.logger.debug( "Error of initial digitalWrite call." )
 

  def __enter__( self ):
    pass
 

  def __exit__( self, exc_type, exc_value, traceback ):
    self.logger.debug( "tearing things down ..." )
    self.set_actuator( int( 0 ) )


  def set_actuator( self, value ):
    try:
      if self.button_pressed:
        grovepi.analogWrite(self.connector, self.value)
      else:
        # The button is not pressed but we've received a new value through
        # the RotaryResource.
        # Simply disable the LED in this case.
        grovepi.analogWrite(self.connector, 0)

      self.updated_state()
      self.logger.debug("****** DP **** set_actuator with value: [" + str(self.value) + "]")
    except IOError:
      self.logger.debug( "Error in writing to sensor at pin " + str( self.connector ) )


  def var_to_int( self, var_to_cast ):
    # If the payload is a string or boolean, the button has been pressed.
    # We already saved the button state in the input_valid method.
    # Therefor there is not need to update the value.
    if not isinstance(var_to_cast, int):
      return self.value

    return int(var_to_cast)


  def is_equal( self, a, b ):
    return a == b


  def input_valid( self, input ):
    if input == "True":
      self.button_pressed = True
      return True

    if input == "False":
      self.button_pressed = False
      return True

    if isinstance(input, int):
        self.value = int(input)
        return True

    if input.isdigit():
        self.value = int(input)
        return True

    return False


  @asyncio.coroutine
  def render_get( self, request ):
    payload = ( str( self.value ) + "\n" ).encode( 'ascii' )
    response = aiocoap.Message( code = aiocoap.CONTENT, payload = payload )
    response.opt.content_format = self.ct
    return response


  @asyncio.coroutine
  def render_put( self, request ):
    payload = request.payload.decode( 'ascii', 'strict' )

    #self.logger.debug("****** DP ******** render_put with value: [" + payload + "]")

    if self.input_valid( payload ):
      #self.logger.debug("****** DP ******** input valid")
      new_value = self.var_to_int( payload )

      if not self.is_equal( new_value, self.value ) or new_value == "True" or new_value == "False" or True:
        self.value = new_value
        self.set_actuator( new_value )
        #self.logger.debug("****** DP ******** SETTING NEW VALUE")
      #else:
        #self.logger.debug("****** DP ******** i am not calling set_actuator")
			
      response = aiocoap.Message( code = aiocoap.CHANGED, \
                 payload = "request payload was valid\n".encode( 'ascii' ) )

    else:
      #self.logger.debug("****** DP ******** input INVALID!")
      response = aiocoap.Message( code = aiocoap.BAD_REQUEST, \
                 payload = "resource only supports True or False as payload\n".encode( 'ascii' ) )

    response.opt.content_format = self.ct
		
    return response

