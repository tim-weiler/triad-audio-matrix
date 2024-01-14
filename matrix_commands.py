
# These all copied from the Triad AMS 16 driver
# Only setOutputToInput and setOutputVolume are implemented
# TODO: implement getOutputSource and getOutputVolume so when HA starts they can be read from the audio matrix

# Power / Network
############################- Power / Network ############################
# powerOn =        "FF 55 02 01 01"     # OK
# powerOff =       "FF 55 02 01 02"     # OK, but unused due to turnon delay, also messes digital connections, requires physically rebooting...
# powerToggle =    "FF 55 02 01 03"     # Unknown, probably same...
# getPowerStatus = "FF 55 03 01 01 F5"  # Not Working in 1.0042 (what is parameter 01-03 for?)

# factoryReset =   "FF 55 02 0B B0"     # OK
# reboot =         "FF 55 03 06 B4 00"  # OK from 1.0047

# getCredentials = "FF 56 03 06 02 F5"  # OK from 1.0047
# # setCredentials is a method, as it can't be sent without calculation of length...

# networkStandbyOn  = "FF 55 03 08 83 01"  # OK, unused
# networkStandbyOff = "FF 55 03 08 83 00"  # OK, sent on net connect
# getMACAddress     = "FF 55 03 08 80 F5"


###########################- Input Gain / Delay ###########################-
# setInputGain = "FF 55 04 02 04" # format is FF55040204 + XX[input] + XX[gain val 00-18]
# getInputGain = "FF 55 04 02 04 F5" # format is FF55040204F5 + XX[input]
# setInputDelay = "FF 56 04 02 04" # format is FF 56 04 02 04 chn dly
# getInputDelay = "FF 56 04 02 04 F5"


############################# Output Delay #############################
# setOutputDelay = "FF 56 04 03 09" # format is FF 56 04 03 09 chn dly
# getOutputDelay = "FF 56 04 03 09 F5"


############################# Stereo / Mono (OLD) ############################-
# setOutputStereo = "FF 55 03 03 10" # format is FF55030310 + XX[output]
# getMonoStereo   = "FF 55 04 03 10 F5"
# setOutputMono   = "FF 55 03 03 11" # format is FF55030311 + XX[output]
# #toggleOutputMono = "FF 55 03 03 12" # Unused

############################# NEW OUTPUT MODES / CROSSOVER SETTINGS ############################-

# setOutputMode = "ff 56 04 03 0b" # format is FF5604030B + XX[output] + MM[mode]
# getOutputMode = "ff 56 04 03 0b F5"
#OUTPUT_MODES = { Stereo: 1, Mono : 2, ["DSP Bypass Stereo"] = 0, Test = 5, ["2.1 Stereo"] = 3, ["2.1 Mono"] = 4 }

# setOutputTestToneVolume = "ff 56 04 04 01" # format is FF56040401 + XX[output] + Test Volume (0-48 -24 -> 0, .5 steps)

# setCrossoverFrequency = "FF 56 07 03 05" # FF56070305 + CC + vv vv vv vv (4 byte freq value)
# getCrossoverFrequency = "FF 56 07 03 05 F5"

# setCrossoverType = "FF 56 04 03 06" # FF56070305 + CC + VV (0-6 from table)
# # CROSSOVER_TYPE = {}
# # CROSSOVER_TYPE["Butterworth 12 dB"] = 0
# # CROSSOVER_TYPE["Butterworth 24 dB"] = 1
# # CROSSOVER_TYPE["Butterworth 48 dB"] = 2
# # CROSSOVER_TYPE["Linkwitz-Riley 12 dB"] = 3
# # CROSSOVER_TYPE["Linkwitz-Riley 24 dB"] = 4
# # CROSSOVER_TYPE["Linkwitz-Riley 48 dB"] = 5
# getCrossoverType = "FF 56 04 03 06 F5"

# setSubVolumeOffset = "FF 56 04 03 07" # FF56040307 + CC + VV (1 byte gain value)
# getSubVolumeOffset = "FF 56 04 03 07 F5"


