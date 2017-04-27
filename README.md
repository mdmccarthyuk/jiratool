# jiratool
A tool to query Jira via the REST API. 

Usage
Create a config.json similar to the following:
{
  "config": {
    "user" : "USER.NAME",
    "pass" : "PASSW0RD",
    "url" : "https://jira.endpoint.url/api/2"
  }
}

Example usage:
./jira.py query -q "assignee=mike&maxItems=5"
Output is currently returned as JSON. 
