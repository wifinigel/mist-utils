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

(Note this repo is under development)
