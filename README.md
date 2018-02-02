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
barcodes. A handy viewer for this language can be found [here](http://labelary.com/viewer.html)
