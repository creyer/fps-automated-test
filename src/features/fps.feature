Feature: Fps avarage
    In order to have a nice user experience 
    the fps on the page should be over 25
Scenario: Visit a page and extract the fps when scrolling
Given I have initial setup: Firefox
     When I go to login page
     And I insert the fps javascript
     And I fill in the credentials fields "id_username" "id_password"
     And I submit
     And I go to the check page 
     And I insert the fps javascript
     And I scroll 50 times to ensure data is loaded
     And I scroll again to extract the fps values
     Then the avarage fps valus should be over 25
