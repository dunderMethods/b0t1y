# B0t1y – The Real Coding Robot

**By:** DunderMethods

## Overview

Introducing **B0t1y**, a Python library designed to control the Botley 2.0 Coding Robot using *actual* programming commands. This project, initiated as a hardware hacking endeavor, aims to replicate the functionalities of the physical Botley remote through Python method calls, enabling more advanced and customizable interactions with the robot.

## Project Status

Please note, this project was last updated in April 2022 and has not been actively maintained since. Despite this, the codebase is thoroughly commented, and extensive notes are provided to assist in understanding and potential further development.

## Inspiration

The project was inspired by the desire to enhance Botley 2.0 by allowing control via a real programming language. The goal was to emulate the Botley remote's functionality, enabling users to issue commands like moving forward, turning, and more through Python scripts.

## Technical Details

The core challenge addressed was reverse-engineering the proprietary infrared (IR) protocol used for communication between Botley and its remote. This endeavor marked my first experience with IR protocols, and I've included all my raw notes and findings within this repository for reference.

The primary component of the project is the `B0t1yRemote` class. By instantiating this class, users can simulate the physical remote's button presses programmatically. For example:


```python
botley = B0t1yRemote()
botley.move('f')  # Adds a single forward move to the command queue
```


The `moves` method allows for queuing a series of commands:


```python
botley.moves('f, f, l90, f, f, l45, b, b')
```


These commands correspond to Botley's movements, such as moving forward ('f'), turning left 90 degrees ('l90'), moving backward ('b'), and so on.

## Hardware Setup

Initially, the aim was to utilize a cost-effective USB IR blaster for transmitting commands. However, due to low-level interfacing challenges, the implementation was successfully achieved using a Raspberry Pi 4 Model B, leveraging its GPIO pins connected to an IR LED. While this setup was not extensively documented, it should be straightforward to replicate for those familiar with Raspberry Pi configurations. I believe I also had it working on windows, using an Arduino Uno with an IR LED.

## Getting Started

To explore or contribute to this project:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dunderMethods/b0t1y.git
   ```


2. **Review the Code and Notes:**

   Delve into the commented code and accompanying notes to understand the implementation details and the reverse-engineering process of the IR protocol.

3. **Set Up the Hardware:**

   If you wish to test or extend the functionality, set up a Raspberry Pi with an IR LED as described. Ensure you have the necessary libraries and permissions to control the GPIO pins.

## Contributing

Given the project's inactive status since 2022, contributions are highly encouraged to breathe new life into it. Whether it's enhancing the existing code, improving documentation, or adapting it for other platforms, your input is welcome.

## Contact

If you have questions or need assistance, feel free to reach out. While my involvement with the project has been dormant, I'm open to providing insights or guidance where possible.

*Happy coding with B0t1y!* 