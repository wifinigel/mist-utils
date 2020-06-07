# Mist-Utils

A few Mist utilities I'm creating while learning more about the Mist API. I'm trying to build a collection of scripts that can be run by an engineer to list or dump useful data.


# Useful resources:

* Mist public repo: https://github.com/mistsys/mist-public
* Mist API docs: https://api.mist.com/api/v1/docs/Home
* Postman API guide: https://documenter.getpostman.com/view/224925/SzYgQufe?version=latest#8a365e04-2121-48c9-b141-f32ea8582b1a
* Mist API sandbox class: https://api-class.mist.com/
* Mist online training: https://courses.mist.com/dashboard
* Test webhook output: http://requestbin.net/

# Scripts:

* aps_org_dump_to_csv.py - dump an org's AP info in to a CSV file
* aps_site_dump_to_csv.py - dump an site's AP info in to a CSV file
* check_env.py - check if our env is set up to use the Mist API
* clients_list_site_apple.py - list Apple clients on a site
* clients_list_site_apple_to_csv.py - dump all Apple clients on a site to a CSV file
* token_create.py - create an API token
* token_lisy.py - list the token we currently have created
* simple_summary.py - very simple overview listing of your org
* token_tidy.py - tidy up our tokens by removing all except the token we are currently using

# Usage

To use these scripts, you'll need to get your environment set up to run the scripts against your Mist network API.

You'll need to do the following steps (which are all detailed in this document):

1. Get an API token
2. Set you environment to use the token
3. Install Python 3 (if don;t already have it)
4. Download the scripts
5. test your environment works with the API
6. Run the scripts

I'm assuming you have a Mist cloud dashboard account and an online AP or two to be able to perform the steps detailed in this document.

# Mist API Overview

The Mist API allows you to perform a whole variety of operations on your organisation's Mist network instead of using their cloud dashboard.

This allows incredible flexibility if you would like to perform automation on your network.

The examples provided in this repository demonstrate how to pull data from the network to provide status and reporting information. The target audience I had in mind when writing these scripts is very much network engineers who would like to pull off infrastructure data to include in reports and documentation.

The scripts are written in Python as everyone tells me a I need to be able to code and Python is the flavour of the moment.

## How Do We Pull Data Via An API ?

