# bitbar_jira_client_gui
gui for the bitbar_jira_client argos script

it's using the bitbar_jira script
https://github.com/bycym/bitbar_jira_client.git

The configuration is in this repostory under the bitbar_jira_client folder.
More information on [this repository](https://github.com/bycym/bitbar_jira_client.git).

![bitbar jira client](/main_python_jira_gui.png?raw=true "Optional Title")

requirements:
```
python3 
pip3 install jira
or
pip3 install jira-client

pip3 install tkinter
```

Create an API token here for password: 
https://id.atlassian.com/manage/api-tokens


connection:
```py
USER="<jira_user>@email"
PASSW="<jira_api_token>"
SERVER="<jira_server>"
TOPRECENT=10
```

example:
```py
USER="foo.foo@mymail.com"
PASSW="th1s1s4n4p1t0k3n"
SERVER="https://myserver.atlassian.net"
TOPRECENT=10
```
