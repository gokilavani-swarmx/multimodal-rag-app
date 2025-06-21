## Note

Positioning times stroke model

## 4 Functions and control

## 4.1 3-position control

<!-- image -->

A 3-position signal drives the actuator via connection terminals Y1 or Y2. The required position is transferred to the valve.

<!-- image -->

| 1               | A/D conversion   | A/D conversion         |
|-----------------|------------------|------------------------|
| 3               | functions        | Identification of seat |
| 3               | functions        | Motor control          |
| 3               | functions        | Manual adjustment      |
| Gear train      | Gear train       | Gear train             |
| Manual adjuster | Manual adjuster  | Manual adjuster        |

| Positioning signal      | Stroke actuator                        | Rotary actuator                                          | Control path valve A à AB   | Bypass valve B à  AB   |
|-------------------------|----------------------------------------|----------------------------------------------------------|-----------------------------|------------------------|
| Voltage at Y1           | Actuator's stem extends                | Actuator's spindle turns in clockwise direction          | Opening                     | Closing                |
| Voltage at Y2           | Actuator's stem retracts               | Actuator's spindle turns in counter- clockwise direction | Closing                     | Opening                |
| No voltage at Y1 and Y2 | Actuator's stem maintains the position | Actuator's spindle maintains the position                | Maintains the position      | Maintains the position |

Observe information given in chapter "Acting direction and flow characteristic" on page 44.

Internal control ensures very constant positioning times and determination of the actuator's position.

The specified positioning times refer to the respective nominal stroke / nominal angular rotation. Since the end positions of rotary actuators are inside the actuator, the following remarks refer to stroke actuators.

The resulting effective strokes vary, depending on the type of valve, resulting in shorter or longer actuator positioning times.

Notes

Notes

<!-- image -->

Deviations occur…

- · after several positioning signals Y1 and Y2 in the same direction since the stroke movement starts with a delay of 200 ms. when positioning signals Y1 and Y2 are active for less than 200 ms since the

stroke movement cannot be made in that case.

<!-- image -->

Accurate position feedback is made possible with the help of a potentiometer (page 53).

## 4.1.1 Combination with RVD.. controller for direct domestic hot water distribution by heat exchanger

The design based slow reaction on control signals of SAX31.. and SAX81.. actuators doesn't allow the actuator to react on very short control pulses. Only control pulses with a length greater than 400 ms allow a sufficient reaction.

Especially the direct domestic hot water control does not allow such long control pulses. The specific optimized control loops - equipped with an SIGMAGYR RVD.. controller and Acvatix SQS359.05 actuator- work with pulses down to 40 ms.

SAX31.. and SAX81.. are not able to work with these short pulses. The following table gives alternatives which actuators can be used within these control loops.

| Controller                   | Plant type   | Prefered actuator   | Valve line      | DN        | kvs                   |
|------------------------------|--------------|---------------------|-----------------|-----------|-----------------------|
| RVD130                       | 4 und 5      | SQS35.03            | VVG55..         | DN15 ..25 | 0.25 .. 6.3           |
| RVD135/109                   | 4 und 5      | SQS359.05           | VVG549..        | DN15 ..25 | 0.25 .. 6.3           |
| RVD135/309                   | 4 und 5      | SQS359.54           | VVG549..        | DN15 ..25 | 0.25 .. 6.3           |
| RVD140 RVD144/109            | 4 und 5      | SKD32.21            | VVG41.. VVF53.. | DN15 ..50 | 0.63 .. 40 0.16 .. 40 |
| RVD145/109                   | 4 und 5      | SKD32.21E           |                 | DN15 ..50 | 0.63 .. 40            |
| RVD139                       | 4 und 5      |                     |                 |           | 0.16 .. 40            |
| RVD230                       | x- 4         | SQS35.03            | VVG55..         | DN15 ..25 | 0.25 .. 6.3           |
| RVD235/109                   | x- 4         | SQS359.05           | VVG549..        | DN15 ..25 | 0.25 .. 6.3           |
| RVD250                       | x- 4         | SQS359.54           | VVG549..        | DN15 ..25 | 0.25 .. 6.3           |
| RVD255/109 RVD240            | x- 4         | SKD32.21            | VVG41.. VVF53.. | DN15 ..50 | 0.63 .. 40 0.16 .. 40 |
| RVD245/109 RVD260 RVD265/109 | x- 4         | SKD32.21E           | VVG41.. VVF53.. | DN15 ..50 | 0.63 .. 40 0.16 .. 40 |

