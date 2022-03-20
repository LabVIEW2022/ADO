rev = str('RL Rev 2.0.0.00.04T')  # ADO version
ST_FW = str('BW_RC_U-04.4.3-3c3269a539.bin')  # ST Version

# Note need to change part numbers

debug = int(0)  # todo Debug bit
db = int(0)  # DropBox Enable bit todo remember to disable before release
# D_OLED = int (1) # Enable second OLED display
ST1 = int(3)  # Load Iteration # Default to 50 after debug
ST2 = int(50)  # Drop Iteration # Default to 50 after debug
ST3 = int(50)  # Exit Iteration # Default to 50 after debug
ST4 = int(1)  # Exhaust Iteration # Default to 1 after debug
ST5 = int(1)  # EIO Module
ST6 = int(1)
ST7 = int (2) # Bypass

# BW Test
ST1_BW = int(1)
ST2_BW = int(1)
ST3_BW = int(1)
ST4_BW = int(1)
ST5_BW = int(1)
ST6_BW = int(1)
ST7_BW = int(1)

IC1 = str('4582')  # interface cable Load
IC2 = str('4582')  # interface cable Drop
IC2_2 = str('6725')  # interface cable PNU Drop
IC3 = str('8610')  # interface cable Exit
IC4 = str('5917')  # interface cable Exhaust
IC4_2 = str('9376')  # interface cable Exhaust
IC5 = str('1332')  # interface EIO Module
IC6 = str('2459')  # interface SLT Module
IC7 = str('3598')  # ByPass Module

TSN = str('TEST')

