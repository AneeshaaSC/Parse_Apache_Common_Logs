# Parse_Apache_Common_Logs
Imagine that we store our static data files on a single isolated server behind a RESTful API.  Whenever we want to use one of those data files we make an API request to the server and download the file for use.  The data is organised by language, such that a request will be to a URL that can be broken down like this:  https://speechmatics.data.com/English/some_audio_file.wav  https://speechmatics.data.com – this is our base server url (this part will be omitted in logs) English – this is the language the data is being drawn from some_audio_file.wav – this is the actual data file name, which could be anything  We want to monitor our usage of this data server so that we can determine if we can optimise our practices.  To help do this we store access logs for the server in the Apache Common Log Format.  Require a Python program that can parse these logs and produce a standardised report on monthly usage of certain aspects of the server.

Problem specification present in the .docx file
