# Raspberry Pi 4 Spotify Music Player with Physical Controls

Welcome to our Raspberry Pi Spotify Music Player project! 🎶 This project was developed as part of our class on Embedded Platforms Programming (PROGRAMMATION DE PLATEFORMES EMBARQUÉES), where we learned how to program Raspberry Pis to create cool and practical applications.

### What Does it Do?

This fun little project turns your Raspberry Pi into a music player that interacts with Spotify's API. It features physical controls including buttons, a rotary encoder, and a volume knob, all of which let you control your music effortlessly.

### How Does it Work?

Let's break it down:

1. **SpotifyControls Module**: We've built a module that communicates with Spotify's API. It handles tasks like playing, pausing, skipping tracks, and fetching song information.

2. **LCD Screen**: We've connected an Adafruit Character LCD to the Raspberry Pi. It displays song details like the track name and artist, giving you a visual of what's playing.

3. **Physical Buttons**: Using GPIO pins on the Raspberry Pi, we've set up buttons for play/pause, skip forward, and skip backward functions. Just press a button to control your music!

4. **Rotary Encoder**: We've integrated a rotary encoder that detects clockwise and counterclockwise rotations. Simply twist the knob to switch tracks forward or backward.

5. **Volume Knob**: A potentiometer acts as a volume knob. Turn it to adjust the volume of your music playback.

### How to Set it Up?

Follow these steps:

1. **Hardware Setup**: Connect the LCD screen, buttons, rotary encoder, and volume knob to your Raspberry Pi. We've provided pin configurations in the script for easy setup.

2. **Install Dependencies**: Make sure to install the required Python libraries such as `RPi.GPIO`, `adafruit-blinka`, `adafruit-circuitpython-charlcd`, and `pigpio`.

3. **Get Spotify API Credentials**: Obtain your Spotify API credentials (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI) and store them in a JSON file named `api-secret.json`.

4. **Run the Script**: Execute the Python script on your Raspberry Pi. Once running, you'll be able to control your music using the physical controls!

### Conclusion

With this project, we've combined our knowledge of Raspberry Pi programming with our love for music to create a nifty Spotify music player. Enjoy grooving to your favorite tunes with the convenience of hardware controls! 🎵🎉
