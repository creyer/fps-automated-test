# Please consider the following:
# 1. This script needs to be changed in order to satisfy your html
#    please modify the @step(u'And I scroll (\d+) times to ensure data is loaded')
# 2. This script is build to acomodate a page with multiple scrolling
#    elements and with eventually ajax loading
# 3. In order to work, the opened browser page should be keep maximized
# 4. The script is using a mouse over selenium method to perform scrolling
#    This method I have found it to give results closer to reality, as
#    ussualy people tend to scroll with the mouse weel, which eventually
#    has also a mouse over event (and also mouse out)

from lettuce import before, world, step
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import numpy
from perf_util import predefined
from selenium.webdriver.chrome.options import Options



@before.all
def setup_():
    logging.basicConfig(filename='perf.log',level=logging.INFO)


@step(u'I have initial setup: ([^"]*)')
def parse_params_of_argv(step, browser):
    #add here any other setup you want
    if (browser.lower() == "chrome"):
        logging.info("Start new test with Chrome")
        chromedriver = predefined['chromedriver']
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # next line it can be used together with setting the javascript
        # value of useHighAnimation to true, for debug purpose only
        # options.add_argument("--show-fps-counter=true")
        world.driver = webdriver.Chrome(executable_path = chromedriver, \
            chrome_options = options)

    elif (browser.lower() == "firefox"):
        world.driver = webdriver.Firefox()
        world.driver.maximize_window()
        logging.info("Start new test with Firefox")

    else:
       logging.info("Unsupported browser: %s" % (browser))
       raise Exception("Unsupported browser: %s" % (browser))


@step(u'I go to the check page')
def submit_pass(step):
    world.driver.get(predefined['check_url'])
    world.driver.execute_script('window.focus();')
    # wait for all to load
    time.sleep(10)


@step(u'I insert the fps javascript')
def javascript_insert_pass(step):
    # insert the magic javascript
    with open(predefined['local_javascript_url']) as f:
        content = f.readlines()
    js = "".join(content)
    javascript = "\
        var doc = window.document;\
        var script = doc.createElement(\"script\");\
        script.innerHTML=\"%s\";\
        doc.body.appendChild(script);" % (js.strip()\
            .replace('\t','').replace("\n", "").replace('"','\\"'))
    #logging.info("javascript = "+javascript)
    world.driver.execute_script(javascript)


@step(u'I scroll (\d+) times to ensure data is loaded')
def scroll(step, times):
    #perform initial scrolling
    for x in range(0, int(times)):
        for div in range (0,predefined['number_of_widgets']):
            world.driver.execute_script('window.scroll(0, %d)' % (x * predefined['scroll_step']))
            logging.info("scrolling widget: %d for %d time" % (div, x))
            time.sleep(0.01)

    elems = []
    #insert id on each element for easy retrieval
    for div in range (0,predefined['number_of_widgets']):
        elems.append(world.driver.execute_script('return document.\
            getElementById("stream-items-id").\
            children.length'))
        for li in range(0, elems[div]):
            world.driver.execute_script('document.getElementById("stream-items-id").\
                children[%d].getElementsByTagName("div")[0].id = "div_scroll_%d"' % (li,li))
        logging.info("number of elements in widget[%d]: %d" % (div, elems[div]))

    #extract the elements we need to hover over
    li_hover = []
    heights = []
    for div in range (0,predefined['number_of_widgets']):
        li_hover.append([])
        heights.append([])
        for li in range(0, elems[div]):
            element_to_hover_over = world.driver.find_element_by_id("div_scroll_%d" % (li))
            li_hover[div].append(element_to_hover_over)
            heights[div].append(world.driver.execute_script('return document.getElementById("stream-items-id").\
                children[%d].offsetHeight' % (li)))
    world.elems = elems
    world.li_hover = li_hover
    world.heights = heights


@step(u'I scroll again to extract the fps values')
def fps_values(step):
    elems = world.elems
    li_hover = world.li_hover
    sleep = 0
    #start logging the fps values
    world.driver.execute_script('insertIntoFpsArr = true');
    for div in range (0,predefined['number_of_widgets']):
        # we will split by 4 as the tweets are usualy small so a scroll it will
        # move more tweets in one move
        for li in range(0, elems[div]-1):
            ActionChains(world.driver).move_to_element(li_hover[div][li]).perform()
            # add a minimum sleep give time to perform
            # here is a trial mimic of a normal user which actualy has
            # a small pause between scrols
            time.sleep(.3)
            world.driver.execute_script('window.scrollBy(0,%s) ' % (world.heights[div][li]))
    #read the fps values
    world.fps_values = world.driver.execute_script("return fps_arr")


@step(u'the avarage fps valus should be over (\d+)')
def avarage_lookup(step,avg):
    mean = numpy.mean(world.fps_values)
    std = numpy.std(world.fps_values)
    # std could be check to ensure we don't have a large spread data
    # but Firefox has a much larger value the Chrome for std
    logging.info("numpy mean: %s ,std: %s" % (mean,std))
    logging.info("values are: %s " % (world.fps_values))
    #world.driver.close()
    assert mean > int(avg)


