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
- Soccer (Premier/Championship/English League 1/English League 2/ENL/Budesliga/Bundesliga2/MSL/NWSL)
- US College NCAA (Mens Football/Mens Basketball)
- Racing - F1/NASCAR

### Sensors directory has the following sesnsor yaml's broken up by sport: 
- US Sports
  - nhl_sensors.yaml
  - nfl_sensors.yaml
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
  - ncaaf_sensors.yaml (Mens Football)
  - ncaam_sensors.yaml (Mens Basketball)
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
![image](https://github.com/user-attachments/assets/b37e0bed-0c38-45ed-80ae-e08d5a85f11f)
![image](https://github.com/user-attachments/assets/5ee2a06c-c46a-4496-b5a1-41ef5be23d08)



<html xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:x="urn:schemas-microsoft-com:office:excel"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta name=ProgId content=Excel.Sheet>
<meta name=Generator content="Microsoft Excel 15">
<link id=Main-File rel=Main-File href="../espnapi.htm">
<link rel=File-List href=filelist.xml>
<link rel=Stylesheet href=stylesheet.css>
<style>
<!--table
	{mso-displayed-decimal-separator:"\.";
	mso-displayed-thousand-separator:"\,";}
@page
	{margin:.75in .7in .75in .7in;
	mso-header-margin:.3in;
	mso-footer-margin:.3in;}
-->
</style>
<![if !supportTabStrip]><script language="JavaScript">
<!--
function fnUpdateTabs()
 {
  if (parent.window.g_iIEVer>=4) {
   if (parent.document.readyState=="complete"
    && parent.frames['frTabs'].document.readyState=="complete")
   parent.fnSetActiveSheet(0);
  else
   window.setTimeout("fnUpdateTabs();",150);
 }
}

if (window.name!="frSheet")
 window.location.replace("../espnapi.htm");
else
 fnUpdateTabs();
//-->
</script>
<![endif]>
</head>

<body link="#467886" vlink="#96607D">

<table border=0 cellpadding=0 cellspacing=0 width=1682 style='border-collapse:
 collapse;table-layout:fixed;width:1262pt'>
 <col width=64 span=4 style='width:48pt'>
 <col width=211 style='mso-width-source:userset;mso-width-alt:7716;width:158pt'>
 <col width=818 style='mso-width-source:userset;mso-width-alt:29915;width:614pt'>
 <col width=256 style='mso-width-source:userset;mso-width-alt:9362;width:192pt'>
 <col width=74 style='mso-width-source:userset;mso-width-alt:2706;width:56pt'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2450;width:50pt'>
 <tr height=20 style='height:15.0pt'>
  <td height=20 width=64 style='height:15.0pt;width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=211 style='width:158pt'></td>
  <td width=818 style='width:614pt'></td>
  <td width=256 style='width:192pt'></td>
  <td width=74 style='width:56pt'></td>
  <td width=67 style='width:50pt'></td>
 </tr>
 <tr height=80 style='height:60.0pt;mso-xlrowspan:4'>
  <td height=80 colspan=9 style='height:60.0pt;mso-ignore:colspan'></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td class=xl65>Leagues</td>
  <td class=xl65>&nbsp;</td>
  <td class=xl65>League</td>
  <td class=xl65>Active</td>
  <td class=xl65>Notes</td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>afc.champions</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/afc.champions/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>AFC Champions League Elite</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>afc.cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/afc.cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>AFC Champions League Two</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>afc.cupq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/afc.cupq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>AFC Asian Cup Qualifiers</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>aff.championship</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/aff.championship/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>ASEAN Championship</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Argentine Liga Profesional de Fútbol</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Argentine Nacional B</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.3</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.3/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Argentine Primera B</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.4</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.4/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Argentine Primera C</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.5</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.5/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Argentine Primera D</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.copa</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.copa/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>arg.urba</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/arg.urba/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>aus.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/aus.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Australian A-League Men</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>aut.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/aut.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Austrian Bundesliga</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>bel.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/bel.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Belgian Pro League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>bol.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/bol.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Bolivian Liga Profesional</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>bra.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/bra.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Brazilian Serie A</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>bra.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/bra.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Brazilian Serie B</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>bra.3</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/bra.3/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Brazilian Serie C</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>caf.nations</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/caf.nations/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Africa Cup of Nations</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>chi.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/chi.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Chilean Primera División</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>chi.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/chi.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Segunda División de Chile</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>col.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/col.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Colombian Primera A</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>col.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/col.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Colombian Primera B</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>concaaf.champions_cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/concaaf.champions_cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>concacaf.champions</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.champions/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Concacaf Champions Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>concacaf.golf</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.golf/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>concacaf.superliga</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.superliga/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>North American SuperLiga</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>concacaf.u23</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.u23/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>CONCACAF U23 Tournament</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>conmebol.america</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.america/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Copa América</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>conmebol.libertadores</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.libertadores/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>CONMEBOL Libertadores</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>conmebol.sudamericana</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.sudamericana/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>CONMEBOL Sudamericana</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>conmebol.sudamericano_sub20</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.sudamericano_sub20/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>CONMEBOL Sudamericano Sub-20</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>crc.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/crc.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Costa Rican Primera Division</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>den.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/den.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Danish Superliga</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ecu.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ecu.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>LigaPro Ecuador</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ecu.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ecu.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Ecuador Serie B</td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>eng.charity</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/eng.charity/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>English FA Community Shield</td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>eng.fa</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/eng.fa/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>English FA Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>eng.trophy</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/eng.trophy/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>eng.w.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/eng.w.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>English Women's Super League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>eng.worthington</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/eng.worthington/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>esp.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/esp.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Spanish LALIGA 2</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>esp.copa_del_rey</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/esp.copa_del_rey/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Spanish Copa del Rey</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>esp.super_cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/esp.super_cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Spanish Supercopa</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.ofc</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.ofc/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA World Cup Qualifying - OFC</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.confederations</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.confederations/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA Confederations Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.cwc</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.cwc/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA Club World Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.friendly</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.friendly/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Men's International Friendly</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.friendly.w</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.friendly.w/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Women's International Friendly</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.olympics</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.olympics/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Men's Olympic Soccer Tournament</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.olympicsq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.olympicsq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.w.algarve</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.algarve/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Algarve Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.w.olympics</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.olympics/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Women's Olympic Soccer Tournament</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.w.olympicsq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.olympicsq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.world</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA World Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.world.u17</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world.u17/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA Under-17 World Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.world.u20</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world.u20/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA Under-20 World Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>World Cup Qualifying</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.afc</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.afc/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.caf</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.caf/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.concacaf</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.concacaf/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.conmebol</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.conmebol/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.worldq.uefa</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.uefa/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.wwc</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.wwc/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>FIFA Women's World Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fifa.wyc</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.wyc/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td></td>
  <td>x</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fra.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fra.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>French Ligue 1</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fra.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fra.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>French Ligue 2</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fra.coupe_de_france</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fra.coupe_de_france/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Coupe de France</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>fra.coupe_de_la_ligue</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/fra.coupe_de_la_ligue/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>French Coupe de la Ligue</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ger.dfb_pokal</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ger.dfb_pokal/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>German Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ger.super_cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ger.super_cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>German DFL-Supercup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>global.world_football_challenge</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/global.world_football_challenge/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>WORLD FOOTBALL CHALLENGE</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>gre.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/gre.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Greek Super League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>gua.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/gua.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Guatemalan Liga Nacional</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>hon.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/hon.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Honduran Liga Nacional</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>intercontinental</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/intercontinental/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Intercontinental Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>irl.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/irl.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Irish Premier Division</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ita.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ita.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Italian Serie B</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ita.coppa_italia</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ita.coppa_italia/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Coppa Italia</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ita.super_cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ita.super_cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Italian Supercoppa</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>jpn.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/jpn.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Japanese J.League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>mex.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/mex.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Mexican Liga de Expansión MX</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>mex.interliga</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/mex.interliga/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Torneo Interliga de México</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ned.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ned.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Dutch Eredivisie</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ned.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ned.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Dutch Keuken Kampioen Divisie</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ned.cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ned.cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Dutch KNVB Beker</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>nir.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/nir.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Northern Irish Premiership</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>nor.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/nor.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Norwegian Eliteserien</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>panam.m</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/panam.m/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Pan Am Men's Soccer</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>panam.w</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/panam.w/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Pan Am women's Soccer</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>par.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/par.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Paraguayan Primera División</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>par.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/par.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Segunda División de Paraguay</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>per.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/per.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Peruvian Liga 1</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>per.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/per.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Segunda División de Perú</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>por.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/por.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Portuguese Primeira Liga</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>rsa.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/rsa.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>South African Premier Division</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>rsa.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/rsa.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>South African First Division</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>rus.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/rus.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Russian Premier League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish Premiership</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish Championship</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.3</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.3/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish SPFL League One</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.4</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.4/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish SPFL League Two</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.challenge</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.challenge/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish League Challenge Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.cis</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.cis/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish League Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sco.tennents</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sco.tennents/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td>Scottish Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>slv.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/slv.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Salvadoran Primera Division</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>sui.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/sui.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Swiss Super League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>swe.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/swe.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Swedish Allsvenskan</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>tur.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/tur.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Turkish Super Lig</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.carling</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.carling/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Carling Nations Cup</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.euro</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euro/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA European Championship</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.euro.u19</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euro.u19/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA European Under-19 Championship</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.europa</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.europa/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA Europa League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.euroq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euroq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA European Championship Qualifying</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.intertoto</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.intertoto/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA Intertoto Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.super_cup</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.super_cup/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA Super Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.uefa</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.uefa/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA Cup</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.worldq</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.worldq/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>UEFA World Cup Qualifying</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uefa.wchampions</td>
  <td class=xl67><a
  href="https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.wchampions/standings?seasontype=2&amp;type=0&amp;level=3"
  target="_parent">https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.wchampions/standings?seasontype=2&amp;type=0&amp;level=3</a></td>
  <td class=xl66>UEFA Women's Champions League</td>
  <td colspan=2 style='mso-ignore:colspan'></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uru.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uru.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Liga UAF Uruguaya</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>uru.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/uru.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Segunda División de Uruguay</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.misl</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.misl/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>&quot;Major Indoor Soccer League</td>
  <td>?</td>
  <td>Dissolved</td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.ncaa.m.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.ncaa.m.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>NCAA Men's Soccer</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.ncaa.w.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.ncaa.w.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>NCAA Women's Soccer</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.open</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.open/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>U.S. Open Cup</td>
  <td colspan=2 style='mso-ignore:colspan'></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.usl.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.usl.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>USL Championship</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.usl.l1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.usl.l1/standings?seasontype=2&amp;type=0&amp;level=3</td>
  <td class=xl66>USL League One</td>
  <td colspan=2 style='mso-ignore:colspan'></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.w.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.w.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>USA Women's United Soccer Association</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>usa.world_series</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/usa.world_series/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>World Series of Football</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ven.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ven.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Venezuelan Primera División</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>ven.2</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/ven.2/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Segunda División de Venezuela</td>
  <td>?</td>
  <td></td>
 </tr>
 <tr height=20 style='height:15.0pt'>
  <td height=20 colspan=4 style='height:15.0pt;mso-ignore:colspan'></td>
  <td>wal.1</td>
  <td>https://site.web.api.espn.com/apis/v2/sports/soccer/wal.1/standings?seasontype=1&amp;type=0&amp;level=3</td>
  <td class=xl66>Welsh Premier League</td>
  <td>Active 2025</td>
  <td></td>
 </tr>
 <![if supportMisalignedColumns]>
 <tr height=0 style='display:none'>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=211 style='width:158pt'></td>
  <td width=818 style='width:614pt'></td>
  <td width=256 style='width:192pt'></td>
  <td width=74 style='width:56pt'></td>
  <td width=67 style='width:50pt'></td>
 </tr>
 <![endif]>
</table>

</body>

</html>