The API allows us to read, write, update and delete data on our network. We'll be primarily reading data, as that is the safest option when we're sending API requests in to our network. I'll leave you to explore writing, updating and deleting stuff yourself...I don't fancy being responsible for giving you tools that may damage your network (...yes I'm a coward like that).

To perform any sort of API operations, we need to send a http request to the API URL of the Mist cloud. You can think of this as being very similar to the operation we perform with a web browser when we pull pages from a web site. But, instead of using a browser, we use a Python script to send a https request, and, we get data back rather than a web page. The operations of a browser talking to a web page and a Python script pulling data from the Mist API site are outlined in the image below:

![http_get_image](images/http_get.png)

## Authentication Token

When we use http to pull data with a Python script, we need to ensure that only authorized people can send requests to the API and retrieve our network data or potentially make configuration changes.

One way of authenticating any requests we send to the Mist API is to send our username and password with each request to verify our identity and that we are authorized to perform the request operation (such as getting a list of all APs on one of our network sites). However this is programmatically challenging and if the credentials are inadvertently revealed (e.g. they are seen by a third party), the may be easily recorded and used to provide unauthorized access. 

A preferred method is to use an authentication token string. This is a very long randomised string of characters that cannot be remembered if seen and can be easily revoked and replace with a new token created if required. The token is used in place of username/password credentials when making requests to the API.

A token looks something like this:

```
    Nm3A2LkqTlgm8eDhnsZUjeJjdeuw6EAzvsoTgCYxtnkv51A2bcfjiGkAZB8QSgD3LCWeSzaHyeeyLFjouG6Ek7YroOcW1h
```

When a http request is set to a web server of API, a number of "headers" are sent with the request. These can contain a variety f data such a as cookies and information about the web client (e.g. the browser type). When we are making an API call to the Mist cloud, we have to include the token as header in the format of :

```
  Authorization: Token Nm3A2LkqTlgm8eDhnsZUjeJjdeuw6EAzvsoTgCYxtnkv51A2bcfjiGkAZB8QSgD3LCWeSzaHyeeyLFjouG6Ek7YroOcW1h
```

(Note the handling of the token in headers is taken care of automatically in the scripts in this repo once you have created your own token, so don't worry too much about this detail.)

When the request is received by the mist API (at api.mist.com), it checks the token to see if it is valid and will then provide the appropriate access policy for that token. It will allow permissions such as read or write access, and will determine which organisations and sites may be accessed by the API call.

### Getting an Authentication Token

To create a token to use with scripts that perform operations via the Mist API, we need to login to the Mist dashboard with our username and password.  

Next, perform the following steps:

1. Login to the Mist dashboard with a browser

2. Open a new tab in your browser

3. Enter the following URL in your browser: https://api.mist.com/api/v1/self/apitokens

4. Assuming you are correctly logged in to your Mist site, you will see a page similar to this:

![no_tokens_image](images/no_tokens.png)

5. This page shows us the token we have associated with our account. It should look like the image above (with an empty pair of square brackets in the upper highlighted area), assuming you have not created any token previously.

6. Next we need to create a token by hitting the "Post" button highlighted in the image above. This will create a token for us.

7. Now, we will see the token that as been generated for us. NOTE: You will only see this token once, so make sure you copy and paste it to somewhere safe. There is no way of retrieving a token later, the only option will to be generate a new token if you lose this one. The token field is shown in the image below. The value you need to save is the long string beginning 'CYbLfqGt' highlighted in the blue rectangle in the image below:

![no_tokens_image](images/token.png)

### Using The Authentication Token

Now that we have an authentication token we can use it to provide authentication to the Mist cloud for our script operations.

The token created will be subject to the same access restrictions as our Mist dashboard account. For instance, if you do not have rights to delete APs with your dashboard login, your API token will also not be able to delete APs.

As the API token is a valuable set of credentials that could allow anyone who gets hold of it to access your network, it needs to be protected in the same way as any other credentials. Embedding the credentials in your script is probably not a great idea, as if you share it or it is accessed in some other way then your security is compromised.

A method that I like to use is to configure the token as an user-level environmental variable on the machine I am working on. This allows all of my scripts to access the token value, but it is only available to me. All of the scripts in this repo use this method. Therefore, you must set an environmental variable on your machine called MIST_TOKEN that contains the value of your token. All scripts will look for this value when they run - if it is not present, they will not run.

#### Setting the Env Var Token Value On A Mac

Temporarily setting the value in a terminal window:

1. Open a terminal window
2. Enter the command:
```
MIST_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(where the xxxxx is replaced with your token string)
```
3. Test it is set by executing the command (the configured token string should be shown):
```
echo $MIST_TOKEN
```

(Note, each time you close your terminal window, this will need to be repeated)

Permanently set the env var for all terminal windows you open:

1. Open a terminal window
2. Edit the file .profile using the Nano text editor:
```
nano .profile
```
3. Add the following line at the bottom of the file
```
MIST_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(where the xxxxx is replaced with your token string)
```
4. Save the file using ctrl-x
5. Close the terminal window and open a new one. Enter the following command to verify that the env var is set:
```
echo $MIST_TOKEN
```

#### Setting the Env Var Token Value On A Windows Machine

Temporarily setting the value in a command window:

1. Open a command window (i.e. CMD)
2. Enter the command:
```
set MIST_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(where the xxxxx is replaced with your token string)
```
3. Test it is set by executing the command (the configured token string should be shown):
```
echo %MIST_TOKEN%
```

(Note, each time you close your command window, this will need to be repeated)

Permanently set the env var for all command windows you open:

1. Click on the Windows start button
2. Type the word "environment"
3. The option "Edit environment variables for your account" should appear in the search results - click on it
4. In the "Environment Variables" panel that appears, we need to create an entry in the upper part of the panel in the user variables section.
5. Hit the 'New' button and enter the env var details are shown below:

![new_var_image](images/new_var.png)

6. Once this has been created, the MIST_TOKEN variable should be shown as in the image below:

![env_vars_image](images/env_vars.png)

7. Open a new command window (i.e. CMD)
8. Check that the env var is available by typing the command:
```
echo %MIST_TOKEN%
```

(Note: this env var will always be available in every command window you open until you remove it from the environment variables panel)

## Getting Python

You will need to have Python 3 installed on your machine to run the scripts in this repo. I cannot go through all of the steps required to do this, but you can get the Python software and installation instructions from : https://www.python.org/downloads/ (get the latest version of 3.x.x).

Once you have installed Python, open a terminal and command window and type the command "python -V" (that's capital 'V') to ensure it is correctly installed (note some platforms may require you to type "python3 -V"). This is a good confidence check that your good to go:

![python_version_image](images/python_version.png)

## Getting The Scripts

There are 2 methods of getting the scripts in this repo:

1. Use git (if you have it installed) using the command 'git clone https://github.com/wifinigel/mist-utils.git'

2. Download a zip file of all the repo files and unzip them on your machine: https://github.com/wifinigel/mist-utils/archive/master.zip

## Running The Scripts

Once you have downloaded the scripts, open a terminal or command windows and change directory to the folder you have created that contains the scripts.

Next, try running the 'check_env.py' script. This will check your environment and connectivity to the Mist cloud:
```
python check_env.py
```

![check_env_image](images/check_env.png)

If this passes all tests, you're good to go! I'll leave you to explore the other scripts yourself and hopefully create your own over time. Enjoy!!!

(Note this repo is under development and additions will be made over time.)
