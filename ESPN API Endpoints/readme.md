# ESPN API Endpoints

## Some Notes
- This document is for informational purposes only, with big thanks to ESPN for providing access to these APIs. The ability to view specific stats while watching ESPN is fantastic.
- You will find various APIs and endpoints listed below.
- Season types vary by sport but share some commonality. For example:

| Sport                | Season Type 1       | Season Type 2         | Season Type 3       | Season Type 4       | Season Type 5       | Season Type 6       |
|-----------------------|---------------------|-----------------------|---------------------|---------------------|---------------------|---------------------|
| Soccer               | Regular Season      | Promotion Semi-Finals | Promotion Final     | -                   | -                   | -                   |
| NFL/College Basketball | Pre-Season         | Regular Season        | Post-Season         | Off-Season          | -                   | -                   |
| College Baseball     | Pre-Season          | Regular Season        | Regionals           | Super-Regionals     | World Series        | Championship Series |
| MLB Baseball         | Pre-Season          | Regular Season        | Post-Season         | Off-Season          | -                   | -                   |

## API Endpoints by Sport

### Baseball
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/baseball/{leagues}/`   | [View Link](https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/standings?seasontype=2&type=0&level=3) | MLB            |
| `/baseball/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard    | MLB            |

### Basketball
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/basketball/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/basketball/nba/standings?seasontype=2&type=0&level=3 | NBA            |
| `/basketball/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/basketball/wnba/standings?seasontype=2&type=0&level=3 | WNBA           |
| `/basketball/{leagues}/` | https://site.api.espn.com/apis/site/v2/sports/basketball/nba-development/scoreboard?seasontype=2&type=0&level=3 | G-League       |
| `/basketball/{leagues}/` | -                                                                        | Summer League  |
| `/basketball/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/basketball/nbl/standings?seasontype=2&type=0&level=3 | National Basketball League |
| `/basketball/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/basketball/wnbl/standings?seasontype=2&type=0&level=3 | Women's National Basketball League |

### Boxing
| Sport Path              | URL Path | League |
|--------------------------|----------|--------|
| `/???/{leagues}/`        | -        | -      |

### College (Men's/Women's/Football/Basketball)
| Sport Path              | URL Path                                                                 | League                  |
|--------------------------|--------------------------------------------------------------------------|-------------------------|
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?seasontype=2&type=0&level=3 | Men's College Football  |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings?seasontype=2&type=0&level=3 | Men's College Football Top 25 |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/football/college-football/standings?seasontype=2&type=0&level=3 | Men's College Football Standings |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/baseball/college-baseball/standings?seasontype=2&type=0&level=3 | NCAA Men's Baseball     |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/baseball/college-softball/standings?seasontype=2&type=0&level=3 | NCAA Women's Softball   |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/site/v2/sports/baseball/college-softball/scoreboard?dates=20250517-20250617 | NCAA Women's Softball Playoffs |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?seasontype=2&type=0&level=3 | Men's College Basketball |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/rankings?seasontype=2&type=0&level=3 | Men's College Basketball Top 25 |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/basketball/mens-college-basketball/standings?seasontype=2&type=0&level=3 | Men's College Basketball Standings |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/scoreboard?seasontype=2&type=0&level=3 | Women's College Basketball |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/rankings?seasontype=2&type=0&level=3 | Women's College Basketball Top 25 |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/basketball/womens-college-basketball/standings?seasontype=2&type=0&level=3 | Women's College Basketball Standings |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/hockey/mens-college-hockey/scoreboard