.

Notes

## Modulating control

<!-- image -->

The modulating positioning

signal drives the actuator steplessly. The positioning signal range (DC 0...10 V / DC 4...20 mA, 0...1000 Ω ) corresponds in a range (fully closed...fully open,

linear manner to the positioning or 0…100 % stroke).

The actuator is driven via connection terminal Y or forced control Z (page 49). The required stroke / rotation is transferred to the valve's stem / spindle.

| Calibration slot   | Calibration slot                                | Calibration slot   |
|--------------------|-------------------------------------------------|--------------------|
| LED (2 colors)     | LED (2 colors)                                  | 2                  |
| DIL switches       | Changeover of characteristic Positioning signal | 3                  |
| Function module    | Function module                                 | 4                  |
| A/D conversion     | A/D conversion                                  | 5                  |
| Power supply       | Power supply                                    | 6                  |
| Control functions  | Identification of seat                          | 7                  |
| Control functions  | Position control                                | 7                  |
| Control functions  | Motor control                                   | 7                  |
| Control functions  | Detection of foreign bodies                     | 7                  |
| Control functions  | Forced control                                  | 7                  |
| Control functions  | Characteristics function                        | 7                  |
| Brushless DC motor | Brushless DC motor                              | 7                  |
| Gear train         |                                                 | 8 9                |
| Manual adjuster    | Manual adjuster                                 |                    |

| Positioning signal     | Stroke actuator                        | Rotary actuator                                        | Control path valve A à AB   | Bypass valve B à  AB   |
|------------------------|----------------------------------------|--------------------------------------------------------|-----------------------------|------------------------|
| Signal Y, Z increasing | Actuator's stem extends                | Actuator's spindle turns in clockwise direction        | Opening                     | Closing                |
| Signal Y, Z decreasing | Actuator's stem retracts               | Actuator's spindle turns in counterclockwise direction | Closing                     | Opening                |
| Signal Y, Z constant   | Actuator's stem maintains the position | Actuator's spindle maintains the position              | Maintains the position      | Maintains the position |

- · If function module AZX61.1 is used, observe the information given in chapter "Changeover of acting direction" (page 42).
- · Observe the information given in chapter "Acting direction and flow characteristic" on page 44.

<!-- image -->

## DIL switches

## HEX switches

Notes

## 4.3 Function module AZX61.1

<!-- image -->

<!-- image -->

1) Factory setting: All switches set to OFF

|                                          | Acting direction                     | Sequence control   |
|------------------------------------------|--------------------------------------|--------------------|
| Direct acting positioning signal Y or Z  | Sequence control not  active         | OFF 1)             |
| Reverse acting positioning signal Y or Z | Sequence control (signal adaptation) | ON 1)              |

## 4.3.1 Sequence control (signal adaptation)

<!-- image -->

|    | Sequence control                     | Sequence control   |
|----|--------------------------------------|--------------------|
| 1) | Sequence control (signal adaptation) | ON                 |

- 1) Factory setting: All switches set to OFF

<!-- image -->

| Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   | Setting sequence control Rotary switches LO and UP are used to set the starting point or working range of a sequence.   |
|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                         | Position "LO"                                                                                                           |                                                                                                                         | Starting point                                                                                                          | Position "UP"                                                                                                           | Working range                                                                                                           |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 0                                                                                                                       | 0,3 V                                                                                                                   | 0                                                                                                                       |                                                                                                                         |                                                                                                                         | 9,4 V                                                                                                                   |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 1                                                                                                                       | 1 V                                                                                                                     | 1                                                                                                                       |                                                                                                                         |                                                                                                                         |                                                                                                                         | 3 V                                                                                                                     |                                                                                                                         |
|                                                                                                                         | 2                                                                                                                       | 2 V                                                                                                                     | 2                                                                                                                       |                                                                                                                         | 4 V                                                                                                                     |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 3 4                                                                                                                     | 3 V                                                                                                                     | 3                                                                                                                       |                                                                                                                         |                                                                                                                         |                                                                                                                         | 5 V                                                                                                                     |                                                                                                                         |
|                                                                                                                         |                                                                                                                         | 4 V                                                                                                                     |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 5                                                                                                                       | 5 V                                                                                                                     | 4 5                                                                                                                     |                                                                                                                         | 6 V 7 V                                                                                                                 |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         |                                                                                                                         |                                                                                                                         | 6                                                                                                                       |                                                                                                                         | 8 V                                                                                                                     |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 6                                                                                                                       | 6 V                                                                                                                     |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 7                                                                                                                       | 7 V                                                                                                                     | 7                                                                                                                       | 8                                                                                                                       | 9 V                                                                                                                     |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         | 8 9 A D E F                                                                                                             | 8 V 9 V                                                                                                                 | 9 A D E F E E                                                                                                           | F  F F                                                                                                                  | 14 V 16 V                                                                                                               | 10 V                                                                                                                    |                                                                                                                         | C D E F                                                                                                                 |
|                                                                                                                         | 0                                                                                                                       | 10 V 11 V                                                                                                               |                                                                                                                         |                                                                                                                         |                                                                                                                         | 12 V B                                                                                                                  | 20 V 25 V 30 V                                                                                                          |                                                                                                                         |
|                                                                                                                         | B C                                                                                                                     | 2 3 F F F F                                                                                                             | B C 6  7                                                                                                                | E E                                                                                                                     | E E                                                                                                                     | 18 V F                                                                                                                  | 18 V F                                                                                                                  | 18 V F                                                                                                                  |
|                                                                                                                         | LO                                                                                                                      | 12 V 13 V                                                                                                               |                                                                                                                         |                                                                                                                         | E F  E                                                                                                                  |                                                                                                                         |                                                                                                                         | F                                                                                                                       |
|                                                                                                                         |                                                                                                                         | 14 V 15 V                                                                                                               |                                                                                                                         | 8  9                                                                                                                    |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |
|                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         | Invalid HEX switches combinations                                                                                       |                                                                                                                         |                                                                                                                         |                                                                                                                         |                                                                                                                         |

- · Can only be used with voltage input.
- · Maximum input voltage is DC 30 V. If the configuration is invalid, the actuator operates on DC 0…10 V.

## Examples

## DIL switches

## Selecting the acting direction

<!-- image -->

| Legend diagram                         | Positioning signal range               | Position LO                            | Position UP                            | Position feedback U                    |
|----------------------------------------|----------------------------------------|----------------------------------------|----------------------------------------|----------------------------------------|
| A DC 2…10 V                            | 2                                      | 6                                      |                                        | DC 0…10 V                              |
| DC 0…5 V                               | 0                                      | 3                                      | DC 0…10 V                              | B                                      |
| C DC 12…17 V                           | C                                      | 3                                      | DC 0…10 V                              |                                        |
| Acting direction: Reverse (A', B', C') | Acting direction: Reverse (A', B', C') | Acting direction: Reverse (A', B', C') | Acting direction: Reverse (A', B', C') | Acting direction: Reverse (A', B', C') |

## 4.3.2 Changeover of acting direction

<!-- image -->

| Acting direction   | Acting direction                        | Acting direction   | Acting direction                         |
|--------------------|-----------------------------------------|--------------------|------------------------------------------|
| OFF 1)             | Direct acting positioning signal Y or Z | ON 1)              | Reverse acting positioning signal Y or Z |

