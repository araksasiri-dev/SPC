*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Verify Web And Take Screenshot Test
    Open Browser    https://th.wikipedia.org    chrome
    Maximize Browser Window
    Input Text    id=searchInput    อิตาลี
    Press Keys    id=searchInput    ENTER
    Sleep    2s
    Capture Page Screenshot    wikipedia_result.png
    Close Browser