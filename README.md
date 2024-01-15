# Triad Audio Matrix Amp [[Home Assistant](https://www.home-assistant.io/) Component]

#### Installation

To install, simply copy the triad-audio-matrix folder into your CUSTOM_COMPONENTS folder and restart Home Assistant.

#### Component Configuration
```yaml
# Example configuration.yaml entry
media_player:
  - platform: triad-audio-matrix
    name: "Living Room"
    host: "192.168.1.1"
    port: 52000
    channel: 1
    source_list:
      - name: "Dad's Spotify" # name to show in the media player source list
        input: 1 # matrix input channel
        spotify_id: "media_player.spotify_dad" # optional, only if the source is a spotify media player
      - name: "Mom's Spotify"
        input: 2
        spotify_id: "media_player.spotify_mom"
````
### Available configuration parameters
* **platform** (Required): Name of a platform
* **host** (Required):  IP address of a Triad Audio Matrix
* **port**(Optional): port of audio matrix. Defaults to 52000
* **channel** (Required): Output channel of the matrix

* **source_list** (Optional): List of source names in source order (e.g., first name = source 1 on amp, second name = source 2 on amp)
