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

@step(u'I go to login page')
def given_i_go_to_loginpage(step):
    world.driver.get(predefined['login_url'])


@step(u'I fill in the credentials fields "([^"]*)" "([^"]*)"')
def input_user(step, id1,id2):
    world.driver.execute_script('console.timeline()')
    el = world.driver.find_element_by_id(id1)
    el.send_keys(predefined[id1])
    el = world.driver.find_element_by_id(id2)
    el.send_keys(predefined[id2])


@step(u'I submit')
def submit_pass(step):
    button = world.driver.find_element_by_class_name("btn-red")
    button.click()
    world.driver.execute_script('window.focus();')
    # wait for the magic login cookie
    time.sleep(10)


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
            world.driver.execute_script('document.getElementsByClassName\
                ("mention-container-wrapper")[%d].getElementsByClassName("mentions")\
                [0].getElementsByTagName("ul")[0].scrollTop = %d ' % (div,x * predefined['scroll_step']))
            logging.info("scrolling widget: %d for %d time" % (div,x))

    elems = []
    #insert id on each element for easy retrieval
    for div in range (0,predefined['number_of_widgets']):
        elems.append(world.driver.execute_script('return document.\
            getElementsByClassName("mention-container-wrapper")[%d].\
            getElementsByClassName("mentions")[0].getElementsByTagName("ul")[0].\
            children.length' % (div)))
        world.driver.execute_script('document.getElementsByClassName\
                ("mention-container-wrapper")[%d].getElementsByClassName("mentions")\
                [0].getElementsByTagName("ul")[0].id = "ul_scroll_%d"' % (div,div))
        for li in range(0, elems[div]):
            world.driver.execute_script('document.getElementsByClassName\
                ("mention-container-wrapper")[%d].getElementsByClassName("mentions")\
                [0].getElementsByTagName("ul")[0].children[%d].id = "ul_scroll_%d_%d"' % (div,li,div,li))
        logging.info("number of elements in widget[%d]: %d" % (div,elems[div]))

    #extract the elements we need to hover over
    li_hover = []
    for div in range (0,predefined['number_of_widgets']):
        element_to_hover_over = world.driver.find_element_by_id("ul_scroll_%d" % (div))
        li_hover.append([])
        for li in range(0, elems[div]):
            element_to_hover_over = world.driver.find_element_by_id("ul_scroll_%d_%d" % (div,li))
            li_hover[div].append(element_to_hover_over)
    world.elems = elems
    world.li_hover = li_hover


@step(u'I scroll again to extract the fps values')
def fps_values(step):
    elems = world.elems
    li_hover = world.li_hover
    sleep = 0
    #start logging the fps values
    world.driver.execute_script('insertIntoFpsArr = true');
    for div in range (0,predefined['number_of_widgets']):
        for li in range(0, elems[div]-1):
            ActionChains(world.driver).move_to_element(li_hover[div][li]).perform()
            # add a minimum sleep give time to perform
            # here is a trial mimic of a normal user which actualy has
            # a small pause between scrols
            sleep += 1
            if sleep % 3 == 1:
                time.sleep(0.3)
                world.driver.execute_script('document.getElementsByClassName\
                    ("mention-container-wrapper")[%d].getElementsByClassName("mentions")\
                    [0].getElementsByTagName("ul")[0].scrollTop = document.getElementsByClassName\
                    ("mention-container-wrapper")[%d].getElementsByClassName("mentions")\
                    [0].getElementsByTagName("ul")[0].scrollTop + 20 ' % (div, div))
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
    world.driver.close()
    assert mean > int(avg)


