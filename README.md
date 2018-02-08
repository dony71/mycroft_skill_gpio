## Raspberry Pi GPIO Demo
Example of interacting with GPIO on a Raspberry Pi

## Description 
Demonstrates interacting with Raspberry Pi GPIO with a Mycroft skill.  This explores both reading from a GPIO port (detecting a pushbutton) and writing to it (illuminating an LED).

## Examples 
* "Turn LED on "
* "Turn LED off"
* "Blink LED"
* "LED status"

## Credits 
@amcgee7
Mycroft AI

## Require 
platform_mark1 platform_picroft 

## Exclude 
platform_plasmoid 

## Documentation

### Generation

The documentation is done by Sphinx with some of it in the code.  The following will generate the html docs.

```make docs```

You can then find the generated html in ```docs/build/html/index.html```.  Open that file in your browser and you should be able to navigate the docs.

## Installing
Change the Makefile IP address for the RPi installation.  Also create the folder ```/opt/mycroft/skills/skill-gpio``` on the RPi for the installer.

```make install.pi```

## Testing

```make test.pi```

This will run a test to be sure you have access to the gpio be sure to test on the system in a simular manner as mycroft.

## Notes

If the blinking is too fast it will be impossible to get a command in edgewise because of the voice responce to the led turning on and off during blinking.

## Circuit
For now, use the below image as a guide to the circuit.
![](https://github.com/MycroftAI/picroft_example_skill_gpio/blob/master/IMG_20170706_153744.jpg)
