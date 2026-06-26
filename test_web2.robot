*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Search Google Test
    Open Browser    https://www.google.com    chrome
    Input Text    name=q    BizSmartERP
    Press Keys    name=q    ENTER
    Sleep    3s
    Close Browser