#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#include <SoftwareSerial.h>

#define NUMPIXELS 56
#define PIN 8

SoftwareSerial Bluetooth(10,9);

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

void setup() {
  Serial.begin(9600);
  Bluetooth.begin(9600);
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code

  strip.setBrightness(130);
  strip.begin();
  rainbowCycle(50);
  strip.show(); // Initialize all pixels to 'off'
}

char user = 'n';

void loop() {
  // Initialize the input to ""
  user = 'n';
  String value = "";
  if (Bluetooth.available()) {
    user = Bluetooth.read();
    Serial.println(user);
  }
  if (Serial.available()) {
    value = Serial.readString();
    if (value == "y") {
      dispensed();
    }
  }
  if (user == '!') {
    strip.setBrightness(0);
    strip.show();
  }
  if (user == ',') {
    strip.setBrightness(26);
    strip.show();
  }
  if (user == '#') {
    strip.setBrightness(52);
    strip.show();
  }
  if (user == '$') {
    strip.setBrightness(78);
    strip.show();
  }
  if (user == '%') {
    strip.setBrightness(104);
    strip.show();
  }
  if (user == '&') {
    strip.setBrightness(130);
    strip.show();
  }
  if (user == '/') {
    strip.setBrightness(156);
    strip.show();
  }
  if (user == '(') {
    strip.setBrightness(182);
    strip.show();
  }
  if (user == ')') {
    strip.setBrightness(208);
    strip.show();
  }
  if (user == '*') {
    strip.setBrightness(234);
    strip.show();
  }
  if (user == '+') {
    strip.setBrightness(255);
    strip.show();
  }
  
  if (user == '1') {
    while(user == '1'){
      rainbowCycle(50);
    }
  }
  if (user == '2') {
    while(user =='2') {
      colorWipe(strip.Color(255, 0, 0), 50); // Red
      colorWipe(strip.Color(0, 255, 0), 50); // Green
      colorWipe(strip.Color(0, 0, 255), 50); // Blue
    }
  }
  if (user == '3') {
    while(user == '3') {
      theaterChase(strip.Color(127, 127, 127), 50); // White
      theaterChase(strip.Color(127, 0, 0), 50); // Red
      theaterChase(strip.Color(0, 0, 127), 50); // Blue
    }
  }
  if (user == '4') {
    theaterChaseRainbow(50);
  }
  if (user == 'r') {
    colorchange(255, 0, 0);
  }
  if (user == 'o') {
    colorchange(255, 127, 0);
  }
  if (user == 'e') {
    colorchange(255, 255, 0);
  }
  if (user == 'g') {
    colorchange(0, 255, 0);
  }
  if (user == 'b') {
    colorchange(0, 0, 255);
  }
  if (user == 'i') {
    colorchange(75, 0, 130);
  }
  if (user == 'v') {
    colorchange(148, 0, 211);
  }
}

void dispensed() {
  for (int j = 0; j < 20; j++) {
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, 255, 0, 0);
    }
    strip.show();
    delay(100);
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
    delay(100);
  }
}

void colorchange(int r, int g, int b) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    if (Bluetooth.available()) {
      user = Bluetooth.read();
    }
    if (user != '2') break;
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256; j++) {
    for (i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on wheel
    for (i = 0; i < strip.numPixels(); i++) {
      if (Bluetooth.available()) {
        user = Bluetooth.read();
      }
      if (user != '1') break;
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    if (user != '1') break;
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j = 0; j < 10; j++) { //do 10 cycles of chasing
      if (Bluetooth.available()) {
        user = Bluetooth.read();
      }
      if (user != '3') break;
    for (int q = 0; q < 3; q++) {
      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, c);  //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, 0);      //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j = 0; j < 256; j++) {   // cycle all 256 colors in the wheel
      if (Bluetooth.available()) {
        user = Bluetooth.read();
      }
      if (user != '4') break;
    for (int q = 0; q < 3; q++) {
      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, Wheel( (i + j) % 255)); //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
        strip.setPixelColor(i + q, 0);      //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