- 1) Factory setting: All switches set to OFF
- · With valves whose stem is extended in the fully closed position, "direct acting" means that the valve is fully closed (0 %) when positioning signal Y = 0 V resp. Z = 0 Ω . This applies to all Siemens valves according to "Equipment combinations" (page 10).
- · With valves whose stem is retracted in the fully closed position, "direct acting" means that the valve is fully open (100 %) when positioning signal Y = 0 V resp. Z = 0 Ω .

<!-- image -->

<!-- image -->

Flow characteristic SAX61.03 + VVF..

Flow characteristic SAX61P03 + VPF..

## 4.4 Positioning signal and flow characteristic selection

<!-- image -->

| Positioning signal "Y"   | Position feedback "U"   | Flow characteristic     | Flow characteristic   |
|--------------------------|-------------------------|-------------------------|-----------------------|
| DC 0…10 V                | DC 0…10 V               | log = equal- percentage | OFF 1)                |
| DC 4…20 mA               | DC 0…10 V               | lin = linear            | ON                    |

- 1) Factory setting: All DIL switches set to OFF Ω

<!-- image -->

<!-- image -->

## Acting direction and flow characteristic

The selection of changeover of acting direction and characteristic with the DIL switches depends on the type of actuator (with or without fail safe function) and the associated type of valve (valve characteristic, push to open, pull to open).

When the positioning signal increases (DC 0…10 V, DC 4…20 mA, 0...1000 Ω ), the objective is to have the valve's volumetric flow V rising, but to fully open the valve, V = 100 % (NO = normally open), or to fully close it, V = 0 % (NC = normally closed) in the event of a power failure.

<!-- image -->

## 4.6 Position Feedback U

The position feedback U (DC 0...10 V) is always proportional to stroke H of the actuator's stem.

<!-- image -->

|                         | Actuator Positioning signal Y, Z   | Actuator Position feedback U   |
|-------------------------|------------------------------------|--------------------------------|
| log = equal- percentage |                                    |                                |
| lin = linear            |                                    |                                |

<!-- image -->

|                                | Actuator Positioning signal Y, Z   | Actuator Position feedback U   | Actuator Position feedback U   |
|--------------------------------|------------------------------------|--------------------------------|--------------------------------|
| Direct acting                  |                                    |                                |                                |
| Reverse acting                 |                                    |                                |                                |
| Y, Z Positioning signal Stroke | Y, Z Positioning signal Stroke     |                                |                                |
| H U Position feedback          | H U Position feedback              |                                |                                |
| Acting direction: direct       | Acting direction: direct           |                                |                                |
|                                | Acting direction: reverse          |                                |                                |

## 4.7 Position control with ClosedPosition Synchronisation

Within SAX/SAL61.. actuators the position control works based on the HALLsensor pulses from the brushless DC-motor calculating with an internal stroke model calculating the actual position. This kind of control is more accurate and wearless compared with a physical element for position measurement and grants a precise position control with high resolution.

During manual operation the motor is declutched from the geartrain and the internal position control get's not sensor pulses. So real position will deviate from the internally calculated position. As a consequence the position feedback on terminal U is set to '0V' during manual operation.

To grant  - after manual  operation - that real mechanical position and internal position control are matching the SAX61.. does after manual operation an automatic ClosedPosition-Synchronisation.

## 4.7.1 ClosedPosition-Synchronisation

Returned into automatic operation the actuator runs for 0.5.. 2 s into opening direction to grant secure closed-position detection. Then the actuator runs into closed position (seat A-AB in the valve). Reaching the closed position the internal stroke model is synchronized. Positioning signal, position feedback and meachnical position now match perfectly again.

With this function it's granted that the position feedback U - which was zero during manual operation and synchronization - always represents the real mechanical position of the actuator.

After synchronization the actuator follows the control signal again.

Note

Note

<!-- image -->

## 4.7.1.1 Active forced position input on Z

If after return to automatic mode a signal on Z is active (GND, AC/DC 24 V or 0…1000 Ohm) the ClosedPosition-Synchronisation is deactivated as long as the signal on Z remains. After Z is deactivated the ClosedPosition-Synchronisation will be performed.

