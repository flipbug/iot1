#!/usr/bin/env python3

import log
from Actuator import Actuator

from grove_pi_interface import InteractorMember, \
                               ANALOG_WRITE

class LedPotentiometerResource( Actuator ):

  def __init__( self, connector, mqtt_client, \
                sub_topic, \
                nuances_resolution ):
    
    super( LedPotentiometerResource, self ).__init__( connector, mqtt_client, \
                                         sub_topic, nuances_resolution )
    
    self.logger = log.setup_custom_logger( "mqtt_thing_led_resource" )
    self.grovepi_interactor_member = InteractorMember( connector, \
                                                       'OUTPUT', \
                                                       ANALOG_WRITE )

    self.value = 0

    self.grovepi_interactor_member.tx_queue.put( \
        ( self.grovepi_interactor_member, int( self.value ) ) )

  def on_mqtt_message( self, client, userdata, message ):
    self.logger.debug( "Got message on topic: " + str( message.topic ) )
    payload = int(message.payload)

    new_value = int(payload / 1024 * 255)
    
    if new_value != self.value:
      self.logger.debug(new_value)
      self.value = new_value

      self.grovepi_interactor_member.tx_queue.put( \
          ( self.grovepi_interactor_member, self.value ) )

  def tear_down( self ):
    self.logger.debug( "tearing things down ..." )
    self.set_actuator( int( 0 ) )
