# Peloton Tracking Widget

## Summary
Using Python, Windows Task Scheduler, Google Sheets, and the app Widgetify I am able to automatically pull workout data from Peloton, populate a Google Sheet, update a dashboard, and display it to my phone's home screen. My partner and I use this to compete against one another to see who can produce the most kilojoules each week and work together to meet our goal of 5,000 combined kilojoules regularly.

## Details
I created a python script which requires the use of our Peloton credentials and my Google credentials to pull all the workout history for each of us. After pulling this data, it writes any new rows of data to the bottom of the Google Sheet. A simple .bat file inconjunction with Windows Task Scheduler allows me to automatically run this python script every day.

A second tab is a custom dashboard which tracks our weekly and 5,000kj goal. Using Sheet's "Publish to Web" feature, I am able to publish an image of this dashboard to the web. Then using the app Widgetify, I can display this webpoage to my homescreen.

![Screenshot_20250303_164800_One UI Home~2](https://github.com/user-attachments/assets/96fcf23c-b9f6-475d-8b6e-d2784fd89919)