ClosedPosition-Synchronisation is only automatically activated after manual operation. A power failure does not activate this function automatically, to avoid that all actuators in a section close in parallel.

If the customer likes synchronization also after a power failure he should take care that the plant restarting routine drives the actuator automatically into an end position. This will also synchronies the internal position control and the real position.

## 4.8 Calibration

To match the actuator to production-related mechanical tolerances of the indiv idual valves, accurate positioning and position feedback must be ensured, if calibration is performed when the plant is commissioned (page 33). During commissioning, the actuator detects the valve's end positions and files the exact stroke in its internal memory.

Calibration takes place in the following phases:

- · Actuator drives to H0 (1), valve closes. Detection of upper end position.
- · Actuator drives to H100 (2), valve opens. Detection of lower end position.
- · The detected values are stored (3). Then the actuator follows the positioning signal.

<!-- image -->

- · Observe status indication (LED) during and after calibration (page 52).
- · If the actuator does not detect the second end position within an appropriate stroke range (max. 25 mm), the first end stop will be adopted and the actuator operates with a working range of 20 mm.

## Examples

## Example

## 4.9 Signal priorities

The actuators are controlled via different interlinked positioning signal paths (positioning signal 'Y', forced control input 'Z', manual adjuster). The signal paths are assigned the following priorities:

| Priority    | Description                                                                                                                                                                                         |    |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|
| 1 (highest) | The manual adjuster always has priority 1, thus overriding all signals active at 'Z' or 'Y', independent of whether or not power is applied.                                                        |    |
| 2           | Only SA..61..: As soon as a valid positioning signal is active at input 'Z', the position is determined via positioning signal 'Z' (forced control). Prerequisite: The manual adjuster is not used. | Z  |
| 3 (lowest)  | The position is determined via positioning signal 'Y'. The manual adjuster is not used and on Z there is no active signal.                                                                          | Y  |

| Manual adjuster             | Forced control (Z)   | Positioning signal (Y)   | Stroke actuator                           | Rotary actuator                                                         |
|-----------------------------|----------------------|--------------------------|-------------------------------------------|-------------------------------------------------------------------------|
| Automatic mode              | Not connected        | 5 V                      | Actuator's stem travels to position (50%) | Actuator's spindle travels to position (50%)                            |
| Automatic mode              | G                    | 3 V                      | Actuator's stem extends                   | Actuator's spindle turns in clockwise direction                         |
| Automatic mode              | G0                   | 3 V                      | Actuator's stem retracts                  | Actuator's spindle turns in counter-clockwise direction                 |
| Operated (30%)  and engaged | G                    | 8 V                      | Actuator's stem retracts manual (to 30%)  | Actuator's spindle turns manual in counterclock-wise direction (to 30%) |

Bold printing = positioning signal currently active

## 4.10 Detection of valve seat

The actuators feature force-dependent valve seat detection. After calibration, the exact valve stroke is filed in the actuator's memory. When the actuator reaches the respective end of stroke, it does not hit the valve's seat at full speed, but stops for 5 seconds at about 1% before the stored position is reached. If the positioning signal stays at 0% or 100%, the actuator travels to the calculated end position at reduced positioning speed and builds up the required nominal force.

This function extends the actuator's service life since the dynamic forces are reduced when approaching the valve seat and there will be less strain on the gear train.

In addition, the actuator's oscillations in the case of instable control are suppressed.

If no force is built up in the calculated end position (e.g. in the event of temperature effects for instance), the actuator continues to operate at a reduced positioning speed until the nominal positioning force is restored. This ensures that the valve always fully closes.

After a power failure, valve seat identification is not active - the actuators define their stroke position on power resoration to be at 50%. From now on, the actuator follows the positioning signal.

When the valve plug reaches its seat for the first time, the actuator readjusts its stroke model.

The supposed position is 50%, Y = 2 V, the actuator travels 30% of the stored valve stroke in the direction of "Actuator's stem retracted".

