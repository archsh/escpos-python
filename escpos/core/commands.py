# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
### ESC/POS Command List ##############################################################################################

### Standard Commands
HT='\x09'           # Horizontal tab,
                    # Moves print position to next horizontal tab position.
LF='\x0a'           # Line feed,
                    # Prints the data in the print buffer and performs a line feed based on the set line feed amount.
FF='\x0c'           # Print and recover to page mode,
                    # Prints all buffered data to the print region collectively, then recovers to the standard mode.
CR='\x0d'           # Print and carriage return,
                    # When an automatic line feed is enabled, this command functions in the same way as LF (print and line feed). When the automatic line feed is disabled, this command is ignored.
CAN='\x18'          # Cancel print data in page mode,
                    # Deletes all print data in the currently set print region in page mode.
DLE_04_n='\x10\x04' # Real-time status transmission,
                    # Transmits the status specified by n in real-time.
                    # n = 1: Transmit printer status
                    # n = 2: Transmit offline cause status
                    # n = 3: Transmit error cause status
                    # n = 4: Transmit continuous paper detector status
                    # n = 5: Transmit presenter paper detector status
                    # The printer transmits the present status.
                    # Each status is represented by one-byte of data.
DLE_05_n='\x10\x05' # Real-time request to printer.
                    # Responds to requests n specifications from the host in real-time. n specifications are below.
                    # n = 1: Recover from the error and start printing from the line where the error occurred.
                    # n = 2: Recover from error after clearing the reception buffer and print buffer.
DLE_14_n_m_t='\x10\x14'
                    # Real-time output of specified pulse
                    # This outputs a signal specified by t to the connector pin specified by m.
                    # n = 1; m = 0,1;  1 ≤ t ≤ 8
                    # This outputs a signal specified by t to the connector pin specified by m.
                    # m = 0: #2 Pin of the drawer kick connector
                    # m = 1: #5 Pin of the drawer kick connector
                    # On time is set to t x 100 msec; Off time is set to t x 100 msec.
ESC_0c='\xqb\x0c'   # Print data in page mode
                    # Prints all buffered data in the print area collectively in page mode.
ESC_20_n='\x1b\x20' # Set character right space amount
                    # 0 ≤ n ≤ 255, n = 0
                    # Sets the right space amount for the character to [n x basic calculated pitch].
ESC_21_n='\x1b\x21' # Batch specify print mode
                    # 0 ≤ n ≤ 255,n = 0
                    # Specifies batch print mode
                    # Bit   Function                0       1
                    # 7     Underline               OFF     ON
                    # 6     Undefined               --      --
                    # 5     Double wide expanded    OFF     ON
                    # 4     Double tall expanded    OFF     ON
                    # 3     Emphasized printing .   OFF     ON
                    # 2     Undefined --
                    # 1     Undefined -- --
                    # 0     Character Fonts         Font-A  Font-B
ESC_24_nL_nH='\x1b\x24'
                    # Specify absolute position
                    # 0 ≤ nL ≤ 255, 0 ≤ nH ≤ 255
                    # Specifies the next printing starting position using an absolute position based on the left margin
                    # position. The next printing starting position is the position specified by [(nL+nH×256) × basic
                    # calculated pitch] from the left margin position.
ESC_25_n='\x1b\x25' # Specify/cancel download character set
                    # 0 ≤ n ≤ 255, n = 0
                    # Specifies or cancels the download character set.
                    #  When n = <*******0>B, the download character set is cancelled.
                    #  When n = <*******1>B, the download character set is specified.
ESC_26_y_c1_c2='\x1b\x26'
                    # Define download characters
                    # ESC & y c1c2 [x1 d1 ... d (yX x1)] ... [a xd1 ... d (y× ax)]
                    # y = 3, 32 ≤ c1 ≤ c2 ≤ 126, 0 ≤ x ≤ 12 (Font A), 0 ≤ x ≤ 9 (Font B), 0 ≤ d1....d (y×ax) ≤ 255
                    # Defines the download characters to the specified character code.
                    # y specifies the number of bytes in the vertical direction.
                    # c1 specifies the starting character code for the definition; c2 specifies the final character code.
                    # x specifies the number of dots in the horizontal direction for the definition.
ESC_2a_m_nL_nH='\x1b\x2a'
                    # Specify bit image mode
                    # ESC * m nL nHd1...dk
                    # m = 0,1,32,33; 0 ≤ nL ≤ 255; 0 ≤ nH ≤ 3; 0 ≤ d ≤ 255
                    # Selects a bit-image mode in mode m for the number of dots specified by nL and nH.
                    # m Mode
                    # 0 8-dot single density
                    # 1 8-dot double density
                    # 32 24-dot single density
                    # 33 24-dot double density
