import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for fetching 2025 Club World Cup live data
API_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.cwc/scoreboard?dates=20250614-20250715"

# Updated group assignments based on 2025 FIFA Club World Cup draw
GROUP_TEAMS = {
    "A": ["Inter Miami CF", "Al Ahly", "Palmeiras", "FC Porto"],
    "B": ["Paris Saint-Germain", "Atlético Madrid", "Botafogo", "Seattle Sounders FC"],
    "C": ["Bayern Munich", "Auckland City", "Boca Juniors", "Benfica"],
    "D": ["Flamengo", "Chelsea", "Esperance Sportive de Tunis", "LAFC"],
    "E": ["River Plate", "Internazionale", "Urawa Red Diamonds", "Monterrey"],
    "F": ["Fluminense", "Borussia Dortmund", "Mamelodi Sundowns", "Ulsan HD"],
    "G": ["Manchester City", "Juventus", "Wydad AC", "Al Ain"],
    "H": ["Real Madrid", "RB Salzburg", "Pachuca", "Al Hilal"]
}

def fetch_and_filter_data(stage_or_group):
    try:
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())
        print("Full API response length:", len(data.get('events', [])))  # Debug: Total events
        if stage_or_group.startswith("group-"):
            group_letter = stage_or_group.split("-")[1].upper()
            group_teams = [t.lower() for t in GROUP_TEAMS[group_letter]]
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == "group-stage"
                and any(t.lower() in (event.get('name', '').lower() or ''.join(c['team']['displayName'].lower() for c in event.get('competitions', [{}])[0].get('competitors', []))) for t in group_teams)
            ]
            print(f"Filtered events for {stage_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
        else:
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == stage_or_group
            ]
            print(f"Filtered events for {stage_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {stage_or_group}: {e}")
        return {"events": []}

def extract_round_name(stage_or_group):
    round_map = {
        "group-A": "Group A", "group-B": "Group B", "group-C": "Group C", "group-D": "Group D",
        "group-E": "Group E", "group-F": "Group F", "group-G": "Group G", "group-H": "Group H",
        "round-of-16": "Round of 16", "quarterfinals": "Quarter-finals",
        "semifinals": "Semifinals", "final": "Final"
    }
    return round_map.get(stage_or_group, "Unknown Round")

