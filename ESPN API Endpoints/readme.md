# ESPN API Endpoints

## Some Notes
- This document is for informational purposes only, with big thanks to ESPN for providing access to these APIs. The ability to view specific stats while watching ESPN is fantastic.
- You will find various APIs and endpoints listed below.

- Also you will notice that there are multiple ways to access data.  If you don't get data one way try a different path.  Some examples inlcude:
  - https://site.web.api.espn.com/apis/v2/sports 
  - https://site.api.espn.com/apis/site/v2/sports 
  - http://sports.core.api.espn.com/v2/sports 

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
| `/baseball/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/baseball/caribbean-series/scoreboard | caribbean-series            |

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
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/hockey/mens-college-hockey/scoreboard?seasontype=2&type=0&level=3 | NCAA Men's Ice Hockey   |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/hockey/womens-college-hockey/scoreboard?seasontype=2&type=0&level=3 | NCAA Women's Hockey     |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/lacrosse/mens-college-lacrosse/scoreboard?seasontype=2&type=0&level=3 | NCAA Men's Lacrosse     |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/lacrosse/womens-college-lacrosse/scoreboard?seasontype=2&type=0&level=3 | NCAA Women's Lacrosse   |
| `/???/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/field-hockey/womens-college-field-hockey/scoreboard?seasontype=2&type=0&level=3 | NCAA Women's Field Hockey |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/volleyball/mens-college-volleyball/standings?seasontype=1&type=0&level=3 | NCAA Men's Volleyball   |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/volleyball/womens-college-volleyball/standings?seasontype=1&type=0&level=3 | NCAA Women's Volleyball |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/water-polo/mens-college-water-polo/standings?seasontype=1&type=0&level=3 | NCAA Men's Water Polo   |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/water-polo/womens-college-water-polo/standings?seasontype=1&type=0&level=3 | NCAA Women's Water Polo |

### Cricket
| Sport Path              | URL Path                                                                 | League                 |
|--------------------------|--------------------------------------------------------------------------|------------------------|
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/1324623/scoreboard  | Big Bash League        |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/1474856/scoreboard  | International Masters League |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/8050/scoreboard     | Ranji Trophy           |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/1449668/scoreboard  | CSA Women Pro50 Series 2024/25 |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/20978/scoreboard    | SLC Major League Tournament |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/1474265/scoreboard  | Canada tour of Zimbabwe 2024/25 |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/20676/scoreboard    | CSA Provincial One-Day Challenge Division Two |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/8897/scoreboard     | Women's National Cricket League |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/19481/scoreboard    | Hong Kong Premier League T20 Tournament |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/20675/scoreboard    | CSA Provincial One-Day Challenge Division One |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/1474258/scoreboard  | Bahrain tour of Singapore 2024/25 |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/19934/scoreboard    | Hong Kong Women's Premier League 2020/21 |
| `/cricket/{leagues}/`    | https://site.api.espn.com/apis/site/v2/sports/cricket/8880/scoreboard     | -                      |

### Golf
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/pga/scoreboard     | PGA Scoreboard |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/lpga/rankings?region=us&lang=en | LPGA Rankings |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/lpga/scoreboard    | LPGA Scoreboard |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/liv/scoreboard     | LIV            |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/eur/scoreboard     | DP World Tour  |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/leaderboard?league=ntw | Korn Ferry     |
| `/golf/{leagues}/`       | https://site.web.api.espn.com/apis/site/v2/sports/golf/tgl/scoreboard     | Tomorrow's Golf League  |

### MMA
| Sport Path              | URL Path                                                                 | League |
|--------------------------|--------------------------------------------------------------------------|--------|
| `/mma/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard          | UFC    |
| `/mma/{leagues}/`        | https://site.api.espn.com/apis/site/v2/sports/mma/all/scoreboard          | -      |

### NFL
| Sport Path              | URL Path                                                                 | League |
|--------------------------|--------------------------------------------------------------------------|--------|
| `/football/{leagues}/`   | https://site.web.api.espn.com/apis/v2/sports/football/nfl/standings?seasontype=2&type=0&level=3 | NFL    |
| `/football/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/football/nfl/news           | NFL    |
| `/football/{leagues}/`   | https://site.web.api.espn.com/apis/v2/sports/football/ufl/standings?seasontype=2&type=0&level=3 | UFL    |
| `/football/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/football/ufl/news           | UFL    |
| `/football/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/football/ufl/transactions   | UFL    |

