# just a Dummy file creator (for hiyaCFW)

The Nintendo DSi system menu uses a signed 32-bit integer to represent how much free space the system has.
In it's intended use this would be sufficient since the NAND on the Nintendo DSi was always smaller than 128MB

However when using hiyaCFW, the free space is now the free space on the SD card not the NAND and so can easily go above the limit a 32-bit signed integer can hold which causes an overflow. This overflow makes the value jump to a negative number and it causes the DSi system to throw the "An error has occured" screen on boot.

To remedy this, dummy files can be created to reduce the amount of free space detected and prevent the overflow from occuring.

This program automates this process and calculates and creates the dummy files necessary

Credits to
 - BananaMan95#0800 of Discord for the idea and for testing on macOS
 - @NightYoshi370 for the explanation of why the error occurs 
 - the hiyaCFW devolopers 
 - Nintendo for making the DSi!
