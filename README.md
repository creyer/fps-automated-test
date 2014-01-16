fps-automated-test
==================

Calculates in an automated way, with selenium, the frames per second for an html page.

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


Thanks:
===
The javascript is based on the original work of mrdoob: https://github.com/mrdoob/stats.js 

Many thanks
