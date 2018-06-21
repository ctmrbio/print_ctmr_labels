# CTMR Zebra label printing application
A very simple application to print only CTMR labels using the Zebra printer
at [CTMR](http://ki.se/en/research/centre-for-translational-microbiome-research-ctmr).

# Artwork credits
* <img src="https://image.flaticon.com/icons/svg/141/141701.svg" width=40> Zebra icon by [Freepik](www.freepik.com) from www.flaticon.com. Used under the [Flaticon basic license](http://file000.flaticon.com/downloads/license/license.pdf).
* <img src="http://ki.se/sites/default/files/styles/1_of_3/public/ina-ctmr_0.jpg?itok=AWJgtpVZ" width=80> Bacteria artwork by [Ina Schuppe Koistinen](http://www.inasakvareller.se/). Used with permission.

# Running the application
The application runs in Python 2.7 with
[Gooey](https://github.com/chriskiehl/Gooey) (used for the simple GUI). It is
possible to run the application without GUI in pure command-line mode with
just a simple modification of the source code. Just edit the code and comment
the `@Gooey` decorator line on line 21 in `print_cmtr_labels.py`.

# Printer information
The Zebra label printer is model ZT230 and uses the ZPL language for rendering
barcodes. A handy viewer for this language can be found [here](http://labelary.com/viewer.html).

# Computer connection
The Zebra printer is now connected to the printer computer using a USB network card (StarTech USB
2.0 to 10/100Mpbs Fast Ethernet Network Adapter Dongle, Part # USB2100). The network adapter's
IPV4 configuration has been set to `169.254.133.162`/`255.255.0.0` (IP address/hostmask).
The Zebra label printer should be automatically connected, and the network LED icon should be
lit green.
The network settings of the Zebra printer should be set to "PERMANENT", and the IP address 
`169.254.133.1` and hostmask `255.255.0.0` (same as the computer). 
The gateway can be left as `0.0.0.0`. After setting these,  
then the network settings should be "RESET" to save this configuration.
