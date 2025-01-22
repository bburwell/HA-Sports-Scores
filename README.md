# Ha-Sports-Scores

## Yaml and dashboard configuration for Sports Scores.  
I orginally found Kbrowns original code because I was trying to get a sports ticker setup and ran across this site.  That is why you will marquee text scrolling on some of the dashboards.  

My goal was to have a single place to look at scores quickly thorugh HA.  This is a work in progress and based on the excellent work Kbrown started and others have contributed to.  I am just riding coat-tails, go to the thread below to see those who are working to make this project great.

Good place for information - https://community.home-assistant.io/t/sports-standings-and-scores/547094

I would also encourage reviewing the:
  - HA-Teamtracker Card (https://github.com/vasqued2/ha-teamtracker )
  - Flex-Table card (https://github.com/custom-cards/flex-table-card)
  - Card-mod (https://github.com/thomasloven/lovelace-card-mod)
  - Formula One Card (https://community.home-assistant.io/t/formula-one-card/476902) they are all a big part of this.
           
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
Lots of good info in the thread above on trouble-shooting and I may add a section here later.

### Pictures
Here are a couple pics of the dashboards:

![image](https://github.com/user-attachments/assets/6424c963-fbe8-49f3-8fa2-9ce729889c79)
![image](https://github.com/user-attachments/assets/f420e4c7-e26a-4705-a805-1a983c972a6d)
![image](https://github.com/user-attachments/assets/6f5bc9eb-6a67-444a-bcff-a70020db93a2)
![image](https://github.com/user-attachments/assets/62adf59c-5f28-481e-80a4-675d863c0617)