### NHL
| Sport Path              | URL Path                                                                 | League |
|--------------------------|--------------------------------------------------------------------------|--------|
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/hockey/nhl/standings?seasontype=2&type=0&level=3 | NHL    |
| `/???/{leagues}/`        | https://site.web.api.espn.com/apis/v2/sports/hockey/nhl/standings?region=us&lang=en&contentorigin=espn&type=3&level=2&sort=playoffseed%3Aasc%2Cpoints%3Adesc%2Cgamesplayed%3Aasc%2Crotwins%3Adesc&seasontype=2 | NHL    |

### Racing
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/irl/standings?seasontype=1&type=0&level=3 | IRL            |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/nationwide/standings?seasontype=1&type=0&level=3 | -              |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/sprint/standings?seasontype=1&type=0&level=3 | -              |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/nascar-truck/standings?seasontype=1&type=0&level=3 | Nascar-Truck   |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/f1/standings?seasontype=1&type=0&level=3 | F1             |
| `/racing/{leagues}/`     | -                                                                        | Xfinity        |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/nhra/standings?seasontype=1&type=0&level=3 | -              |
| `/racing/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/racing/nascar-premier/standings?seasontype=1&type=0&level=3 | Nascar         |

### Rugby
| Sport Path              | URL Path                                                                 | League             |
|--------------------------|--------------------------------------------------------------------------|--------------------|
| `/rugby/{leagues}/`      | https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=rugby       | Rugby              |
| `/rugby/{leagues}/`      | https://site.api.espn.com/apis/site/v2/sports/rugby/289262/scoreboard     | Major League Rugby |
| `/rugby/{leagues}/`      | https://site.api.espn.com/apis/site/v2/sports/rugby/270559/scoreboard     | French Top 14      |
| `/rugby/{leagues}/`      | https://site.api.espn.com/apis/site/v2/sports/rugby/270557/scoreboard     | United Rugby Championship |
| `/rugby/{leagues}/`      | https://site.api.espn.com/apis/site/v2/sports/rugby/242041/scoreboard     | Super Rugby Pacific |

### Soccer
| Sport Path              | URL Path                                                                 | League                     |
|--------------------------|--------------------------------------------------------------------------|----------------------------|
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/afc.champions/standings?seasontype=1&type=0&level=3 | AFC Champions League Elite |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/afc.cup/standings?seasontype=1&type=0&level=3 | AFC Champions League Two   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/afc.cupq/standings?seasontype=1&type=0&level=3 | AFC Asian Cup Qualifiers   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/aff.championship/standings?seasontype=1&type=0&level=3 | ASEAN Championship         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.1/standings?seasontype=1&type=0&level=3 | Argentine Liga Profesional de Fútbol |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.2/standings?seasontype=1&type=0&level=3 | Argentine Nacional B       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.3/standings?seasontype=1&type=0&level=3 | Argentine Primera B        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.4/standings?seasontype=1&type=0&level=3 | Argentine Primera C        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.5/standings?seasontype=1&type=0&level=3 | Argentine Primera D        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.copa/standings?seasontype=1&type=0&level=3 | -                         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/arg.urba/standings?seasontype=1&type=0&level=3 | -                         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/aus.1/standings?seasontype=1&type=0&level=3 | Australian A-League Men   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/aut.1/standings?seasontype=1&type=0&level=3 | Austrian Bundesliga       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/bel.1/standings?seasontype=1&type=0&level=3 | Belgian Pro League        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/bol.1/standings?seasontype=1&type=0&level=3 | Bolivian Liga Profesional |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/bra.1/standings?seasontype=1&type=0&level=3 | Brazilian Serie A         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/bra.2/standings?seasontype=1&type=0&level=3 | Brazilian Serie B         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/bra.3/standings?seasontype=1&type=0&level=3 | Brazilian Serie C         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/caf.nations/standings?seasontype=1&type=0&level=3 | Africa Cup of Nations     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/chi.1/standings?seasontype=1&type=0&level=3 | Chilean Primera División  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/chi.2/standings?seasontype=1&type=0&level=3 | Segunda División de Chile |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/col.1/standings?seasontype=1&type=0&level=3 | Colombian Primera A       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/col.2/standings?seasontype=1&type=0&level=3 | Colombian Primera B       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/concaaf.champions_cup/standings?seasontype=1&type=0&level=3 | -                         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.champions/standings?seasontype=1&type=0&level=3 | Concacaf Champions Cup   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.golf/standings?seasontype=1&type=0&level=3 | -                         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.superliga/standings?seasontype=1&type=0&level=3 | North American SuperLiga |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/concacaf.u23/standings?seasontype=1&type=0&level=3 | CONCACAF U23 Tournament  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.america/standings?seasontype=1&type=0&level=3 | Copa América            |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.libertadores/standings?seasontype=1&type=0&level=3 | CONMEBOL Libertadores   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.sudamericana/standings?seasontype=1&type=0&level=3 | CONMEBOL Sudamericana   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/conmebol.sudamericano_sub20/standings?seasontype=1&type=0&level=3 | CONMEBOL Sudamericano Sub-20 |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/crc.1/standings?seasontype=1&type=0&level=3 | Costa Rican Primera Division |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/den.1/standings?seasontype=1&type=0&level=3 | Danish Superliga        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ecu.1/standings?seasontype=1&type=0&level=3 | LigaPro Ecuador         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ecu.2/standings?seasontype=1&type=0&level=3 | Ecuador Serie B         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/eng.charity/standings?seasontype=1&type=0&level=3 | English FA Community Shield |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/eng.fa/standings?seasontype=1&type=0&level=3 | English FA Cup          |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/eng.trophy/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/eng.w.1/standings?seasontype=1&type=0&level=3 | English Women's Super League |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/eng.worthington/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/esp.2/standings?seasontype=1&type=0&level=3 | Spanish LALIGA 2        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/esp.copa_del_rey/standings?seasontype=1&type=0&level=3 | Spanish Copa del Rey    |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/esp.super_cup/standings?seasontype=1&type=0&level=3 | Spanish Supercopa       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.ofc/standings?seasontype=1&type=0&level=3 | FIFA World Cup Qualifying - OFC |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.confederations/standings?seasontype=1&type=0&level=3 | FIFA Confederations Cup |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.cwc/standings?seasontype=1&type=0&level=3 | FIFA Club World Cup     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.friendly/standings?seasontype=1&type=0&level=3 | Men's International Friendly |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.friendly.w/standings?seasontype=1&type=0&level=3 | Women's International Friendly |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.olympics/standings?seasontype=1&type=0&level=3 | Men's Olympic Soccer Tournament |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.olympicsq/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.algarve/standings?seasontype=1&type=0&level=3 | Algarve Cup            |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.olympics/standings?seasontype=1&type=0&level=3 | Women's Olympic Soccer Tournament |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.w.olympicsq/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world/standings?seasontype=1&type=0&level=3 | FIFA World Cup          |
| `/soccer/{leagues}/`     | https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20221203-20221218 | FIFA World Cup Matches (2022) |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world.u17/standings?seasontype=1&type=0&level=3 | FIFA Under-17 World Cup |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world.u20/standings?seasontype=1&type=0&level=3 | FIFA Under-20 World Cup |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq/standings?seasontype=1&type=0&level=3 | World Cup Qualifying    |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.afc/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.caf/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.concacaf/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.conmebol/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.worldq.uefa/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.wwc/standings?seasontype=1&type=0&level=3 | FIFA Women's World Cup  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.wyc/standings?seasontype=1&type=0&level=3 | -                       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fra.1/standings?seasontype=1&type=0&level=3 | French Ligue 1          |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fra.2/standings?seasontype=1&type=0&level=3 | French Ligue 2          |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fra.coupe_de_france/standings?seasontype=1&type=0&level=3 | Coupe de France         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/fra.coupe_de_la_ligue/standings?seasontype=1&type=0&level=3 | French Coupe de la Ligue |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ger.dfb_pokal/standings?seasontype=1&type=0&level=3 | German Cup              |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ger.super_cup/standings?seasontype=1&type=0&level=3 | German DFL-Supercup     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/global.world_football_challenge/standings?seasontype=1&type=0&level=3 | WORLD FOOTBALL CHALLENGE |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/gre.1/standings?seasontype=1&type=0&level=3 | Greek Super League      |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/gua.1/standings?seasontype=1&type=0&level=3 | Guatemalan Liga Nacional |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/hon.1/standings?seasontype=1&type=0&level=3 | Honduran Liga Nacional  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/intercontinental/standings?seasontype=1&type=0&level=3 | Intercontinental Cup    |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/irl.1/standings?seasontype=1&type=0&level=3 | Irish Premier Division  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ita.2/standings?seasontype=1&type=0&level=3 | Italian Serie B         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ita.coppa_italia/standings?seasontype=1&type=0&level=3 | Coppa Italia            |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ita.super_cup/standings?seasontype=1&type=0&level=3 | Italian Supercoppa      |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/jpn.1/standings?seasontype=1&type=0&level=3 | Japanese J.League       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/mex.2/standings?seasontype=1&type=0&level=3 | Mexican Liga de Expansión MX |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/mex.interliga/standings?seasontype=1&type=0&level=3 | Torneo Interliga de México |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ned.1/standings?seasontype=1&type=0&level=3 | Dutch Eredivisie        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ned.2/standings?seasontype=1&type=0&level=3 | Dutch Keuken Kampioen Divisie |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ned.cup/standings?seasontype=1&type=0&level=3 | Dutch KNVB Beker        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/nir.1/standings?seasontype=1&type=0&level=3 | Northern Irish Premiership |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/nor.1/standings?seasontype=1&type=0&level=3 | Norwegian Eliteserien   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/panam.m/standings?seasontype=1&type=0&level=3 | Pan Am Men's Soccer     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/panam.w/standings?seasontype=1&type=0&level=3 | Pan Am Women's Soccer   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/par.1/standings?seasontype=1&type=0&level=3 | Paraguayan Primera División |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/par.2/standings?seasontype=1&type=0&level=3 | Segunda División de Paraguay |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/per.1/standings?seasontype=1&type=0&level=3 | Peruvian Liga 1         |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/per.2/standings?seasontype=1&type=0&level=3 | Segunda División de Perú |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/por.1/standings?seasontype=1&type=0&level=3 | Portuguese Primeira Liga |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/rsa.1/standings?seasontype=1&type=0&level=3 | South African Premier Division |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/rsa.2/standings?seasontype=1&type=0&level=3 | South African First Division |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/rus.1/standings?seasontype=1&type=0&level=3 | Russian Premier League  |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.1/standings?seasontype=1&type=0&level=3 | Scottish Premiership    |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.2/standings?seasontype=1&type=0&level=3 | Scottish Championship   |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.3/standings?seasontype=1&type=0&level=3 | Scottish SPFL League One |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.4/standings?seasontype=1&type=0&level=3 | Scottish SPFL League Two |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.challenge/standings?seasontype=1&type=0&level=3 | Scottish League Challenge Cup |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.cis/standings?seasontype=1&type=0&level=3 | Scottish League Cup     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sco.tennents/standings?seasontype=1&type=0&level=3 | Scottish Cup            |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/slv.1/standings?seasontype=1&type=0&level=3 | Salvadoran Primera Division |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/sui.1/standings?seasontype=1&type=0&level=3 | Swiss Super League      |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/swe.1/standings?seasontype=1&type=0&level=3 | Swedish Allsvenskan     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/tur.1/standings?seasontype=1&type=0&level=3 | Turkish Super Lig       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.carling/standings?seasontype=1&type=0&level=3 | Carling Nations Cup     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euro/standings?seasontype=1&type=0&level=3 | UEFA European Championship |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euro.u19/standings?seasontype=1&type=0&level=3 | UEFA European Under-19 Championship |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.europa/standings?seasontype=1&type=0&level=3 | UEFA Europa League      |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.euroq/standings?seasontype=1&type=0&level=3 | UEFA European Championship Qualifying |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.intertoto/standings?seasontype=1&type=0&level=3 | UEFA Intertoto Cup      |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.super_cup/standings?seasontype=1&type=0&level=3 | UEFA Super Cup          |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.uefa/standings?seasontype=1&type=0&level=3 | UEFA Cup                |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.worldq/standings?seasontype=1&type=0&level=3 | UEFA World Cup Qualifying |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uefa.wchampions/standings?seasontype=2&type=0&level=3 | UEFA Women's Champions League |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uru.1/standings?seasontype=1&type=0&level=3 | Liga UAF Uruguaya       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/uru.2/standings?seasontype=1&type=0&level=3 | Segunda División de Uruguay |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.misl/standings?seasontype=1&type=0&level=3 | Major Indoor Soccer League |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.ncaa.m.1/standings?seasontype=1&type=0&level=3 | NCAA Men's Soccer       |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.ncaa.w.1/standings?seasontype=1&type=0&level=3 | NCAA Women's Soccer     |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.open/standings?seasontype=1&type=0&level=3 | U.S. Open Cup           |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.usl.1/standings?seasontype=1&type=0&level=3 | USL Championship        |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.usl.l1/standings?seasontype=2&type=0&level=3 | USL League One          |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.w.1/standings?seasontype=1&type=0&level=3 | USA Women's United Soccer Association |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/usa.world_series/standings?seasontype=1&type=0&level=3 | World Series of Football |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ven.1/standings?seasontype=1&type=0&level=3 | Venezuelan Primera División |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/ven.2/standings?seasontype=1&type=0&level=3 | Segunda División de Venezuela |
| `/soccer/{leagues}/`     | https://site.web.api.espn.com/apis/v2/sports/soccer/wal.1/standings?seasontype=1&type=0&level=3 | Welsh Premier League    |
| `/soccer/{leagues}/`     | https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/660/schedule | USA Men's Soccer Team Schedule |

### Tennis
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/tennis/{leagues}/`     | https://site.web.api.espn.com/apis/site/v2/sports/tennis/atp/rankings?region=us&lang=en | Men's Tennis  |
| `/tennis/{leagues}/`     | https://site.web.api.espn.com/apis/site/v2/sports/tennis/wta/rankings?region=us&lang=en | Women's Tennis |

