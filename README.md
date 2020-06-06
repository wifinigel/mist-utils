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

Pull (clone or download the zip file) the repo from GitHub and execute the scripts you require.

Note: you need to set your Mist API token in the env var MIST_TOKEN to use these scripts.

# Using the Mist API Overview

The Mist API allows you to perform a whole variety of operations on your organisation's Mist network instead of using their cloud dashboard.

This allows incredible flexibility if you would like to perform your own network automation on your network.

The examples provided in this repository demonstrate how to pull data from the network to provide status and reporting information. The target audience I had in mind when writing these scripts is very much network engineers who would like to pull of data to include in reports and documentation.

The scripts are written in Python as everyone tells me a I need to be able to code and Python is the flavour of the moment.

## How We Pull Data Via An API ?

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
  Token Nm3A2LkqTlgm8eDhnsZUjeJjdeuw6EAzvsoTgCYxtnkv51A2bcfjiGkAZB8QSgD3LCWeSzaHyeeyLFjouG6Ek7YroOcW1h
```

When the request is received by the mist API (at api.mist.com), it checks the token to see if it is valid and will then provide the appropriate access policy for that token. It will allow permissions such as read or write access, and will determine which organisations and sites may be accessed by the API call.

(Note this repo is under development)