############################ Source Selection ############################
setOutputToInput = bytearray.fromhex("FF5504031D")  # format is FF5504031D + XX[output] + XX[input]
getOutputSource =  bytearray.fromhex("FF5504031DF5")

# # Same command as setOutputToInput, setting input value as #inputs + 1 does disconnect
# disconnectOutput = "FF 55 04 03 1D" # format is FF5504031D + XX[output] + XX (BYTE(8) or BYTE(16) indicates 'disconnect output')


# ############################# Volume / Mute ############################-
setOutputVolume = bytearray.fromhex("FF5504031E") # format is FF5504031E + XX[output] + XX[val 00-A1, 00 is off, A1 if full on]
getOutputVolume = bytearray.fromhex("FF5504031EF5")
# setOutputMaxVol = "FF 55 04 03 1F" # format is FF5503031F + XX[output] + XX[value 00-A1]
# getOutputMaxVol = "FF 55 04 03 1F F5"
# setOutputStartVol = "FF 55 04 03 33" # format is FF55040333 + XX[output] + XX[value 00-A1]
# getOutputStartVol = "FF 55 04 03 33 F5"

# setOutputMuteOn = "FF 55 03 03 17" # format is FF55030317 + XX[output]
# setOutputMuteOff = "FF 55 03 03 18" # format is FF55030318 + XX[output]
# getMuteStatus = "FF 55 04 03 17 F5"
# #setOutputMuteToggle = "FF 55 03 03 19" # Unused

# #setOutputVolUp = "FF 55 03 03 13" # Unused
# #setOutputVolDown = "FF 55 03 03 14" # Unused
# #setOutputVolUp3 = "FF 55 03 03 15" # Unused
# #setOutputVolDown3 = "FF 55 03 03 16" # Unused


# #######################- Bass / Treble / Balance / Loudness #######################-
# # OLD Bass (Low Shelf) Commands:
# setOutputBass =    "FF 55 04 03 2F" # format is FF5504032F + XX[output] + XX[value 00-30, 00 is -12db, 30 is +12db, 18 is 0db]
# getOutputBass =    "FF 55 04 03 2F F5"
# # NEW Low Shelf Commands:
# setLowShelf_Freq = "FF 56 07 03 03"
# getLowShelf_Freq = "FF 56 04 03 03 F5"
# setLowShelf_Gain = "FF 56 07 03 0D"
# getLowShelf_Gain = "FF 56 07 03 0D F5"
# setLowShelf_Q    = "FF 56 07 03 04"
# getLowShelf_Q    = "FF 56 07 03 04 F5"

# # OLD Treble (High Shelf) Commands:
# setOutputTreble =  "FF 55 04 03 30" # format is FF55040330 + XX[output] + XX[value 00-30, 00 is -12db, 30 is +12db, 18 is 0db]
# getOutputTreble =  "FF 55 04 03 30 F5"
# # NEW High Shelf Commands:
# setHighShelf_Freq = "FF 56 07 03 01"
# getHighShelf_Freq = "FF 56 07 03 01 F5"
# setHighShelf_Gain = "FF 56 07 03 0C"
# getHighShelf_Gain = "FF 56 07 03 0C F5"
# setHighShelf_Q    = "FF 56 07 03 02"
# getHighShelf_Q    = "FF 56 04 03 02 F5"

# setOutputBalance = "FF 55 04 03 31" # format is FF55040331 + XX[output] + XX[value 00-30, 00 is -12db left, 30 is +12db right, 18 is center]
# getOutputBalance = "FF 55 04 03 31 F5"

# setOutputLoudnessOn =  "FF 55 03 03 1A" # format is FF5503031A + XX[output]
# getOutputLoudness =    "FF 55 04 03 1A F5"
# setOutputLoudnessOff = "FF 55 03 03 1B" # format is FF5503031B + XX[output]
# #setOutputLoudnessToggle = "FF 55 03 03 1C" # Unused