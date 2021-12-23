# candle_heightmap_adjust

This program is used to shift a Candle (CNC software) heightmap up or down
when cutting isolation routes on copper PCBs.

I have found through controlled testing on two separate machines that the
heightmap function of Candle combined with a "budget" 3018 CNC machine
has a measurement tolerance of around 0.1mm.  Interestingly, the execution
tolerance is more precise.

The tests I ran told the machine to cut a small grid at 0.15mm, 0.10mm, 0.05mm,
0.0mm and -0.05mm.  A perfect machine and heightmap file would lead to no
contact until 0.0mm, a tiny brushing at 0.0mm, and full penetration through
the thin copper at -0.05mm.  Indeed I saw exactly this on both machines, but
only about 25% of the time.

The rest of the time, it cut deeper and I would see initial contact at 0.05mm
or 0.1mm.  This means that an intended -0.05mm depth setting with those
heightmaps would actually be cutting at -0.15mm.  With a 0.1mm tipped v bit,
this depth error can be enough to break the end off of the bit.

There are several solutions, but I propose the one below which involves
manipulating (z shifting) the height.map file until it is right on.

Looking at more detail:

## Run the `make_gcode.py` file to create a test gcode file.

    ./make_gcode.py test.yaml

This creates a simple gcode file which traces a rectangle at z = 0.0.
Parameters are in `test.yaml`. 

**Make sure the width and height parameters in the yaml are larger than your design**.

Otherwise you'll could be cutting a test trace right through where you want
isolation traces later.

The feed speed is also something you may want to change in the .yaml. I found
140 mm/min to be safe but slow.  I found 200 mm/min OK most of the time but did
break a 0.1mm tip at this setting once.  Any value can work or not work
depending on your bit, machine runout, and plunge tolerance so you might need
to experiment with plenty of spare bits on hand (e.g. don't get expensive bits
before you get some experience!)

The default output is `test.nc` 

## Load `test.nc` into Candle.

   1. Prep your material
   2. Connect z-probes
   3. Find your x,y origin and hit the 'xy origin' button.
   4. Get about 1-2mm above the surface and press the 'z origin' button followed by the 'z probe button'
   5. Start the heightmap function.  Use the 'auto' button to set the size.  Choose a row and column count for a 5-10mm spacing.
   6. Use the "Save As..." menu option to save the height map to a file `height.map`
   7. Disconnect the probes.

From this point forward, **do not** rezero xy or z!  If you do, you'll have to start over.


## Run `candle_heightmap_adjust.py` to shift the height map up

    ./candle_heightmap_adjust.py --input=height.map --delta=0.1

This creates a `height_delta0.1.map` file.  Load that file into Candle and make
sure the "Use heightmap" checkbox is checked.

## Run the CNC job to check the height

If you get no contact, then you should generate another height map that is a
little closer, maybe

    ./candle_heightmap_adjust.py --input=height.map --delta=0.07

and load the newly created `heightmap_delta0.07.map` file into Candle (again,
no rezeroing!).  No need to reload the gcode file.  Try another CNC run. 

Keep repeating with different heightmap offsets until you get a sign of
contact.  At this point you are close to the perfect heighmap file.  Tweak the
final offset a little if you want or leave it be.  Within 0.03mm should be good
enough for any bit.  With a wider bit that does not break as easily, within
0.1mm should be fine.

Now you have the height map file that you can use with your actual
isolation routing and things *should* work out well assuming you don't
have bad luck.
