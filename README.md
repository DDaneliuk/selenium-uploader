# Selenium NFT Uploader
## Bypass recaptcha v2
Test script for bypass recaptcha v2. Using Chrome extension.

![](https://github.com/DDaneliuk/selenium-uploader/blob/main/recaptcher.gif?raw=true)
After click on checkbox open a second ```iframe``` with 
images where we can find solver icon. Problem is to click on it (Because this extension use shadow dom which is closed).
Solving this issue I use selenium ```ActionChains``` for click by coordinate.

![](https://raw.githubusercontent.com/DDaneliuk/selenium-uploader/main/src/examples/shadow-example.png)

