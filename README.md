# Ha-Sports-Scores

## Yaml and dashboard configuration for Sports Scores.  
I orginally found Kbrowns original code because I was trying to get a sports ticker setup and ran across the community site that he started.  That is why you will see marquee text scrolling on some of the dashboards.  

My goal was to have a single place to look at scores quickly thorugh HA.  This is a work in progress and based on the excellent work Kbrown started and others have contributed to.  I am just riding coat-tails, go to the thread below to see those who are working to make this project great - https://community.home-assistant.io/t/sports-standings-and-scores/547094

I would also encourage reviewing the:
  - HA-Teamtracker Card (https://github.com/vasqued2/ha-teamtracker )
  - Flex-Table card (https://github.com/custom-cards/flex-table-card)
  - Card-mod (https://github.com/thomasloven/lovelace-card-mod)
  - Formula One Card (https://community.home-assistant.io/t/formula-one-card/476902)
    
They are all a part of this project.
           
## Setup vs Kbrowns
My setup has changed from Kbrowns in that he uses Templates (which work for most sports) where I moved most to REST sensors.  The reason was that NCAA conferences sometimes exhausted the limits and wouldn't return anything.  In the sensors directory I have the sensors I populate and are broken out, where possible, by sport.

### Dashboards directory has the following dashboard code: 
- US Sports (NHL/NFL/UFL/MLB/NBA/WNBA/WTA/ATP/PGA/LIV/LPGA)
- There is also a playoffs dashboard.  I have been working to create a bracket format for the sports.  I will continue to refine but this at least gives me something closer to what I am looking for in a bracket.  This will eventually get rolled into their respective sports once I am comfortable with the design.
  - The flow is I grab data from an ESPN endpoint based on the playoff date.  The downside is I will need to manually update the dates each year, but will work on that later.
  - I then filter out the groups by whatever defines that group.  This is done in the Template.yaml. NCAA Mens for example is First Four/West/Midwest/South/East/Sweet 16/Elite 8/Final 4/Championship, NCAA Women's are Regions, NFL is AFC/NFC/etc., and MLB is AL/NL/etc.
  - I then use the Flex-table card probably not how its desined to be used.  I use it as a single customizeable, html column.
  - Screen shots of what each looks like are below.
- Soccer (Premier/Championship/English League 1/English League 2/ENL/Budesliga/Bundesliga2/MSL/NWSL)
- US College NCAA (Mens Football/Mens Basketball)
- March Madness
- Racing - F1/NASCAR

### Playoff Dashboard
- I am working on a Playoff Bracket for the professional teams.
- I have created a holding Sandbox in Dashboards that I have a good collection so far - NCAAM/NCAAW/NFL/MLB/NHL/NBA.
  - NCAAM/NCAAF/NFL/MLB all seem to be working.  A little understanding on how I am getting the brackets filled out.
  - I first call the ESPN API based on the dates of the March Madness/Playoffs/etc.
  - Here is the MLB call from last year that you can find, in this case, in the mlb_sensor.yaml -- resource: https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20241001-20241030
  - You can see the playoff dates at the end - October 1 thru October 30 2024.
  - I then use Templates to break the brackets up by the notes section.  ESPN is awesome by the way.  You can check out the template.yaml to see what I am doing.
  - Now most of you know I don't like Templates for 1 reason.  If you have too much data the Template will max out which causes an error and its empty.  So I normally use a REST sensor instead and filter out what I want.  With the MM/Playoffs API though ESPN doesn't break 
    it out that way, but what they do is essentially put the bracket in the notes section.  So I can filter there.
  - Still with me ;) - Now NCAAM/NCAAF/MLB/NFL work fine - NHL and NBA so far have too much data in the 1st Round.  So I had to create 2 Python Scripts and they are in the Python Files Directory - NBA-1st.py and NHL-1st.py
  - These files filter out the API First Round data and create 2 separate JSON files - East and West First Round - for each sport and put them in the /config/www directory.
  - I then have a REST sensor in each of the sports sensors yaml's (nhl_sensors/nba_sensors) that pull the data out of these json files.  You will see that I call the local IP to run the script and you will need to update this to reflect your IP.  This is what is in there 
    right now for the nba west 1st round: resource:  http://192.168.xxx.xxx:8123/local/nba_west_1st_round.json.
  - The last piece is that I have an automation that calls the python script every 3 mintues during the playoff season.
  - The call the automation makes is a shell command.  I have updated the configuration.yaml with the shell command calls I make.  Here is the NBA example:   get_nba_first_round: 'python /config/www/nba-1st.py'
  - Here is what my NHL automation looks like:
    ```
     alias: NHL 1st Round
     description: ""
     triggers:
       - minutes: /3
         trigger: time_pattern
     conditions:
       - condition: time
         after: "00:00:00"
         before: "23:59:59"
       - condition: template
         value_template: >
           {{ now().date() >= as_datetime('2025-04-17').date() and now().date() <=
           as_datetime('2025-06-23').date() }}
     actions:
       - data: {}
         action: shell_command.get_nhl_first_round
       - data: {}
         action: shell_command.get_nhl_first_round_grok
     mode: single
    ```
- That's it but here is a summarized flow for NBA/NHL:
   - Automation during the playoffs makes a call every 3 mintues to the Python Script that Calls the NHL/NBA API
   - 2 JSON files are created/updated for East/West 1st Rounds
   - Sports sensor is monitoring this file and updates on chages
   - dashboard is populated with sensor data.
### Playoff Dashboard - GROK'd
- So I didn't like the layout of the playoffs dashboard.  The code is still there but I wanted to have something that was more logical.  So for fun I spoke with GROK.
- All of the grok files have grok in them - Grok Dashboard, Grok callouts in the sensors, grok python file names, etc.
- I have differenct python files for the Grok dashboard but they basically do the same thing.  I tested them against last years data, so as long as nothing changes it should work.  I have left the links to the previous year's api call.  To test you can just comment out this years and remove the comment from last years.
- I was playing with College Baseball and that is why you see the beginnings of that.  I ran into something strage with the calls on that one.  To get the different playoffs I had to make separate date calls.  When I tried to grab all of the API data from ESPN it didn't include it.  GUessing therre is a limit ESPN has, but if I break them out like I did in the files it works.
- Anyway, I'll work on that maybe and will watch the sensors for this years playoffs in NHL/NBA.
- You get an idea of where I was going with the image below.
### Sensors directory has the following sesnsor yaml's broken up by sport: 
- US Sports
  - nhl_sensors.yaml
  - nfl_sensors.yaml
  - ufl_sensors.yaml
  - mlb_sensors.yaml
  - nba_sensors.yaml
  - wnba_sensors.yaml
- Tennis
  - tennis.yaml
- Golf
  - golf.yaml
- Soccer
  - soccer_sensors.yaml includes all -Premier/Championship/English League 1/English League 2/ENL/Budesliga/Bundesliga2/MSL/NWSL (San Diego added to MLS/soccer.yaml 2/20/25)
- US College NCAA
  - ncaaf_sensors.yaml (Men's Football)
  - ncaam_sensors.yaml (Men's Basketball)
  - ncaaw_sensors.yaml (Women's Basketball)
- Racing
  - racing_sensors.yaml (F1/NASCAR)


  
### Template.yaml
I also have template.yaml that is used for items that I haven't converted yet or need to be in the template.yaml.

### Configuration.yaml to split up individual sensors
I have added the configuration.yaml section that I use to call the sensors.

### Sandbox
I create Sandbox dashboards to test what I am trying to create without messing up my existing dashboards.  Because of that I have also included the sandbox code I use and you will see in the sensors/dashboards.  Some of it is commented out, some isn't used, and some are placeholders.  I am including the code because I am lazy ;) and figured some may want to explore some of the items I have done.

### Troubleshooting
Lots of good info in the thread above on trouble-shooting and I may add more later.

What I will say is when you run into problems try to figure where some of the basics firsts.
1. Make sure that the configuration yamls are correct and check your logs.  HA needs everything pretty and will let you know in logs (most of the time) where it is having a problem.
2. Double-check your configuration against my config, kbrown's or others that may have contributed to the community thread above.
3. Use the Home Assistant Developer tools (states and template) mostly to check your sensors and see if the data is in the sensor and use template to test code if it isn't showing up in your dashboard.
   ![image](https://github.com/user-attachments/assets/7594977f-8e22-4c73-9988-e5a324181485)
   Here is an example when I wanted to scroll the data that was included in the nhl_starting_goalies sensor and I wanted to see how it was formatted and if it was there so I tested in the Template first.
   ![image](https://github.com/user-attachments/assets/ef3367b7-24fa-4f68-bcbf-8b7bd78caa83)
   You can see that I am using that data with marquee wrapped around to scroll across the header
   ![image](https://github.com/user-attachments/assets/31ca9dfb-bc37-4102-ac53-2eed7c740eaf)

5. If there isn't data in the sensor but you know it is setup correctly, take a look at Settings->Devices & Services->Entities.  You can see if there is an error or possibly a duplicate.  There have been times that I made a change and HA created a 2nd, duplicate sensor and threw a _2 at the end of it.  If this happens, delete the original and then go in and edit the entity and remove the _2.
   Here is what an error looks like as an example
   ![image](https://github.com/user-attachments/assets/20d56dc5-4b5e-4932-8719-b53bd70fb886)
6. Be patient on the intial load - if may take a bit to populate the sensors the first time.
7. Sometimes ESPN changes their formatting and you will most likely need to go in and change the decluttering template.
8. Ask questions on the community but please use the formatting tools for your code, and show what isn't working.  A bunch of us can test quickly in our environment and possibly help.
9. 99% of the people on the community want to help.  Harsh words may be language translation thing or if they are being mean the village normally rises up.

### Pictures
Here are a couple pics of the dashboards that use the code in the dashboard and sensors directories.  Feel free to pull anything out of it you don't need or won't use:

![image](https://github.com/user-attachments/assets/6424c963-fbe8-49f3-8fa2-9ce729889c79)
![image](https://github.com/user-attachments/assets/f420e4c7-e26a-4705-a805-1a983c972a6d)
![image](https://github.com/user-attachments/assets/6f5bc9eb-6a67-444a-bcff-a70020db93a2)
![image](https://github.com/user-attachments/assets/62adf59c-5f28-481e-80a4-675d863c0617)
![image](https://github.com/user-attachments/assets/ad30e6da-c7e0-407c-80f1-dc452e9d01b1)
![image](https://github.com/user-attachments/assets/7e43400f-8dc7-48f6-baff-a0b320227f71)
![image](https://github.com/user-attachments/assets/8a3abe26-048f-4eec-99f2-58b89ebfbd94)
![image](https://github.com/user-attachments/assets/02ad26b9-35ed-48d3-b5ed-7f8113823e5a)
![image](https://github.com/user-attachments/assets/7a2c1ec1-0b48-4570-bf90-960a47bf6ef8)






![image](https://github.com/user-attachments/assets/b37e0bed-0c38-45ed-80ae-e08d5a85f11f)
![image](https://github.com/user-attachments/assets/5ee2a06c-c46a-4496-b5a1-41ef5be23d08)
