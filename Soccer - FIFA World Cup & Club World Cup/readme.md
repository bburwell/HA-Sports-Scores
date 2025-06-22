Testing Code For World Cup and Club World Cup.  Keeping them here so I don't mess up others that may want to use my existing code.
Lots of moving parts and I am just testing this when I can.
Using Flextable probably not how it really should be used but I feel comfortable with it.
- Setup:
- 2 Python Files call FIFA World Cup (2022 Data) and FIFA Club World Cup (Current 2025).  They create json files that I then use rest sensors to pull the data in.  They basically go through ESPN's API's and then trys to organize them in the  series section of the json.  For testing I have just saved the filed in the config/www directory and then call them from the command line.
- You will need to automate the calls to update during the season.  Automation is not here, you will need to add the python call in configuration.yaml (eg. get_soccer_fifa_worldcup: 'python /config/www/worldcup.py')

** Update 6-22-2025 - Python file now has a few fixes: displayNames being pulled didn't match ESPN API names (fixed), logos weren't matched up correctly in some cases (fixed), Code is updated with changes.

** Added Concacaf Gold Cup


  get_soccer_fifa_club_worldcup: 'python /config/www/fifaclubworldcup.py') like I do with my other sectionns show, and you will need to update the save locations to point to your local directory eg. /config/www/.
- soccer_sensors.yaml has the updates you will need to change the file location's IP address right now they are 192.168.xxx.xxx or should be
- the Dashboard is called Unified World Cup, Club World Cup, NBA, NHL - I eventually plan to try to combine sports
- I have put Group Stage A-H at the top so I can see what is populating and what is not.
- I am trying to highlight those that advance but the logic is off.
- I am sure something will break and feel free to offer any ideas or suggestions - I watch this link more than anything else - https://community.home-assistant.io/t/sports-standings-and-scores/547094 
Here are a couple screen shots:
![image](https://github.com/user-attachments/assets/8eaf3288-404f-4ce1-b052-446a8910b32f)
![image](https://github.com/user-attachments/assets/1d667df7-7773-48c4-9799-eb9641731cba)
![image](https://github.com/user-attachments/assets/893db1ea-534a-4bec-9142-d2de6fdecf42)


