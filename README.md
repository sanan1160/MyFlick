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
   1. Enabling more gestures reduces the accuracy of gesture recognition. In my testing for example, enabling doubles made it        hard to detect normal flicks.
   2. Hold seems to be the most reliable gesture recognized as flicks seem to have a speed requirement.
   3. When hold is detected after 3 seconds, presence is detected after the next second. This results in two consecutive             recognitions. So i disabled hold in order to use presence. However, the detection from the board returns a hold instead        of a presence.
   4. The flick-demo has to be adjusted to account for three arguments to @flicklib.flick()
      def flick(i_type,start,finish):

3. Enabled auto calibration.  The original flicklib had auto calibration disabled, resulting in ghost gesture detections.
4. Added recalibrate method. In my testing, a recalibration every minute seemed optimal. But I have my flick board in front of the TV set where the EM field might be continually changing.
5. I ran into seemingly random GPIO busy errors so I modifed flicklib to swallow the errors in _read_msg(len=132) and  def i2c_read(len).
6. The default configuration for the patched flicklib only enables: Flick: garbage, presence(returned as hold), flick east-west, flick west-east, flick north-south, flick south-north, airwheel CW, airwheel CCW.

MyFlick - Gesture control for Kodi 
1. Due to the ability of setting the state of video playback to pause or play, combinations are now possible where you use hold to pause/play and use this as a condition for another action: For example, hold to pause, then flick north can be assigned to a different action or action combo based on wether playback is in pause or play.
2. A ack_beep or acknowledge beep lets me know if a gesture is recognized which is mostly important for hold gesture. A ready_beep informs me that the script is ready for another recognition. The ack_beep does not guarantee execute of the gesture.
3. By evaluating the value of Z, you can further qualify hold as hover high or hover low, allowing two assignable actions.
4. Its best to presynthesize the speech files into wav files to cut down on cpu processing
5. The garbage model is useful only for waking up the screen as it will occur whenever there is electromagnetic noise on top of the board so I assigned it to pressing Backspace as I don't know of any more direct way of turning off the screensaver on an as needed basis.
6. A recalibration every 60 seconds seems optimal in my setup.
7. A shutdown sequence is implemented to shutdown the raspberry pi.  This is done by performing a certain amount of Left Airwheel and then Right airwheel while video is paused. Unpausing cancels the shutdown.
8. Process priority is adjusted by the script, requiring root privileges. Therefore, a systemd service script is included to start myflick. 

This is a work in progress.  Without patching flicklib, I had to restart my script every 5 minutes with a systemd service becuase it was either detecting ghost gestures or it has run into the gpio busy error.  I have run this for a full day now with no issue.  Use at your own risk of course. 

I would like to find out how to set the timeout for hold and presence with an i2c command. So please let me know if you come across this. 
