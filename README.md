# CTMR Zebra label printing application
A very simple application to print only CTMR labels using the Zebra printer
at [CTMR](http://ki.se/en/research/centre-for-translational-microbiome-research-ctmr).

# Artwork credits
* <img src="https://image.flaticon.com/icons/svg/141/141701.svg" width=40> Zebra icon by [Freepik](www.freepik.com) from www.flaticon.com. Used under the [Flaticon basic license](http://file000.flaticon.com/downloads/license/license.pdf).
* <img src="img/config_icon.png" width=80> Bacteria artwork by [Ina Schuppe Koistinen](http://www.inasakvareller.se/). Used with permission.

# Running the application
The application runs in Python 3 with
[Gooey](https://github.com/chriskiehl/Gooey) (used for the simple GUI). It is
possible to run the application without GUI in pure command-line mode with just
a simple modification of the source code. Just edit the code and comment the
`@Gooey` decorator line on line 21 in `print_cmtr_labels.py`.

## Dependencies
There is a conda environment file with all the required dependencies to run
the application in Linux called `conda_linux.yml`. Install the dependencies
with `conda env create -f conda_linux.yml`. Remember to activate the environment
before running the application.
The required depedencies to run the application in macOS is called `conda_mac.yml`. Install dependencies
with `conda env create -f conda_mac.yml`.
To run the application in Windows, nstall dependencies with `conda env create -f win_env.yml`. Environment can be activated with `conda activate printctmrlabels`.

# Printer information
The Zebra label printer is model ZT230 and uses the ZPL language for rendering
barcodes. A handy viewer for this language can be found [here](http://labelary.com/viewer.html).
Documentation for the language used to code the barcodes can be found [here](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf).
`large_box.py` has a commented barcode which may be used as a reference.

# Computer connection
The Zebra printer is now connected to the printer computer using a USB network
card (StarTech USB 2.0 to 10/100Mpbs Fast Ethernet Network Adapter Dongle, Part
# USB2100). The network adapter's IPV4 configuration has been set to
`169.254.133.162`/`255.255.0.0` (IP address/hostmask).  The Zebra label printer
should be automatically connected, and the network LED icon should be lit
green.
The network settings of the Zebra printer should be set to "PERMANENT",
and the IP address `169.254.133.1` and hostmask `255.255.0.0` (same as the
computer).  The gateway can be left as `0.0.0.0`. After setting these,  then
the network settings should be "RESET" to save this configuration.

# Current Setup:
A laptop runs Windows10 with Python version (3.6.3) installed. The application is located at C:\Users\Public\Public Code\print_ctmr_labels\ and a shortcut is created at C:\Users\Public\Desktop