If the actuator reaches the seat within this 30% travel, it interprets the position as "Valve fully closed" and shifts the position of the valve's stroke accordingly without changing the extent of travel.

From now on, the actuator follows the changed valve stroke position.

This means: New position 0%, Y = 2 V, actuator travels 20% of the stored valve stroke in the direction "Actuator's stem extended".

## 4.11 Detection of foreign bodies

The actuator detects when the valve is clogged and adjusts its operational behavior accordingly to prevent damage to itself or the valve. If the actuator hits an obstacle within the calibrated stroke and is not able to overcome it with its nominal positioning force, it stores the position at which the obstacle was hit. Depending on the direction of travel, as …

- · "Lower limit of valve clogging", if the clogging was detected when traveling in the direction of "Actuator's stem retracting".
- · "Upper limit of valve clogging", if the clogging was detected when traveling in the direction of "Actuator's stem extending".

<!-- image -->

Now, the status LED blinks green and the actuator only follows the positioning signal between the positions "Actuator's stem retracted" and "Upper limit of valve clogging" or "Actuator's stem extended" and "Lower limit of valve clogging". After detection of clogging, 3 attempts are made to overcome clogging by traveling about 15% in the opposite direction and then trying again to overcome the position of clogging. If the attempts made are unsuccessful, the actuator continues to follow the positioning signal within the restricted range only and the LED continues to blink green (refer to "Indicators" on page 52).

SA..61.. only

Note

## 4.12 Forced control Z

Forced control is affected by changeover of acting direction. It uses the following operating modes:

<!-- image -->

The operating modes "Z" shown are based on factory setting "direct acting" and a "push to open" valve.

## Function principle

SAL..

SAX..

## 4.13 Technical and mechanical design

## 4.13.1 Transmission of power

Incoming positioning signals are translated to positioning commands for the motor.

A gear train transmits the motor's positioning steps to the output stage (valve coupling). Attached to the gear train are the electrical and mechanical accessory items and the manual adjuster.

In the case of the rotary actuators, the adjustment to the required torque is made in the output stage. With the stroke actuators, the translation from rotary to stroke movement takes place in the output stage.

<!-- image -->

<!-- image -->

## 4.13.2 Coupling

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

| Automatic              |                                                                                                                                                                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Manual operation       | When pushing the manual adjuster down (1), it engages and the actuator can be manually operated. Stroke actuator: When turning the manual                                                                                        |
| Fixing the position    | adjuster in clockwise / counterclockwise direction (2), the actuator's stem retracts / extends. Rotary actuator: The actuator spindle turns in the same direction. An overload protection prevents damage to the manual adjuster |
| Disengaging the fixing | When resetting the slide switch, the manual adjuster returns to automatic mode. ->The modulating SAX61.. will automatically start a Zero Position Synchronisation                                                                |

| SAL..                                                                                                                                                                                                                                                                                                        |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mounting sets are available for use with butterfly and slipper valves.                                                                                                                                                                                                                                       |
| When the motor drives the manual adjuster turns. Thus in automatic mode, the manual adjuster is used for indication of travel. If the manual adjuster is held firm in this mode, there is no transmission of power to the gear train.                                                                        |
| When pushing the manual adjuster down (1), it engages and the actuator can be manually operated. Stroke actuator: When turning the manual adjuster in clockwise / counterclockwise direction (2), the actuator's stem retracts / extends. Rotary actuator: The actuator spindle turns in the same direction. |
| Upon actuation and locking the slide switch, the manual adjuster remains engaged. When in this mode, do not turn the manual adjuster.                                                                                                                                                                        |

## Operational status indication

## Position indication

## Status indication (LED)

## 4.13.4 Indicators

<!-- image -->

<!-- image -->

In Automatic mode, the manual adjuster serves for the indication of travel. See "Automatic" (page 51).

Position indication is on 2 opposite sides. When turning the manual adjuster, the indicator moves in the same direction.

The scale indicates the stroke. When reaching the stops, the valve is either fully open or fully closed.

<!-- image -->

The status indication informs about the operational state of the actuator.

