import urllib.request
import json
from datetime import datetime, timezone

# Define date ranges for playoff rounds
DATE_RANGES = [
    ("20240531-20240603", "Regionals"),  # Regionals: May 31 to June 3, 2024
    ("20240607-20240610", "Super Regionals"),  # Super Regionals: June 7 to June 10, 2024
    ("20240614-20240624", "College World Series")  # CWS and Finals: June 14 to June 24, 2024
]

# Base API URL template
API_URL_TEMPLATE = "https://site.api.espn.com/apis/site/v2/sports/baseball/college-baseball/scoreboard?dates={}"

def fetch_all_events(date_range, label):
    try:
        api_url = API_URL_TEMPLATE.format(date_range)
        response = urllib.request.urlopen(api_url)
        data = json.loads(response.read())
        events = data.get('events', [])
        print(f"Fetched {len(events)} events for {label} (dates={date_range})")
        for event in events:
            for competition in event.get('competitions', []):
                notes = competition.get('notes', [{}])[0].get('headline', '')
                date = competition.get('date', 'Unknown Date')
                teams = [comp['team']['displayName'] for comp in competition.get('competitors', [])]
                print(f"Event Date: {date}, Teams: {teams}, Notes.headline: {notes}")
        return events
    except Exception as e:
        print(f"Error fetching data for {label} (dates={date_range}): {e}")
        return []

def fetch_all_playoff_data():
    all_events = []
    for date_range, label in DATE_RANGES:
        print(f"Fetching data for {label} (dates={date_range})...")
        events = fetch_all_events(date_range, label)
        for event in events:
            event['round_label'] = label
        all_events.extend(events)
    unique_events = {event['id']: event for event in all_events}.values()
    print(f"Total unique events fetched: {len(unique_events)}")
    return {"events": list(unique_events)}

def extract_round_name(notes_headline, round_label):
    if not notes_headline:
        print(f"No notes.headline, using round_label: {round_label}")
        return round_label if round_label in ["Regionals", "Super Regionals", "College World Series"] else "Unknown Round"
    parts = notes_headline.split(" - ")
    for part in parts:
        if "Regional" in part and "Super Regional" not in part:
            return "Regionals"
        elif "Super Regional" in part or "Super Regional Game" in notes_headline:
            return "Super Regionals"
        elif "College World Series" in part and "Championship" in part:
            return "CWS Finals"
        elif "College World Series" in part:
            return "College World Series"
    print(f"Notes.headline '{notes_headline}' didn't match, using round_label: {round_label}")
    if round_label == "Regionals":
        return "Regionals"
    elif round_label == "Super Regionals":
        return "Super Regionals"
    elif round_label == "College World Series":
        if "Championship" in notes_headline:
            return "CWS Finals"
        return "College World Series"
    return "Unknown Round"

def extract_region_name(notes_headline):
    if not notes_headline:
        return "Unknown Region"
    parts = notes_headline.split(" - ")
    for part in parts:
        if "Regional" in part:
            region = part.replace(" Super Regional", "").replace(" Regional", "")
            return region
        elif "College World Series" in part:
            return "Omaha"
    return "Unknown Region"