def create_series_structure(data, stage_or_group):
    if not data['events']:
        return {}

    first_event = data['events'][0]
    slug = first_event.get('season', {}).get('slug', 'unknown')
    stage = extract_round_name(stage_or_group)

    # Extract all teams and matches, limited to the defined group
    group_letter = stage_or_group.split("-")[1].upper() if stage_or_group.startswith("group-") else None
    all_teams = set(GROUP_TEAMS.get(group_letter, [])) if group_letter else set()
    all_games = []
    print(f"Processing events for {stage_or_group}: {len(data['events'])} events")  # Debug
    for event in data['events']:
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']['displayName']
            team2 = competition['competitors'][1]['team']['displayName']
            if group_letter and (team1 not in GROUP_TEAMS[group_letter] or team2 not in GROUP_TEAMS[group_letter]):
                continue  # Skip games not involving group teams
            print(f"Matched game: {team1} vs {team2}")  # Debug
            all_teams.add(team1)
            all_teams.add(team2)

            status = competition.get('status', {}).get('type', {})
            game_status = status.get('state', 'scheduled')
            if status.get('completed', False):
                game_status = "full_time"
            elif status.get('state') == "in":
                game_status = "live"

            broadcast = ", ".join(b.get('names', ['TBD'])[0] for b in competition.get('broadcasts', []) if b.get('names'))
            venue = competition.get('venue', {}).get('fullName', 'TBD')
            date = competition.get('date', 'TBD')

            game = {
                "gameNumber": len(all_games) + 1,
                "Date": date,
                "Lowest Seed": {
                    "Name": min(team1, team2),  # Simple sorting for consistency
                    "Score": str(competition['competitors'][0].get('score', 0)),
                    "Logo": competition['competitors'][0]['team'].get('logo', ''),
                    "Advance": competition['competitors'][0].get('advance', False)
                },
                "Highest Seed": {
                    "Name": max(team1, team2),
                    "Score": str(competition['competitors'][1].get('score', 0)),
                    "Logo": competition['competitors'][1]['team'].get('logo', ''),
                    "Advance": competition['competitors'][1].get('advance', False)
                },
                "Broadcast": broadcast,
                "Status": game_status,
                "Venue": venue
            }
            all_games.append(game)

    # Calculate advancing teams
    advancing_teams = set()
    if stage.startswith("Group"):
        team_points = {team: 0 for team in all_teams}
        team_goals_for = {team: 0 for team in all_teams}
        team_goals_against = {team: 0 for team in all_teams}
        team_played = {team: 0 for team in all_teams}

        for game in all_games:
            if game["Status"] == "full_time":
                team1 = game["Lowest Seed"]["Name"]
                team2 = game["Highest Seed"]["Name"]
                team1_score = int(game["Lowest Seed"]["Score"])
                team2_score = int(game["Highest Seed"]["Score"])

                team_played[team1] += 1
                team_played[team2] += 1
                team_goals_for[team1] += team1_score
                team_goals_for[team2] += team2_score
                team_goals_against[team1] += team2_score
                team_goals_against[team2] += team1_score

                if team1_score > team2_score:
                    team_points[team1] += 3
                elif team2_score > team1_score:
                    team_points[team2] += 3
                else:
                    team_points[team1] += 1
                    team_points[team2] += 1

        # Sort teams by points, goal difference, then goals for
        sorted_teams = sorted(all_teams, key=lambda x: (
            team_points[x],
            team_goals_for[x] - team_goals_against[x],
            team_goals_for[x]
        ), reverse=True)
        advancing_teams = set(sorted_teams[:2])  # Top 2 teams advance
    elif stage in ["Round of 16", "Quarter-finals", "Semifinals", "Final"]:
        for game in all_games:
            if game["Status"] in ["full_time", "live"]:
                team1_score = int(game["Lowest Seed"]["Score"])
                team2_score = int(game["Highest Seed"]["Score"])
                team1 = game["Lowest Seed"]["Name"]
                team2 = game["Highest Seed"]["Name"]

                if team1_score > team2_score:
                    advancing_teams.add(team1)
                elif team2_score > team1_score:
                    advancing_teams.add(team2)
                elif game["Lowest Seed"]["Advance"]:
                    advancing_teams.add(team1)
                elif game["Highest Seed"]["Advance"]:
                    advancing_teams.add(team2)

    series_title = f"{stage} Matches"
    series_status = f"{stage} {('Standings' if stage.startswith('Group') else 'Matches')}"
    if stage == "Round of 16" and len(advancing_teams) > 16:
        advancing_teams = set(list(advancing_teams)[:16])  # Limit to 16 for Round of 16

    return {
        series_title: {
            "seriesTitle": series_title,
            "seriesStatus": series_status,
            "seriesDetails": {
                "stage": stage,
                "Teams": list(all_teams),
                "AdvancingTeams": list(advancing_teams),
                "seriesGames": all_games,
                "maxGames": 6 if stage.startswith("Group") else (len(all_games) if all_games else 0),  # 6 group games max
                "sport": "Soccer",
                "slug": stage_or_group
            }
        }
    }

def merge_original_and_series(data, series):
    return {
        "sport": "Soccer",
        "events": data.get("events", []),
        "series": list(series.values())
    }

def save_to_file(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

if __name__ == "__main__":
    print("Fetching 2025 FIFA Club World Cup live data...")
    club_world_cup_stages = [
        ("group-A", "fifa_club_worldcup_group_a_gpt.json"),
        ("group-B", "fifa_club_worldcup_group_b_gpt.json"),
        ("group-C", "fifa_club_worldcup_group_c_gpt.json"),
        ("group-D", "fifa_club_worldcup_group_d_gpt.json"),
        ("group-E", "fifa_club_worldcup_group_e_gpt.json"),
        ("group-F", "fifa_club_worldcup_group_f_gpt.json"),
        ("group-G", "fifa_club_worldcup_group_g_gpt.json"),
        ("group-H", "fifa_club_worldcup_group_h_gpt.json"),
        ("round-of-16", "fifa_club_worldcup_round_of_16_gpt.json"),
        ("quarterfinals", "fifa_club_worldcup_quarterfinals_gpt.json"),
        ("semifinals", "fifa_club_worldcup_semifinals_gpt.json"),
        ("final", "fifa_club_worldcup_final_gpt.json")
    ]

    for stage_or_group, filename in club_world_cup_stages:
        print(f"Processing {stage_or_group}...")
        round_data = fetch_and_filter_data(stage_or_group)
        round_series_structure = create_series_structure(round_data, stage_or_group)
        combined_data = merge_original_and_series(round_data, round_series_structure)
        save_to_file(filename, combined_data)