| LED   | Indication   | Operating state                       | Remarks, troubleshooting                                     |
|-------|--------------|---------------------------------------|--------------------------------------------------------------|
| Green | On           | Automatic mode                        | Normal operation                                             |
| Green | Blinking     | Calibration (page 33).                | Wait until calibration is finished (then green or red light) |
| Green | Blinking     | In manual mode                        | Manual adjuster in MAN position                              |
| Green | Blinking     | Detection of foreign bodies (page 48) | Check valve / actuator                                       |
| Red   | On           | Calibration error                     | Start calibration again (page 33)                            |
| Red   | Blinking     | Clogged valve                         | Check valve                                                  |
| Dark  | Dark         | No power or electronics faulty        | Check operating voltage                                      |

<!-- image -->

Application example:

## Potentiometer ASZ7.5/..

<!-- image -->

Flow characteristic

## 4.13.5 Electrical accessories

The auxiliary switch ASC10.51 switches on or off when a certain position is reached. The switching point can be set between 0…100%.

<!-- image -->

Switching point for S1-S2 and S1-S3 cannot be set separately. If S1-S2 is open then S1-S3 is closed.

<!-- image -->

When using an auxiliary switch, position feedback can trigger an automatic stop of the circulating pump in the end position "Fully closed".

Potentiometer ASZ7.5/.. (1000 Ω , 200 Ω , 135 Ω ) delivers an ohmic value to the controller giving the exact position of the actuator (continuous position feedback). A slip clutch prevents damage to the potentiometer in the mechanical end positions. This is also used for accurate balancing of the potentiometer in the fully closed position.

<!-- image -->

The end values of the potentiometers refer to the maximum stroke / maximum angular rotation of the actuators. For this reason, the resulting values in operation deviate, depending on the type of valve used in combination with the actuator. The potentiometer's starting point can be very accurately adjusted during installation (refer page 26).

|             | ASZ7.5/135                                                        | ASZ7.5/200                                                         | ASZ7.5/1000                                                                                  |
|-------------|-------------------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
|             | 104 Ohm at nominal stroke/nominal angular rotation                | 154 Ohm at nominal stroke/nominal angular rotation                 | 770 Ohm at nominal stroke/nominal angular rotation                                           |
|             | R = 0 + 1.04 Ohm x nominal                                        | R = 0 + 1.54 Ohm x nominal                                         | R = 0 + 7.7 Ohm x nominal stroke/nominal angular rotation (%) R = 0 + 38.5 Ohm x stroke (mm) |
|             | stroke/nominal angular rotation (%)                               | stroke/nominal angular rotation (%)                                |                                                                                              |
| SAX.. SAL.. | R = 0 + 5.2 Ohm x stroke (mm) R = 0 + 1.15 Ohm x rotary angle (°) | R = 0 + 7.71 Ohm x stroke (mm) R = 0 + 1.71 Ohm x rotary angle (°) | R = 0 + 8.55 Ohm x rotary angle (°)                                                          |

<!-- image -->

<!-- image -->

## Stem heating element

ASZ6.6

<!-- image -->

<!-- image -->

## Mounting sets ASK3..N

<!-- image -->

Function module AZX61.1offers the following choices for changing control:

- · Changeover of acting direction (page 42)
- · Connection terminals (page 58)
- · Sequence control (page 41)

Stem heating element ASZ6.6 prevents the formation of ice on the stem when medium temperatures drop below 0 °C. It is suited for universal use with valves having a stem diameter of 10 or 14 mm.

<!-- image -->

The stem heating element heats up to 120 °C.

This is a PTC element, which means it shows up with a low resistance at power up - inrush current may reach 13 A at low temperatures / high voltage level

## 4.13.6 Mechanical accessories

Weather shield ASK39.1 protects the actuator when installed outdoors. This does not lead to a change of IP class (IP54).

Mounting sets ASK31N, ASK33N and ASK35Nenable the actuators to be fitted to slipper valves VBF21.., DN65…150 and butterfly valves VKF41.. and VKF45 (page 21-25).