fps-automated-test
==================

Calculates in an automated way, with selenium, the frames per second for an html page.
It uses the javascript requestAnimFrame, in order to calculate the framerate variation.
Please refer to the file: src/javascript/README.md for more insight on the javascript part

Disclaimer
==================
The extracted fps values are not the same as the ones you may experience during your normal user experience.(in the same enviorenment)

Never the less the extracted values are a good measure as long they satisfy the following principles:
* the extracted values are consistent - we have the same mean and the same std deviation between different runs with the same input
* it shows a degarding in performance under the same input as when a normal user experiences the same

The performance is consitent and could vary more or less from what a normal user is experiencing but still it will be a variation in the same direction

In order to better match your user experience it is required to modify the fps.py file
The code does not give any guaranty of your actual performance, it just gives a relative measure of it.

Requirements:
===
* python
* selenium
* lettuce
* numpy

Before run:
===
* Please make sure you have all the reuired dependencies installed:
* Also please insert all the values inside: perf_util.py

How to run it:
===
After you have made the changes required to match your page, you can run it with the `lettuce` command in the src folder.

Case study:
===
Twitter -> look into the example folder to see how the script is modified to check the Twitter performace.

Running the script, you will not see any degradation in performace between 100 and 500 scrols, because there is none.

Thanks:
===
The javascript is inspired from the original work of mrdoob: https://github.com/mrdoob/stats.js

Many thanks
