predefined = {}
#we test the page without the log in
predefined['id_username'] = ""
predefined['id_password'] = ""
# define the login page
predefined['login_url'] = ""

# define local javascript for loading the file from local
predefined['local_javascript_url'] = "javascript/local_perf.js"



# define the check page
predefined['check_url'] = "https://twitter.com/google"

#define how many widgets you wish to scroll
predefined['number_of_widgets'] = 1

#define the step you wish to perform the initial scroll
predefined['scroll_step'] = 162 # this is the number of px

#we will use firfox
predefined['chromedriver'] = ""

# TODO create remote javascript