ESC_2d_n='\x1b\x2d' # Specify/cancels underline mode
                    # 0 ≤ n ≤ 2, 48 ≤ n ≤ 50, n=0
                    # n         Function
                    # 0, 48     Cancels underline
                    # 1, 49     Sets to one-dot width underline and specifies underlines.
                    # 2, 50     Sets to two-dot width underline and specifies underlines.
ESC_32='\x1b\x32'    # Set default line spacing,
                    # Sets line feed amount per one line to approximately 4.23 mm (1/6 inch).
ESC_33_n='\x1b\x33'  # Set line feed amount
                    # 0 ≤ n ≤ 255, Line feed amount equivalent to approximately 4.23 mm (1/6 inch).
                    # Sets the line space for one line to [n x basic calculated pitch].
ESC_3d_n='\x1b\x3d' # Select peripheral device
                    # 0 ≤ n ≤ 255, Initial Value n = 1
                    # Selects the peripheral device for which the data is effective from the host computer.
ESC_3f_n='\x1b\x3f' # Delete download characters
                    # 32 ≤ n ≤ 126
                    # Deletes the download characters to the specified character code.
ESC_40='\x1b\x40'   # Initialize printer
                    # Clears data from the print buffer and sets the printer to its default settings.
ESC_44='\x1b\x44'   # Set horizontal tab position
                    # ESC D n1...nk NUL
                    # 1 ≤ n ≤ 255, 0 ≤ k ≤ 32
                    # Sets horizontal tab position
                    # n specifies the column number for setting a horizontal tab position from the left margin or the beginning of the line.
                    # k indicates the number of horizontal tab positions to be set.
ESC_45_n='\x1b\x45' # Specify/cancel emphasized characters
                    # 0 ≤ n ≤ 255, n=0
                    # Specifies or cancels emphasized characters.
                    # Cancels emphasized characters when n = <*******0>B.
                    # Specifies emphasized characters when n = <*******1>B.
ESC_47_n='\x1b\x47' # Specify/cancel double printing
                    # 0 ≤ n ≤ 255, n=0
                    # Specifies or cancels double printing.
                    # Cancels double printing when n = <*******0>B.
                    # Specifies double printing when n = <*******1>B.
ESC_4a_n='\x1b\x4a' # Print and Paper Feed
                    # ESC J n
                    # 0 ≤ n ≤ 255
                    # Prints the data in the print buffer and feeds the paper [n x basic calculated pitch].
ESC_4c='\x1b\x4c'   # Select page mode
                    # Switches from standard mode to page mode.
ESC_4d_n='\x1b\x4d' # Select character font
                    # n = 0, 1, 48, 49
                    # Selects character font.
                    # n     Function
                    # 0,48  Selects Font A (12 x 24).
                    # 1,49  Selects Font B (9 x 17).
ESC_52_n='\x1b\x52' # Select international characters
                    # 0 ≤ n ≤ 10,Initial Value n = 0
                    # Selects the character set for the country listed below.
                    # n Country
                    # 0 America
                    # 1 France
                    # 2 Germany
                    # 3 UK
                    # 4 Denmark I
                    # 5 Sweden
                    # 6 Italy
                    # 7 Spain I
                    # 8 Japan
                    # 9 Norway
                    # 10 Denmark II
                    # 11 Spain II
                    # 12 Latin America
                    # 13 Korea
ESC_53='\x1b\x53'   # Select standard mode
                    # Switches from page mode to standard mode.
ESC_54_n='\x1b\x54' # Select character print direction in page mode
                    # 0 ≤ n ≤ 3, 48 ≤ n ≤ 51; Initial Value n = 0
                    # Selects the character printing direction and starting point in page mode.
                    # n         Print Direction             Starting Point
                    # 0, 48     Left to Right               Upper Left (A in the figure below)
                    # 1, 49     Bottom to Top               Lower Left (B in the figure below)
                    # 2, 50     Right to Left               Lower Right (C in the figure below)
                    # 3, 51     Top to Bottom               Upper Right (D in the figure below)
ESC_56_n='\x1b\x56' # Specify/cancel character 90 degree clockwise rotation
                    # 0 ≤ n ≤ 1, 48 ≤ n ≤ 49; Initial Value n = 0
                    # Specifies or cancels character 90 degree clockwise rotation.
                    # n         Function
                    # 0, 48     Cancels 90 degree clockwise rotation
                    # 1, 49     Specifies 90 degree clockwise rotation
