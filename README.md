# MyFlick
Python script for controlling Kodi using a Flick Gesture board
This will require a patch to the flicklib library from https://github.com/PiSupply/Flick.

Flicklib patch includes the following changes:
1. Adds support for all the flicklib gestures (this breaks the flick-demo):
   
   Gestures:
   1. garbage               -> any non recognized gesture or environmental noise trigger, 
   2. wave X                -> move across the board and back in the X axis,
   3. wave Y                -> move across the board and back in the Y axis,
   4. hold                  -> hover over the board for 3 seconds,
   5. presence              -> shows up after hold,
   6. edge west east        -> start past the edge and swipe to the board, covering about 70% of its surface, 
   7. edge east west
   8. edge south north
   9. edge north south
   10. double west east      -> flick twice in the same direction,
   11. double east west
   12. double south north
   13. double north south

   Some caveats:
   1. Enabling more gestures reduces the accuracy of gesture recognition. In my testing for example, enabling doubles made it hard to detect normal flicks.
   2. Hold seems to be the most reliable gesture recognized as flicks seem to have a speed requirement.
   3. When hold is detected after 3 seconds, presence is detected after the next second. This results in two consecutive recognitions. So i disabled hold in order to use presence. However, the detection from the board returns a hold instead        of a presence.
   4. The flick-demo has to be adjusted to account for three arguments to @flicklib.flick()
      def flick(i_type,start,finish):
   

2. Enabled auto calibration.  The original flicklib had auto calibration disabled, resulting in ghost gesture detections.
3. Added recalibrate method. In my testing, a recalibration every minute seemed optimal. But I have my flick board in front of the TV set where the EM field might be continually changing.
4. I ran into seemingly random GPIO busy errors so I modifed flicklib to swallow the errors in _read_msg(len=132) and  def i2c_read(len).
5. The default configuration for the patched flicklib only enables: Flick: garbage, presence(returned as hold), flick east-west, flick west-east, flick north-south, flick south-north, airwheel CW, airwheel CCW.
6. Wrapped the init sequence into an init() procedure and created a reinit() procedure.

MyFlick - Gesture control for Kodi 

1. Due to the ability of setting the state of video playback to pause or play, combinations are now possible where you use hold to pause/play and use this as a condition for another action: For example, hold to pause, then flick north can be assigned to a different action or action combo based on wether playback is in pause or play.
2. A ack_beep or acknowledge beep lets me know if a gesture is recognized which is mostly important for hold gesture. A ready_beep informs me that the script is ready for another recognition. The ack_beep does not guarantee execute of the gesture as the gesture may have been detected too far in the past.
3. By evaluating the value of Z, you can further qualify hold as hover high or hover low, allowing two assignable actions.
4. Its best to presynthesize the speech files into wav files to cut down on cpu processing
5. The garbage model is only useful for waking up the screen as it will occur whenever there is electromagnetic noise on top of the board so I assigned it to pressing Backspace as I don't know of any more direct way of turning off the screensaver on an as needed basis.
6. Automatic self calibration for EM noise. A recalibration every 60 seconds seems optimal in my setup with a max_garbage=4. User can force a recalibration by instantiating garbage detections to a set limit (twiddle your fingers on top of the board a few times).  A long beep is played to warn to remove hand from top of board before recalibration triggered by garbage count.  The garbage count will be cleared at each recalibration (interval or garbage count triggered)  so hopefully the long beep only will serve for user intended recalibrations if interval recalibrations occur frequently enough.  If the garbage count increases to max_garbage due to environmental EM noise, a silent (no longbeep) recalibration will be triggered.   
7. Onboard LEDS ACT and PWR are used as visual cues.  ACT (Green LED) signals readiness for detection. PWR (Red LED) signals WAIT ( execute() running, still within the imposed flick interval). This is unfortunately board specific and my settings are for RPI 3B+. Blinking PWR and ACT means a recalibraion is ongoing. 
8. Process priority is adjusted by the script, requiring root privileges. Therefore, a systemd service script is included to start myflick. 
9. Flick gestures are limited to 1 per flick_interval (1 second) and expired after flick_expire (3 seconds). Execute() will only execute the last flick detection and throw away the earlier ones to avoid queueing. Airwheel has no interval limit but in the general UI, it will be interrupted by speech playback so page up and page down will execute one step at a time. 
10. There is code for sending 12 byte and 16 byte Gestic Library Messages for anyone who wishes to experiment.
11. A logging facility is included. Useful to watch the log with tail -f myflick.log

Tips:

1. Gesture recognition is inaccurate:

   Force a recalibration by increasing garbage_count to max_garbage. Do this by putting the video in pause mode (to mute the video volume) and then twiddling your fingers over the board up to max_garbage times. A softbeep will signal recognition of each garbage gesture, followed by a longbeep if you hit max_garbage.  Hands off the board before the longbeep ends.  Pick a softbeep that is barely audible as garbage detection could happen with extraneous EM noise over the board. One of the possible causes of inacurrate recogniton is silent recalibration at intervals with the hand over the board. Silent recalibrations will have a visual warning by blinking the leds. 

2. Gesture recognition is delayed:

   It might be necessary to reinitialize the board. Go through the first part of the shutdown process (Pause the video. Perform Left Airwheel 10 times).  The board will be reinitialized.  Then unpause the video.  

Hardware and Library Notes:

1. No point in testing the sequence byte in the response message to remove duplicates. It resulted in less accurate flick recognitions.
2. Sometimes, the Flick board is displaying increasing latency between flick detection (when hand swipe ocurred)  and sending the library message response back. Try reinitializing the board by performing the first part of the shutdown routine (pause video, perform 10 Left rotations) and resuming playback.

My RPI is upside down with the HDMI port facing the TV so the compass directions are reversed. 

Kodi Actions Implemented while video is playing:

1. West - Seek 1 minute forward
2. East - Seek 1 minute backward
3. North - Jump 10 minutes backward
4. South - Jump 10 minutes forward
5. Hover Low - Pause
6. Hover High - Create Bookmark
7. Airwheel Left - Volume down
8. Airwheel Right - Volume up


Kodi actions implemted while video is paused:

1. Enable/Disable video timebar and clock - Flick West
2. Enable/Disable subtitles - Flick East
3. Play the Next Video in the Directory - Flick North
4. Exit/Stop video - Flick South
5. Shutdown the Raspberry Pi -  10 Left Airwheel (Stage 1 shutdown) and within 40 seconds followed by 10 Right Airwheel (Stage 2 shutdown). Shutdown will occur in 30 seconds. Cancel shutdown by resuming playback. If 10 Right airwheel did not occur within 40 seconds after 10 Left Airwheel, then the Shutdown sequence is cleared (Stage 0).  
6. Reset the Flick Board - Go through the Shutdown sequence, Wait for the board to initialize,  and unpause the video to Abort Shutdown. 

Kodi actions implemented in the general UI:

1. West - Right
2. East - Left
3. North - Down 1 item
4. South - Up 1 item
5. Hover Low - Select
6. Hover High - Back
7. Airwheel Left - Page Up
8. Airwheel Right - Page Down

This is a work in progress.  Without patching flicklib, I had to restart my script every 5 minutes with a systemd service becuase it was either detecting ghost gestures or it has run into the gpio busy error.  Use at your own risk of course. 

I would like to find out how to set the timeout for hold and presence with an i2c command. So please let me know if you come across this or any other useful i2c commands. 
