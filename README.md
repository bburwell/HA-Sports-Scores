# Ha-Sports-Scores

## Yaml and dashboard configuration for Sports Scores.  
I orginally found Kbrowns original code because I was trying to get a sports ticker setup and ran across the community site that he started.  That is why you will see marquee text scrolling on some of the dashboards.  

My goal was to have a single place to look at scores quickly thorugh HA.  This is a work in progress and based on the excellent work Kbrown started and others have contributed to.  I am just riding coat-tails, go to the thread below to see those who are working to make this project great - https://community.home-assistant.io/t/sports-standings-and-scores/547094

I would also encourage reviewing the:
  - HA-Teamtracker Card (https://github.com/vasqued2/ha-teamtracker )
  - Flex-Table card (https://github.com/custom-cards/flex-table-card)
  - Card-mod (https://github.com/thomasloven/lovelace-card-mod)
  - Formula One Card (https://community.home-assistant.io/t/formula-one-card/476902)
    
They are all a big part of this project.
           
## Setup vs Kbrowns
My setup has changed from Kbrowns in that he uses Templates (which work for most sports) where I moved most to REST sensors.  The reason was that NCAA conferences sometimes exhausted the limits and wouldn't return anything.  In the sensors directory I have the sensors I populate and are broken out, where possible, by sport.

### Dashboards directory has the following dashboard code: 
- US Sports (NHL/NFL/NBA/WNBA)
- Soccer (Premier/Championship/English League 1/English League 2/ENL/Budesliga/Bundesliga2/MSL/NWSL)
- US College NCAA (Mens Football/Mens Basketball)
- Racing - F1/NASCAR
  
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
   Here is an example when I wanted to scroll the data that was included in the nhl_starting_goalies sensor.  I tested in the Template first.
   ![image](https://github.com/user-attachments/assets/ef3367b7-24fa-4f68-bcbf-8b7bd78caa83)
   You can see that I am using that datat with marquee wrapped around to scroll across the header
   ![image](https://github.com/user-attachments/assets/31ca9dfb-bc37-4102-ac53-2eed7c740eaf)

5. If there isn't data in the sensor but you know it is setup correctly, take a look at Settings->Devices & Services->Entities.  You can see if there is an error or possibly a duplicate.  There have been times that I made a change and HA created a 2nd, duplicate sensor and threw a _2 at the end of it.  If this happens, delete the original and then go in and edit the entity and remove the _2.
   Here is what an error looks like as an example
   ![image](https://github.com/user-attachments/assets/20d56dc5-4b5e-4932-8719-b53bd70fb886)
6. Be patient on the intial load - if may take a bit to populate the sensors the first time.
7. Sometimes ESPN changes their formatting and you will most like need to go in and change the decluttering template.
8. Ask questions on the community but please use the formatting tools for your code, and show what isn't working.  A bunch of us can test quickly in our environment and possibly help.
9. 99% of the people on the community want to help.  Harsh words may be language translation thing or if they are being mean the village normally rises up.

### Pictures
Here are a couple pics of the dashboards that use the code in the dashboard sensors.  Feel free to pull anything out of it you don't need or won't use:

![image](https://github.com/user-attachments/assets/6424c963-fbe8-49f3-8fa2-9ce729889c79)
![image](https://github.com/user-attachments/assets/f420e4c7-e26a-4705-a805-1a983c972a6d)
![image](https://github.com/user-attachments/assets/6f5bc9eb-6a67-444a-bcff-a70020db93a2)
![image](https://github.com/user-attachments/assets/62adf59c-5f28-481e-80a4-675d863c0617)