# Git Token 36687e475d60b05f17cdaf98149c465d44ec5bd6
"""
ADO Release notes:

Rev 1.3.0.00.0A
Initial test release

11/6/19
Rev 1.3.0.00.01R
Initial CLS release

11/10/19
Rev 1.3.0.00.02R
Added Interface cable interlock(Major)
Added Host name for labeling (Major)

11/14/19
Rev 1.3.0.00.03R
Added part numbers CSV files to identify revision of sub (Major)
Added check for serial number barcode (Major)

11/23/19
Rev 1.3.0.00.04R
Addressed several issues with 48V and PWM on Exhaust (minor).

11/24/19
Rev 1.3.0.00.05R
Addressed not being able to detect faulty PWM lines on Fan 1 and Fan 2
in "ADO_Exhaust".  Added 4 conductor cable from GPIO 11, 12, 13,15 going
to ADO interface CPC.  Using GPIO 11, and 12 in a pull down configuration,
we are able to use the pull up in the Exhaust fan to trigger the bit.
Exhaust testing now requires 2 cables.  Extensive rework in Exhaust code
was needed for record keeping and pwm line detects.  
Changes to "ADO_Exhaust", "ADO_UI" and "ADO_Rev" were made.
Framework is in place, need second barcode for second needed cable.
(Major)

12/5/19
Rev 1.3.0.00.06R
Added QA to Drop for pass fail (Major)

12/12/19
Rev 1.3.0.00.07R
Addressed accounting error in ADO_Drop preventing counting reset. (Major)

12/29/19
Rev 1.3.0.00.08R

Added Q&A for shoe door.  Operator marks "Pass/Fail" (Major)
Added Q&A for cooling agitator.  Operator marks "Pass/Fail" (Major)
Changed timing on drop act (Minor)
Changed timing on Q&A button on "Drop" from 1 second to 1.5 seconds (Minor)


1/23/19

Rev 1.3.0.00.09R
Labeling change on Master list to match individual testes. (Minor)

2/11/20
Rev 1.3.0.00.10R
Added hall sensor adjustment for Bimba Cylinder in Exit. (Major)

3/2/20
Rev 1.3.0.00.11R
Added support for 2 wire hopper detect.  No longer supports 3 wire hopper detect.  
3rd wire must be disconnected from plug.  (Major)

3/5/20
Rev 1.3.0.00.12R
Added support for PNU belly drop (Major)

Changes to:
Add "ADO_PNU_Drop"
Change ADO_ODO_DROP
Change ADO_UI
Change ADO_PN

3/12/20
Rev 1.3.0.00.13R
Added parsing for PN to avoid rev change compatibility issues. "Invalid PN" (Major)
Added change to ADO_BC to reflect changes in parsing.  This is used for manual (local)
change of PN bar codes (Major)
Add "ADO_PN_Buf (Major)
Change ADO_UI
Change ADO_BC
Change ADO_Rev
Change ADO_PN
Change ADO_Load
Change ADO_Drop
Change ADO_PNU_Drop
Change ADO_Exit
Change ADO_Exhaust

4/24/20
Rev 1.3.0.00.14R
Fixed parsing issue to include revision value in PN string for data collection (Minor)
Fixed SSN PN comparator (Major)

Change ADO_UI
Change ADO_Rev
Change ADO_Load
Change ADO_Drop
Change ADO_PNU_Drop
Change ADO_Exit
Change ADO_Exhaust

Cleaned Data on ADO 2 and 3 to address data prior to this fix

4/30/20
Rev 1.3.0.00.15R
Changed Max PWM on exhaust from 75% to 50%.  (Minor)
This brings down the max current down from 5.7A to 2.7A.
The mechanical relay is rated for 6A but there have been reports
of the relay sticking.  This may address the issue.

Reformatted code to be more efficient.


6/3/20
Rev 1.3.0.00.16R
Refined code for easier management. (Major)
Fixed labeling and time stamp issues for reporting. (Major)
Load butterfly in the open position after test (Minor)
Added ability to use CLS BC as well as BW BC's (Minor)
Roll back to 3 wire hopper detect.  Will change to 2 wire  for 1.3.1 release (Major)
Optimized load cycle time (Minor)


 6/4/20
 Rev 1.3.0.00.17R
 Moved pressure test before Master List 
 Added LED indicator for hall / switch adjustment in DRAG (1.3.1) and Exit
 Added simultaneous use of BW and CLS BC's 
 Added debug bit to minimize debug / MFG changes to code

6/5/20
Rev 1.3.0.00.18R
Added time out to address issue with ADO2 I2C issues.  This will not
impact other ADO's. (Minor)

6/9/20
Rev 1.3.0.00.19R
Re-wrote driver for display to support OLED display (Major)
Added BW PN Barcode pass through in 'ADO_BC' (Minor)
Addressed False positive if Little Fuse sensor miswired (Major)
    ADO_Load
    ADO_Exit
        Note: Changes have been made to Exit to perform like Load
        Bimba sensor works reguardless of misswire.
Further code refinements. (Minor)

6/12/20
Rev 1.3.0.00.20R
Adding Overall usage log to provide actual up time and usage at CLS (Minor)
Drop_PNU refinements for 1.3.1 (Major)  Does not effect 1.3.0
Fixed ADO_BC barcode change bug (Minor)

6/16/20
Rev 1.3.0.00.21R
Add Flag alignment Q&A for Load (Major)
6/19/20
Added DropBox support for ADO_Logs (Minor)

6/19/20
Rev 1.3.0.00.22R
Added Test DB (Minor)
6/22/20
Added support for secondary OLED display (Minor)
Expand Debug mode Exit (Minor)
Increased time by 2 sec between open and close (Exit) to account for flow restriction. (Minor)
Added debug via SSN (Minor)
Fixed machine name bug (Minor)
6/23/20
Removed machine name variable from path 'DB' (Minor)
Fixed minor debug bugs in Exhaust 
Added dual OLED detect (Minor)
6/24/20
Added 'NO_NAME' Tag (Minor)

6/25/20 - 7/25/20
Rev 1.3.0.00.23R
Converted ADO code to run on 3.7 interpreter from 2.7.  2.7 EOL 1/1/2020 (Major)
Added Expanded IO (Major)
Separated PASS / FAIL and Error in data collection (Major)
    Will require Marco's team to make changes upt IoT upload scrip from ADO (Major)
Added ADO_Rev in new column (Major)
Added state in new column (Major)
Updated ADO_Data_Reset to include new ADO_Rev and state resets (Major)
Streamlined ADO Dual display support (Major)
Streamlined data logs to drastically minimize lines of code required to capture errors in HVC (Major)
Made code more modular (Major)
Added text scroll capapbilites (Minor)
Added 'ulog' to ADO_BC to monitor PN Barcode Changes (Minor)
Moved Exit hall adjustment prior to agitator test (Minor)
Added buzzer to HVC/EIO
Toggle Dual OLED bit to '0' after completed HVC test to prevent errors when going back to ADO Main screen (Major)

7/25/20
Rev 1.3.0.00.24T
Beginning work on HDMI Expanded Display
Added support for Rev 1.3.0.04.00R hardware (Logic Isolation)
Added support for System pneumatic leak test GPIO 22

8/11/20
Rev 1.3.0.00.25T
Added MCP23017 to ADO main unit at address 0x22.  Leak, System Leak, and Isolation solenoids to be moved to this board.
    This allows for a reclaim of GPIO pins to be used for PWM at a later date.
Changing GPIO from Board to BCM
Added SLT (System Leak Test)
Added Temp differential SW component for future temp projects using 1 wire DS18B20 (BCM4 of GPIO).
    Will require ADO HW 1.3.0.06.00R

8/21/20
Rev 1.3.0.00.26T
Enabled DS18B20 for temperature monitoring and HW validation. 
Added 'if' to allow ADO5 compatibility. 
Changed location of 'Master Lists'  now located in
    /home/pi/Bellwether/ADO_MASTER_LIST_DATA
Expanded on leak test for Load, PNU Drop, Exit to test for housing leaks at the subassembly level.
Added 'ulog' to all reports in HVC
Fixed GPIO to MC IO on ADO_EXIT
9/3/20
Added HW/SW validation to prevent ADO mix ups by hard coding unique identifier.
9/9/20
Added internal temperature monitoring
9/14/20
Added Side B leak (Piston) test on ADO Exit

9/30/20
Fixed addressing conflict on i2c bus.  See ADO HW

9/17/20
Rev 1.3.05.00.01T 
Created new branch to support 1.3.05 version of machine
Added support for pneumatic check valve in exit.
Reduced load and exit cycles by 50%
Added 'CheckV' bit

10/15/20
Added ST Flash support

11/10/20
Added ADO_TEMP for system test (Standalone test)

12/1/20
Added ADO_WatchDog.  This allows for a single interface cable test on the Exhaust system.

12/29/20
Fixed EIOi module (Broke due to 2.0 testing)
Enabled Check valve leak test on SLT

4/12/21
Rev 1.3.1.00.01T 
Moved 2 / 3 wire hopper detect from GPIO to P.IO board.
p.digital.read(3) 2 wire
p.digital.read(4) 3 wire
4/26/21
Added true RPM using interrupt.
4/27/21
Added 'Pass / Fail' if RPM doesn't meet minimum speed.
Added logging for minimum speed not met.
Code clean up.
Note Changes
5/11/21
Changed Exhaust test to prevent over current with Delta fans and under sized ADO 48VDC supply.
Working range 15 - 40% duty cycle

5/11/21
Rev 2.0.0.00.01T
Replaced 'ado' with 'ado_' (Unit).  This is to pave the way for ado object.
5/11/21
Revised and cleaned up Load to use ADO object
Added Basic ID Tag Support
Cleaned Load, Drop to use ADO Object.

5/25/21
Added Open Hall Adjust on load
Bug fix with ADO object
Bug fixes ADO_PNU_Drop
Fixed Drop Reporting
Completed Exhaust single fan (with option for 2)
Exhaust, Load, Drop now using ADO object

8/6/21
Completed Exhaust 2.0
Removed PWM Second cable check


8/7/21
Tuned Load
Added QA Wire Check on Exhaust
Changed Drop (DRAG) cable to 4582 same as Load

8/9/21
Made Changes to allow for small compressor to work.
Exit now uses ADO object.

9/2/21
Added excpetion for missing directory in 'ADO_DATA_RESET'
Added 'user' to headers
Added:
    ADO_ODO_BP.py
    ADO_Step.py (Stepper Driver)
    ADO_BP.py
    Data:
        Added data collection directories for BP

9/9/21
Rev 2.0.0.00.02T
Added Alpha Bypass Test
    Added ADO_Step
    Added ADO_Decoder
    Added ADO_ODO_BP
    Updated ADO_Rev
    Updated ADO_DATA_RESET
    Updated ADO_UI
    Added Directory ADO_BP_DATA
Added User list (TAG)

9/14/21
Began work on SLT_ASS

9/14/21
Rev 2.0.0.00.03T
New branch for SLT_ASS Dev (Scrapped)
BW_CDA in place of SLT_ASS

9/28/21
Rev 2.0.0.00.04T
Unified Reporting work begin
Added Display support in Object ADO
    May have issues with EIO display

9/28/21
Initial Release of Cooling tray 2.0
    
9/30/21
Added External reset

10/7/21
Unified Decoder code
Added array for encoder position comparison

    

"""
