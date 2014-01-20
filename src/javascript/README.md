## local_perf.js


### Attention:
If you wish to modify this javascript please consider that this file will be placed inside a document.write as a single javascript line.

This means that you should not introduce any coments in the code, and that some extra `;` might be required after `}`

### Inside the javascript
The file contains 2 parts, one which takes care of a visual display, nothing but a graph to render the performance, and the main logic, which resides under the `loop function`

### How do we measure performance with this script:
The script is using `requestAnimFrame` method to run the `loop` method on each frame.

Each time the loop method is called we increase the number of frames until we have a new seccond: `now > 1000 + lastTime`

Each new second, the script updates the graph with the number of frames and also cals the `extractFps` function.

The `extractFps` purpose is to register on an array the fps values, in order to be exported. The registration only happens when `insertIntoFpsArr` variable is true (this variable value is controlled from the python script)

### Only for debug:

The value of `useHighAnimation` can be set to true, in order to have a graph which is updated each frame, but be aware that this is going to decrease the performance of the whole web page and should not be used for establishing any performance benchmark. The variable is there only to allow you to debug some aspects of your web page, when not running the automated test.