def infer_double_elimination_structure(region_games):
    # Sort games by date to determine the order of play
    sorted_games = sorted(region_games, key=lambda x: x["seriesDetails"]["seriesGames"][0]["Date"])
    
    # Assume standard double-elimination format: 4 teams, 6-7 games
    # Game 1: 1 vs 4, Game 2: 2 vs 3
    # Game 3: Loser Game 1 vs Loser Game 2 (Elimination)
    # Game 4: Winner Game 1 vs Winner Game 2
    # Game 5: Loser Game 4 vs Winner Game 3 (Elimination)
    # Game 6: Winner Game 4 vs Winner Game 5 (Regional Final)
    # Game 7: If necessary, same teams as Game 6

    teams = set()
    for game in sorted_games:
        teams.add(game["seriesDetails"]["Teams"][0])
        teams.add(game["seriesDetails"]["Teams"][1])
    teams = list(teams)
    
    # Assume seeds based on team names (simplified; in reality, we'd need seed data)
    seeds = {team: idx + 1 for idx, team in enumerate(teams)}
    
    # Track winners and losers
    game_metadata = []
    winners = {}
    losers = {}
    
    # Game 1: 1 vs 4
    game1 = sorted_games[0]
    game1_teams = game1["seriesDetails"]["Teams"]
    game1_scores = [
        int(game1["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game1["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game1_winner = game1_teams[0] if game1_scores[0] > game1_scores[1] else game1_teams[1]
    game1_loser = game1_teams[0] if game1_winner == game1_teams[1] else game1_teams[1]
    winners[1] = game1_winner
    losers[1] = game1_loser
    game1["bracketPosition"] = "Game 1"
    
    # Game 2: 2 vs 3
    game2 = sorted_games[1]
    game2_teams = game2["seriesDetails"]["Teams"]
    game2_scores = [
        int(game2["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game2["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game2_winner = game2_teams[0] if game2_scores[0] > game2_scores[1] else game2_teams[1]
    game2_loser = game2_teams[0] if game2_winner == game2_teams[1] else game2_teams[1]
    winners[2] = game2_winner
    losers[2] = game2_loser
    game2["bracketPosition"] = "Game 2"
    
    # Game 3: Loser Game 1 vs Loser Game 2
    game3 = sorted_games[2]
    game3_teams = game3["seriesDetails"]["Teams"]
    if set(game3_teams) != {losers[1], losers[2]}:
        print(f"Game 3 teams {game3_teams} do not match expected losers {losers[1]} and {losers[2]}")
    game3_scores = [
        int(game3["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game3["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game3_winner = game3_teams[0] if game3_scores[0] > game3_scores[1] else game3_teams[1]
    winners[3] = game3_winner
    game3["bracketPosition"] = "Game 3 (Loser’s Bracket)"
    
    # Game 4: Winner Game 1 vs Winner Game 2
    game4 = sorted_games[3]
    game4_teams = game4["seriesDetails"]["Teams"]
    if set(game4_teams) != {winners[1], winners[2]}:
        print(f"Game 4 teams {game4_teams} do not match expected winners {winners[1]} and {winners[2]}")
    game4_scores = [
        int(game4["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game4["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game4_winner = game4_teams[0] if game4_scores[0] > game4_scores[1] else game4_teams[1]
    game4_loser = game4_teams[0] if game4_winner == game4_teams[1] else game4_teams[1]
    winners[4] = game4_winner
    losers[4] = game4_loser
    game4["bracketPosition"] = "Game 4"
    
    # Game 5: Loser Game 4 vs Winner Game 3
    game5 = sorted_games[4]
    game5_teams = game5["seriesDetails"]["Teams"]
    if set(game5_teams) != {losers[4], winners[3]}:
        print(f"Game 5 teams {game5_teams} do not match expected teams {losers[4]} and {winners[3]}")
    game5_scores = [
        int(game5["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game5["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game5_winner = game5_teams[0] if game5_scores[0] > game5_scores[1] else game5_teams[1]
    winners[5] = game5_winner
    game5["bracketPosition"] = "Game 5 (Loser’s Bracket)"
    
    # Game 6: Winner Game 4 vs Winner Game 5 (Regional Final)
    game6 = sorted_games[5]
    game6_teams = game6["seriesDetails"]["Teams"]
    if set(game6_teams) != {winners[4], winners[5]}:
        print(f"Game 6 teams {game6_teams} do not match expected teams {winners[4]} and {winners[5]}")
    game6_scores = [
        int(game6["seriesDetails"]["seriesGames"][0]["Lowest Seed"]["Score"]),
        int(game6["seriesDetails"]["seriesGames"][0]["Highest Seed"]["Score"])
    ]
    game6_winner = game6_teams[0] if game6_scores[0] > game6_scores[1] else game6_teams[1]
    game6_loser = game6_teams[0] if game6_winner == game6_teams[1] else game6_teams[1]
    winners[6] = game6_winner
    game6["bracketPosition"] = "Game 6 (Regional Final)"
    
    # Game 7: If necessary
    if len(sorted_games) > 6:
        game7 = sorted_games[6]
        game7_teams = game7["seriesDetails"]["Teams"]
        if set(game7_teams) != {winners[6], game6_loser}:
            print(f"Game 7 teams {game7_teams} do not match expected teams {winners[6]} and {game6_loser}")
        game7["bracketPosition"] = "Game 7 (Regional Final)"
    
    return sorted_games, winners.get(6, winners.get(5))

def create_combined_bracket_structure(data):
    series_dict = {}
    team_abbr_to_name = {}
    bracket_structure = {}
    super_regional_pairings = {}

    for event in data.get('events', []):
        round_label = event.get('round_label', 'Unknown')
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']
            team2 = competition['competitors'][1]['team']

            team_abbr_to_name[team1['abbreviation']] = team1['displayName']
            team_abbr_to_name[team2['abbreviation']] = team2['displayName']

            seed1 = competition['competitors'][0].get('seed', float('inf'))
            seed2 = competition['competitors'][1].get('seed', float('inf'))
            if seed1 < seed2:
                lowest_seed, highest_seed = team1, team2
            else:
                lowest_seed, highest_seed = team2, team1

            base_series_title = " vs ".join(sorted([lowest_seed['displayName'], highest_seed['displayName']]))
            notes_headline = competition.get('notes', [{}])[0].get('headline', '')
            round_name = extract_round_name(notes_headline, round_label)
            region_name = extract_region_name(notes_headline)
            series_title = f"{base_series_title} ({round_name})"

            print(f"Series: {series_title}, Round: {round_name}, Region: {region_name}")

            if series_title not in series_dict:
                series_dict[series_title] = {
                    "seriesTitle": series_title,
                    "seriesStatus": "0-0",
                    "seriesDetails": {
                        "Teams": [lowest_seed['displayName'], highest_seed['displayName']],
                        "seriesGames": [],
                        "maxGames": 3 if "Super Regionals" in round_name or "CWS Finals" in round_name else None
                    },
                    "round": round_name,
                    "region": region_name
                }

            if "Super Regionals" in round_name or "CWS Finals" in round_name:
                max_games = competition.get('series', {}).get('totalCompetitions', 3)
                series_dict[series_title]["seriesDetails"]["maxGames"] = max_games

            status_info = competition.get('status', {})
            game_status = "scheduled"
            game_segment = None
            time_remaining = None
            if status_info.get('type', {}).get('completed', False):
                game_status = "final"
            elif status_info.get('type', {}).get('state') == "in":
                game_status = "live"
                inning_num = status_info.get('period', 0)
                if inning_num <= 9:
                    game_segment = f"Inning {inning_num}"
                else:
                    game_segment = "Extra Innings"
                time_remaining = status_info.get('displayClock', '0:00')

            odds_data = competition.get('odds', [])
            odds_details = {}
            if game_status == "scheduled" and odds_data:
                odds = odds_data[0]
                odds_details = {
                    "PointSpread": odds.get('details', 'N/A'),
                    "MoneylineHome": odds.get('homeTeamOdds', {}).get('moneyLine', 'N/A'),
                    "MoneylineAway": odds.get('awayTeamOdds', {}).get('moneyLine', 'N/A'),
                    "OverUnder": odds.get('overUnder', 'N/A')
                }
            else:
                odds_details = {
                    "PointSpread": "N/A",
                    "MoneylineHome": "N/A",
                    "MoneylineAway": "N/A",
                    "OverUnder": "N/A"
                }

            game_details = {
                "sport": "NCAA Baseball",
                "gameNumber": len(series_dict[series_title]["seriesDetails"]["seriesGames"]) + 1,
                "Date": competition.get('date', 'TBD'),
                "Lowest Seed": {
                    "Name": lowest_seed['displayName'],
                    "Score": competition['competitors'][0].get('score', '0') if seed1 < seed2 else competition['competitors'][1].get('score', '0'),
                    "Logo": lowest_seed.get('logo', '')
                },
                "Highest Seed": {
                    "Name": highest_seed['displayName'],
                    "Score": competition['competitors'][1].get('score', '0') if seed1 < seed2 else competition['competitors'][0].get('score', '0'),
                    "Logo": highest_seed.get('logo', '')
                },
                "Broadcast": ", ".join(
                    broadcast.get('names', ['TBD'])[0]
                    for broadcast in competition.get('broadcasts', [])
                ),
                "Status": game_status,
                "GameSegment": game_segment,
                "TimeRemaining": time_remaining,
                "Odds": odds_details
            }
            series_dict[series_title]["seriesDetails"]["seriesGames"].append(game_details)

            series_dict[series_title]["latest_series_info"] = competition.get('series', {})

            # Build bracket structure for all rounds
            if region_name not in bracket_structure:
                bracket_structure[region_name] = {
                    "Regionals": [],
                    "Super Regionals": [],
                    "College World Series": [],
                    "CWS Finals": [],
                    "RegionalVenue": notes_headline.split(" - ")[-1] if " - " in notes_headline else "Unknown Venue"
                }
            bracket_structure[region_name][round_name].append(series_dict[series_title])

    # Update seriesStatus for each series
    for series_title, series in series_dict.items():
        series_info = series.get("latest_series_info", {})
        team1 = series["seriesDetails"]["Teams"][0]
        team2 = series["seriesDetails"]["Teams"][1]

        series_completed = series_info.get('completed', False)
        series_summary = series_info.get('summary', '')

        if series_completed and series_summary:
            if "wins" in series_summary.lower():
                winner_abbr = series_summary.split()[0]
                winner = team_abbr_to_name.get(winner_abbr, winner_abbr)
                wins = series_summary.split()[-1]
                series["seriesStatus"] = f"{winner} wins series {wins}"
            else:
                team1_wins = 0
                team2_wins = 0
                for game in series["seriesDetails"]["seriesGames"]:
                    try:
                        team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                        team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                    except ValueError:
                        team1_score = 0
                        team2_score = 0

                    if team1_score > team2_score and team1_score != 0:
                        team1_wins += 1
                    elif team2_score > team1_score and team2_score != 0:
                        team2_wins += 1

                if team1_wins > team2_wins:
                    series["seriesStatus"] = f"{team1} wins series {team1_wins}-{team2_wins}"
                elif team2_wins > team1_wins:
                    series["seriesStatus"] = f"{team2} wins series {team2_wins}-{team1_wins}"
                else:
                    series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"
        elif series_summary:
            if "leads" in series_summary.lower():
                leader_abbr = series_summary.split()[0]
                leader = team_abbr_to_name.get(leader_abbr, leader_abbr)
                wins = series_summary.split()[-1]
                series["seriesStatus"] = f"{leader} leads series {wins}"
            else:
                team1_wins = 0
                team2_wins = 0
                for game in series["seriesDetails"]["seriesGames"]:
                    try:
                        team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                        team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                    except ValueError:
                        team1_score = 0
                        team2_score = 0

                    if team1_score > team2_score and team1_score != 0:
                        team1_wins += 1
                    elif team2_score > team2_score and team2_score != 0:
                        team2_wins += 1

                if team1_wins > team2_wins:
                    series["seriesStatus"] = f"{team1} leads series {team1_wins}-{team2_wins}"
                elif team2_wins > team1_wins:
                    series["seriesStatus"] = f"{team2} leads series {team2_wins}-{team1_wins}"
                else:
                    series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"
        else:
            team1_wins = 0
            team2_wins = 0
            for game in series["seriesDetails"]["seriesGames"]:
                try:
                    team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                    team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                except ValueError:
                    team1_score = 0
                    team2_score = 0

                if team1_score > team2_score and team1_score != 0:
                    team1_wins += 1
                elif team2_score > team1_score and team2_score != 0:
                    team2_wins += 1

            if team1_wins > team2_wins:
                series["seriesStatus"] = f"{team1} leads series {team1_wins}-{team2_wins}"
            elif team2_wins > team1_wins:
                series["seriesStatus"] = f"{team2} leads series {team2_wins}-{team1_wins}"
            else:
                series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"

        del series["latest_series_info"]

    # Process Regionals to infer double-elimination structure
    for region, rounds in bracket_structure.items():
        if rounds["Regionals"]:
            rounds["Regionals"], regional_winner = infer_double_elimination_structure(rounds["Regionals"])
            rounds["RegionalWinner"] = regional_winner

    # Pair Super Regionals with their corresponding Regionals
    super_regional_regions = [region for region, rounds in bracket_structure.items() if rounds["Super Regionals"]]
    for sr_region in super_regional_regions:
        super_regional = bracket_structure[sr_region]["Super Regionals"][0]
        teams = super_regional["seriesDetails"]["Teams"]
        # Find the two Regionals that these teams came from
        feeding_regions = []
        for team in teams:
            for region, rounds in bracket_structure.items():
                if rounds["RegionalWinner"] == team and region != sr_region:
                    feeding_regions.append(region)
                    break
            else:
                feeding_regions.append(sr_region)  # Fallback: assume the Super Regional region is one of the feeding regions
        super_regional_pairings[sr_region] = feeding_regions

    print("Bracket structure:", json.dumps(bracket_structure, indent=2))
    print("Super Regional pairings:", json.dumps(super_regional_pairings, indent=2))
    return series_dict, bracket_structure, super_regional_pairings

def save_to_file(filename, data):
    try:
        data["filename"] = filename.split("/")[-1]
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

if __name__ == "__main__":
    print("Fetching NCAA college baseball playoff data...")
    all_data = fetch_all_playoff_data()
    series_dict, bracket_structure, super_regional_pairings = create_combined_bracket_structure(all_data)

    # Save combined data
    combined_data = {
        "sport": "NCAA Baseball",
        "events": all_data.get("events", []),
        "series": list(series_dict.values()),
        "bracket": bracket_structure,
        "superRegionalPairings": super_regional_pairings,
        "filename": "ncaa_combined_bracket_gpt.json"
    }
    save_to_file("/config/www/ncaa_combined_bracket_gpt.json", combined_data)
