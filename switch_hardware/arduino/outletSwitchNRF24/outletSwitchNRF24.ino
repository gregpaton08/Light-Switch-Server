#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

// nrf24l01 to Arduino Pro Mini pinout
// =======        ========
// Arduino        nrf24l01
// =======        ========
// Pin 1 GND  ->  GND
// Pin 2 VCC  ->  VCC
// Pin 2 CE   ->  Pin 9
// Pin 4 CSN  ->  Pin 10
// Pin 5 SCK  ->  Pin 13
// Pin 6 MOSI ->  Pin 11
// Pin 7 MISO ->  Pin 12
// Pin 8 IRQ  ->  Pin 7


// IRQ is pin 7
const uint8_t irqPin = 7;

// Set up nRF24L01 radio on SPI bus plus pins for chip enable and chip select.
// Pin 9  - chip enable
// Pin 10 - chip select
RF24 radio(9, 10);

// Radio pipe addresses for the 2 nodes to communicate.
const uint64_t writingPipe = 0xF0F0F0F0E1LL;
const uint64_t readingPipe = 0xF0F0F0F0D2LL;

//
// Payload
//

const int max_payload_size = 32;
char receive_payload[max_payload_size + 1]; // +1 to allow room for a terminating NULL char

const uint8_t relayPin = 8; // Setting to HIGH turns switch off, setting to LOW turns switch on.

void setup(void)
{
  radio.begin();

  // enable dynamic payloads
  radio.enableDynamicPayloads();

  // optionally, increase the delay between retries & # of retries
  radio.setRetries(5, 15);

  radio.openReadingPipe(1, readingPipe);
  radio.openWritingPipe(writingPipe);

  radio.startListening();
  radio.printDetails();

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  pinMode(irqPin, INPUT);
}

void loop(void)
{
  while (radio.available())
  {
    // Fetch the payload, and see if this was the last one.
    uint8_t len = radio.getDynamicPayloadSize();
    
    // If a corrupt dynamic payload is received, it will be flushed.
    if (!len) {
      continue; 
    }
    
    radio.read(receive_payload, len);

    switch (receive_payload[0]) {
      case '0':
        digitalWrite(relayPin, HIGH);
        break;
      case '1':
        digitalWrite(relayPin, LOW);
        break;
      case '2':
        if (digitalRead(relayPin) == HIGH) {
          receive_payload[0] = '0';
        } else {
          receive_payload[0] = '1';
        }
        break;
      default:
        break;
    }

    // Send the response back
    radio.stopListening();
    radio.write(receive_payload, len);
    radio.startListening();
  }
}