### Wrestling
| Sport Path                      | URL Path                                                                 | League     |
|---------------------------------|--------------------------------------------------------------------------|------------|
| `/professional-wrestling/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/professional-wrestling/aew/standings?seasontype=2&type=0&level=3 | AEW        |
| `/professional-wrestling/{leagues}/` | https://site.web.api.espn.com/apis/v2/sports/professional-wrestling/wwe/standings?seasontype=2&type=0&level=3 | WWE        |

### Lacrosse
| Sport Path              | URL Path                                                                 | League             |
|--------------------------|--------------------------------------------------------------------------|--------------------|
| `/lacrosse/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/lacrosse/pll/scoreboard     | Premier Lacrosse League |
| `/lacrosse/{leagues}/`   | https://site.web.api.espn.com/apis/v2/sports/lacrosse/pll/standings?seasontype=2&type=0&level=3 | Premier Lacrosse League |
| `/lacrosse/{leagues}/`   | https://site.api.espn.com/apis/site/v2/sports/lacrosse/nll/scoreboard     | National Lacrosse League |
| `/lacrosse/{leagues}/`   | https://site.web.api.espn.com/apis/v2/sports/lacrosse/nll/standings?seasontype=2&type=0&level=3 | National Lacrosse League |

### Water Polo
| Sport Path              | URL Path                                                                 | League         |
|--------------------------|--------------------------------------------------------------------------|----------------|
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/mens-college-water-polo/seasons?lang=en&region=us | NCAA Men's     |
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/mens-college-water-polo/events?lang=en&region=us | NCAA Men's     |
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/mens-college-water-polo/rankings?lang=en&region=us | NCAA Men's     |
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/womens-college-water-polo/seasons?lang=en&region=us | NCAA Women's   |
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/womens-college-water-polo/events?lang=en&region=us | NCAA Women's   |
| `/water-polo/{leagues}/` | http://sports.core.api.espn.com/v2/sports/water-polo/leagues/womens-college-water-polo/rankings?lang=en&region=us | NCAA Women's   |