ESC_57='\x1b\x57'   # Set print region in page mode
                    # ESC W xL xH yL yH dxL dxH dyL dyH
                    # 0 ≤ xL, xH, yL, yH, dxL, dxH, dyL, dyH ≤ 255; However, this excludes dxL = dxH = 0 or dyL = dyH = 0
                    # Sets the print region position and size.
                    # Horizontal direction starting point [(xL + xH x 256) x basic calculated pitch]
                    # Vertical direction starting point [(yL + yH x 256) x basic calculated pitch]
                    # Horizontal direction length [(dxL + dxH x 256) basic calculated pitch]
                    # Vertical direction length = [(dyL + dyH x 256) basic calculated pitch]
ESC_5c_nL_nH='\x1b\x57'
                    # Specify relative position
                    # 0 ≤ nL ≤ 255, 0 ≤ nH ≤ 255
                    # Specifies the next print starting position with a relative position based on the current position. This
                    # sets the position from the current position to [(nL + nH x 256) x basic calculated pitch] for the next
                    # print starting position.
ESC_61_n='\x1b\x61' # Position alignment
                    # 0 ≤ n ≤ 2, 48 ≤ n ≤ 50; Initial Value n = 0
                    # Aligns all print data in one line to a specified position.
                    # N     Position
                    # 0, 48 Left alignment
                    # 1, 49 Center
                    # 2, 50 Right alignment
ESC_63_33_n='\x1b\x63\x33'
                    # Select paper out sensor to enable at paper out signal output
                    # 0 ≤ n ≤ 15; Initial Value (A) Specification: n = 12; (B) Specification: n = 0
                    # Selects paper out detector that outputs a paper out signal when paper has run out.
                    # Bit   Function                        0           1
                    # 1     Paper roll near end detector    Invalid     Valid
                    # 0     Paper roll near end detector    Invalid     Valid
ESC_63_34_n='\x1b\x63\x34'
                    # Select paper out sensor to enable at printing stop
                    # 0 ≤ n ≤ 255; Initial Value n = 0
                    # Selects the paper out detector to stop printing when paper has run out.
                    # Bit   Function                        0           1
                    # 1     Paper roll near end detector    Invalid     Valid
                    # 0     Paper roll near end detector    Invalid     Valid
ESC_63_35_n='\x1b\x63\x35'
                    # Enable/disable panel switches
                    # 0 ≤ n ≤ 255; Initial Value n = 0
                    # Toggles the panel switches between enabled and disabled.
                    # Enables panel switches when n = <*******0>B.
                    # Disables panel switches when n = <*******1>B.
ESC_64_n='\x1b\x64' # Print and feed paper n lines
                    # 0 ≤ n ≤ 255
                    # Prints the data in the print buffer and performs a paper feed of n lines.
ESC_70_m_t1_t2='\x1b\x70'
                    # Specify pulse
                    # ESC p m t1 t2
                    # 0 ≤ m ≤ 1, 48 ≤ m ≤ 49, 0 ≤ t1 ≤ 255, 0 ≤ t2 ≤ 255
                    # m Connector Pin
                    # 0, 48 Drawer kick connector pin #2
                    # 1, 49 Drawer kick connector pin #5
ESC_74_n='\x1b\x74' # Select character code table
                    # 0 ≤ n ≤ 5, n = 255; Initial Value n = 0
                    # Select page n of the character code table.
                    # n Character Type
                    # 0 PC437 (USA: Standard Europe)
                    # 1 Katakana
                    # 2 PC850(Multilingual)
                    # 3 PC860(Portuguese)
                    # 4 PC863(Canadian-French)
                    # 5 PC865(Nordic)
                    # 16 WPC1252
                    # 17 PC866 (Cyrillic #2)
                    # 18 PC852 (Latin2)
                    # 19 PC858
                    # 255 Blank page
ESC_7b_n='\x1b\x7b' # Specify/cancel upside-down printing
                    # 0 ≤ n ≤ 255, Initial Value n = 0
                    # Specifies or cancels upside-down printing.
                    # Cancels upside-down printing when n = <*******0>H.
                    # Specifies upside-down printing when n = <*******1>H.
FS_67_31_m_a1_a2_a3_a4_nL_nH='\x1c\x67\x31'
                    # Write data to user NV memory
                    # FS g 1 m a1 a2 a3 a4 nL nH d1 ... dk
                    # m = 0
                    # 0 ≤ {a1+ (a2×256) + (a3 × 65536) + (a4×16777216) } ≤ 1023
                    # 1 ≤ {nL+ (nH×256) } ≤ 1024
                    # 32 ≤ d ≤ 255
                    # k = {nL+ (nH×256) }
                    # Stores data in the user NV memory.
                    # m is fixed at 0.
                    # a1, a2, a3 and a4 specify the data storage addresses {a1 + (a2 x 256) + (a3 x 65536) + (a4 x 16777216)}.
                    # nL and nH specify the storage data count in byes of {nL+ (nH x 256)}.
                    # d specifies the stored data.
