# candle_heightmap_adjust

This program is used to shift a Candle (CNC software) heightmap up or down
when cutting isolation routes on copper PCBs.

I have found through structured testing on two separate machines that the
heightmap function of Candle combined with a "budget" 3018 CNC machine
has a measurement tolerance of around 0.1mm.  Interestingly, the execution
tolerance is more precise.

The test told the machine to cut a small grid at 0.15mm, 0.10mm, 0.05mm, 0.0mm
and -0.05mm.  A perfect machine and heightmap file would lead to no contact
until 0.0mm, a tiny brushing at 0.0mm, and full penetration through the thin
copper at -0.05mm.  Indeed I saw exactly this on both machine, but only about
25% of the time.

The rest of the time, it cut deeper and I would see initial contact at 0.05mm
or 0.1mm.  This means that the actual -0.05mm setting with these would actually
be cutting at -0.15mm.  With a 0.1mm tipped v bit, this depth can be enough to
break the end off of the bit.

There are several solutions, but I propose the one below which involves
manipulating (z shifting) the height.map file until it is right on.

Looking at more detail:

##Run the `make_test_box.py` file to create a test gcode file.

    ./make_test_box.py test.yaml

This creates a simple gcode file which traces a box at z=0.
Parameters are in `test.yaml`. 

*Make sure the width and height parameters in the yaml are larger than your design*.

Otherwise you'll could be cutting a test trace right through where you want
isolation traces later.

The feed speed is also something you'll want to change in the .yaml, matching
whatever you decided to use in your actual isolation routing.  I found
140 mm/min to be safe but slow.  I found 200 mm/min OK most of the time but did
break a 0.1mm tip at this setting once.  Any value can work or not work
depending on your bit, machine runout, and plunge tolerance so you might
need to experiment with plenty of spare bits on hand (e.g. don't get expensive
bits before you get some experience!)

The default output is `test.nc` 

## Run `candle_heightmap_adjust.py` to shift the height map up

    ./candle_heightmap_adjust.py --input=height.map --delta=0.1

This creates a `height_delta0.1.map` file.

## Use the `test.nc` with the `height_delta0.1.map` file to check the height

If you get no contact, then you should generate another height map that is a
little closer, maybe

    ./candle_heightmap_adjust.py --input=height.map --delta=0.07

Keep repeating until you get a sign of contact.  At this point you can
decide how much you want to hunt for the perfect number.  Within 0.03mm
should be good enough for any bit.  With a wider bit that does not
break as easily, within 0.1mm should be fine.

Now you have the height map file that you can use with your actual
isolation routing and things *should* work out well assuming you don't
have bad luck.
