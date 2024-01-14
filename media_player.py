""" triad-audio-matrix """

from .triad_matrix import TriadMatrixOutputChannel

import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.components.media_player import (
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState 
)

from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    CONF_NAME,
    STATE_ON,
    STATE_OFF
)

_LOGGER = logging.getLogger(__name__)

#This sets the name used in configuration.yaml
CONF_ON_VOLUME = "on_volume"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_CHANNEL = "channel"
CONF_SOURCE_LIST = "source_list"

DEFAULT_PORT = 52000
DEFAULT_VOLUME = 15

SUPPORT_TRIAD_AMS = (
    MediaPlayerEntityFeature.VOLUME_SET \
    | MediaPlayerEntityFeature.VOLUME_STEP \
    | MediaPlayerEntityFeature.TURN_ON \
    | MediaPlayerEntityFeature.TURN_OFF \
    | MediaPlayerEntityFeature.SELECT_SOURCE \
    | MediaPlayerEntityFeature.VOLUME_MUTE \
    | MediaPlayerEntityFeature.NEXT_TRACK \
    | MediaPlayerEntityFeature.PLAY \
    | MediaPlayerEntityFeature.PAUSE
    #| MediaPlayerEntityFeature.GROUPING  # future functionality?
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ON_VOLUME, default=DEFAULT_VOLUME): cv.positive_int,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_CHANNEL): cv.positive_int,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_SOURCE_LIST): cv.ensure_list
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
        
    entity_name = config.get(CONF_NAME)
    on_volume = config.get(CONF_ON_VOLUME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    channel = config.get(CONF_CHANNEL)
    source_list = config.get(CONF_SOURCE_LIST)

    async_add_entities([TriadAudioMatrixMediaPlayer(hass, entity_name, on_volume, host, port, channel,source_list)],)

class TriadAudioMatrixMediaPlayer(MediaPlayerEntity):
    #Research at https://developers.home-assistant.io/docs/core/entity/media-player/
    #_attr_device_class = 

    def __init__(self, hass, name, on_volume, host, port, channel,source_list):
        self.hass = hass
        self._domain = __name__.split(".")[-2]
        self._name = name
        self._source = None
        self._source_list = source_list
        self._on_volume = on_volume / 100
        self._mute_volume = on_volume / 100
        self._state = STATE_OFF
        self._available = True
        self._muted = False
        
        self._ampChannel = TriadMatrixOutputChannel(host, port, channel)

    async def async_update(self):
        # Not sure if update(self) is required.
        _LOGGER.warn("update...")

    @property
    def should_poll(self):
        return False

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        return "mdi:speaker"
    
    @property
    def is_volume_muted(self):
        return self._muted

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def source(self):
        if self._source is None:
            return None
        else:
            return self._source["name"]

    @property
    def source_list(self):
        sources = []
        for s in self._source_list:
            sources.append(s["name"])
        return sources

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._ampChannel.volume 

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_TRIAD_AMS

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        if mute:
            self._muted = True
            self._mute_volume = self._ampChannel.volume
            self._ampChannel.volume  = 0 
            #_LOGGER.warn("volume set to  zero to mute")
        else:
            self._muted = False
            self._ampChannel.volume  = self._mute_volume 
            #_LOGGER.warn("volume set to pre-mute level")
        self.schedule_update_ha_state()

    async def async_select_source(self,source):
        for s in self._source_list:
            if s["name"] == source:
                self._source = s
                self._ampChannel.source = int(s["input"])
                if self._source["spotify_id"] is not None:
                    action_data = { "entity_id" : self._source["spotify_id"], "source": self._source["name"] }
                    await self.hass.services.async_call('media_player', 'select_source', action_data, True)
                break
        
        self.schedule_update_ha_state()
        #_LOGGER.warn("Source input is " + str(self._source["input"]))
        #_LOGGER.warn("Source set to " + str(self._source["name"]))

    async def async_turn_on(self):
        #_LOGGER.warn("Turning on...")
        self._ampChannel.volume = self._on_volume
        #result = self._ampChannel.turn_on()
        self._state = STATE_ON
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        #_LOGGER.warn("Turning off...")
        self._ampChannel.volume = 0
        self._ampChannel.source = 0

        # if spotify is playing, pause it        
        if self._source is not None and self._source["spotify_id"] is not None:
            action_data = { "entity_id" :  self._source["spotify_id"]}
            entity = self.hass.states.get(self._source["spotify_id"])
            
            state = entity.attributes['state']
            if entity.state == MediaPlayerState.STATE_PLAYING:
                await self.hass.services.async_call('media_player', 'media_pause', action_data)

        self._source = None
        #result = self._ampChannel.turn_off()
        self._state = STATE_OFF
        self.schedule_update_ha_state()

    async def async_volume_up(self):
        self._ampChannel.volume = self._ampChannel.volume + .02
        self.schedule_update_ha_state()
        #_LOGGER.warn("volume set to " + str(self._ampChannel.volume))

    async def async_volume_down(self):
        self._ampChannel.volume = self._ampChannel.volume - .02
        self.schedule_update_ha_state()
        #_LOGGER.warn("volume set to " + str(self._ampChannel.volume))

    async def async_set_volume_level(self, volume):
        self._ampChannel.volume  = volume 
        self.schedule_update_ha_state()
        #_LOGGER.warn("volume set to " + str(self._ampChannel.volume))

    async def async_media_play_pause(self):
        
        if self._state != STATE_ON:
            await self.async_turn_on()

        if self._source is None:
            if self._source_list is not None and len(self._source_list) > 0:                
                await self.async_turn_on()
                s = self._source_list[0]
                await self.async_select_source(s["name"])
                # give spotify time to select the source, otherwise playing will fail below
                #time.sleep(3)

        if self._source is not None and self._source["spotify_id"] is not None:            
            action_data = { "entity_id" : self._source["spotify_id"] }            
            await self.hass.services.async_call('media_player', 'media_play_pause', action_data)
            self.schedule_update_ha_state()
    
    async def async_media_play(self):

        if self._state != STATE_ON:
            await self.async_turn_on()

        if self._source is None:
            if self._source_list is not None and len(self._source_list) > 0:                
                
                s = self._source_list[0]
                await self.async_select_source(s["name"])
                # give spotify time to select the source, otherwise playing will fail below
                #time.sleep(3)
        if self._source is not None and self._source["spotify_id"] is not None:
            action_data = { "entity_id" : self._source["spotify_id"] }            
            await self.hass.services.async_call('media_player', 'media_play', action_data)
        
            self.schedule_update_ha_state()

    async def async_media_next_track(self):
        if self._source is not None and self._source["spotify_id"] is not None:
            action_data = { "entity_id" : self._source["spotify_id"] }            
            await self.hass.services.async_call('media_player', 'media_next_track', action_data)            
            self.schedule_update_ha_state()
        