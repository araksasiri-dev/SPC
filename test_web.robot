*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Login To System Test
    Log    Starting the browser test...
    Open Browser    https://www.google.com    chrome
    Maximize Browser Window
    Title Should Be    Google
    Log    Test passed successfully!
    Close Browser