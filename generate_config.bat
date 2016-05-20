echo OFF
echo login='' > config.py
echo password='' >> config.py
echo jira_url='' >> config.py
echo custom_names={} >> config.py
echo cache_path='' >> config.py

setx JIRA_CMD "%~dp0" 