FS_67_32_m_a1_a2_a3_a4_nL_nH='\x1c\x67\x32'
                    # Read user NV memory data
                    # FS g 2 m a1 a2 a3 a4 nL nH
                    # m = 0
                    # 0 ≤ {a1+ (a2×256) + (a3×65536) + (a4×16777216) } ≤ 1023
                    # 1 ≤ {nL+ (nH×256) } ≤ 80
                    # Sends the data in the user NV memory.
                    # m is fixed at 0.
                    # a1, a2, a3 and a4 specify the data sending starting addresses {a1 + (a2 x 256) + (a3 × 65536) + (a4×16777216)}.
                    # nL and nH specify the transmissino data count in byes of {nL+ (nH x 256)}.
FS_70_n_m='\x1c\x70'
                    # Print NV bit image
                    # 1 ≤ n ≤ 255, 0 ≤ m ≤ 3, 48 ≤ m ≤ 51
                    # Prints NV bit image n using mode m.
                    # m Mode Density of Vertical Direction Dots   Density of Horizontal Direction Dots
                    # 0, 48 Normal Mode 180 DPI 180 DPI
                    # 1, 49 Double-wide Mode 180 DPI 90 DPI
                    # 2, 50 Double-tall Mode 90 DPI 180 DPI
                    # 3, 51 Quadruple Mode 90 DPI 90 DPI
                    # n specifies the NV bit image number.
                    # m specifies the bit-image mode.
FS_71_n='\x1c\x71'  # Define NV bit image
                    # FS q n [xLxHyLyHd1...dk]1 ... [xLxHyLyHd1...dk] n
                    # 1 ≤ n ≤ 255
                    # 0 ≤ xL ≤ 255
                    # 0 ≤ xH ≤ 3 However, 1 ≤ (xL+xH×256) ≤ 1023
                    # 0 ≤ yL ≤ 255
                    # 0 ≤ yH ≤ 1 However, 1 ≤ (yL+yH×256) ≤ 288
                    # 0 ≤ d ≤ 255
                    # k = (xL+xH×256) × (yL+yH×256) ×8
                    # Total defined data area = 2 M bytes (256 K bytes)
                    # Defines the specified NV bit image.
                    # n specifies the number of NV bit images to define.
                    # xL and xH specify the horizontal direction for one NV bit image (xL + xH x 256) x 8 dots.
                    # yL and yH specify the vertical direction for one NV bit image (yL + yH x 256) x 8 dots.
GS_21_n='\x1d\x21'  # Select character size
                    # 0 ≤ n ≤ 255; n = 0
                    # Bit-7 Bit-6 Bit-5 Bit-4 Hor. Dir. Mag.Ratio | Bit-3 Bit-2 Bit-1 Bit-0 Hor. Dir. Mag.Ratio
                    # 0 0 0 0 1 0 0 0 0 1
                    # 0 0 0 1 2 0 0 0 1 2
                    # 0 0 1 0 3 0 0 1 0 3
                    # 0 0 1 1 4 0 0 1 1 4
                    # 0 1 0 0 5 0 1 0 0 5
                    # 0 1 0 1 6 0 1 0 1 6
                    # 0 1 1 0 7 0 1 1 0 7
                    # 0 1 1 1 8 0 1 1 1 8
GS_24_nL_nH='\x1d\x24'
                    # Specify absolute position for character vertical direction in page mode
                    # 0 ≤ nL ≤ 255, 0 ≤ nH ≤ 255
                    # Specifies the character vertical direction position for the data expansion starting position using the
                    # absolute position based on the starting point in page mode. The position of the character vertical
                    # direction for the next data expansion starting position is the position specified by [(nL + nH x 256) x
                    # basic calculated pitch] from the starting point.
GS_2a_x_y='\x1d\x2a'
                    # Define download bit images
                    # ASCII GS * x yd1...d (x×y×8)
                    # 1 ≤ x ≤ 255; 1 ≤ y ≤ 48 However, x × y ≤ 1536; 0 ≤ d ≤ 255
                    # Defines the download bit image of the number of dots specified by x and y.
                    # x specifies the number of dots in the horizontal direction.
                    # y specifies the number of bytes in the vertical direction.







#######################################################################################################################