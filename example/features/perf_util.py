predifined = {}
#we test the page without the log in
predifined['id_username'] = "" 
predifined['id_password'] = ""
# define the login page
predifined['login_url'] = ""

# define local javascript for loading the file from local
predifined['local_javascript_url'] = "javascript/local_perf.js"



# define the check page
predifined['check_url'] = "https://twitter.com/google"

#define how many widgets you wish to scroll
predifined['number_of_widgets'] = 1

#define the step you wish to perform the initial scroll
predifined['scroll_step'] = 162 # this is the number of px

#we will use firfox
predifined['chromedriver'] = ""

# TODO create remote javascript
