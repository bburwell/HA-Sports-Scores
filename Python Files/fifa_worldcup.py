import urllib.request
import json
from datetime import datetime, timezone

# API URL for 2026 FIFA World Cup
API_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260611-20260719"

# 2026 FIFA World Cup groups (post-draw, with placeholders for unresolved playoff winners)
GROUP_TEAMS = {
    "A": ["Mexico", "South Africa", "Korea Republic", "UEFA Path D winner"],  # e.g. Denmark/Czechia/Ireland/N. Macedonia winner
    "B": ["Canada", "UEFA Path A winner", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "UEFA Path C winner"],
    "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "UEFA Path B winner", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Inter-confed Path 2 winner", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Inter-confed Path 1 winner", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}

def fetch_and_filter_data(stage_or_group):
    try:
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())
        print("Full API response events count:", len(data.get('events', [])))

        events = data.get('events', [])

        if stage_or_group.startswith("group-"):
            group_letter = stage_or_group.split("-")[1].upper()
            if group_letter not in GROUP_TEAMS:
                return {"events": []}
            group_teams_lower = [t.lower() for t in GROUP_TEAMS[group_letter]]

            filtered = []
            for event in events:
                comps = event.get('competitions', [{}])
                if not comps:
                    continue
                comp = comps[0]
                season_slug = event.get('season', {}).get('slug', '')
                if season_slug != "group-stage":
                    continue

                names = []
                for c in comp.get('competitors', []):
                    team = c.get('team', {})
                    names.append(team.get('displayName', '').lower())
                    names.append(team.get('shortDisplayName', '').lower())

                if any(team in ' '.join(names) for team in group_teams_lower):
                    filtered.append(event)

            print(f"Filtered events for {stage_or_group}: {len(filtered)}")
            return {"events": filtered}

        else:
            # Knockout stages – filter by season slug
            slug_map = {
                "round-of-32": "round-of-32",
                "round-of-16": "round-of-16",
                "quarterfinals": "quarterfinals",
                "semifinals": "semifinals",
                "third-place": "third-place",   # may vary; check real slug
                "final": "final"
            }
            target_slug = slug_map.get(stage_or_group, stage_or_group)

            filtered = [
                event for event in events
                if event.get('season', {}).get('slug') == target_slug
            ]
            print(f"Filtered events for {stage_or_group}: {len(filtered)}")
            return {"events": filtered}

    except Exception as e:
        print(f"Error fetching data for {stage_or_group}: {e}")
        return {"events": []}

def extract_round_name(stage_or_group):
    round_map = {
        **{f"group-{chr(65+i)}": f"Group {chr(65+i)}" for i in range(12)},  # A-L
        "round-of-32": "Round of 32",
        "round-of-16": "Round of 16",
        "quarterfinals": "Quarter-finals",
        "semifinals": "Semifinals",
        "third-place": "Third-place match",
        "final": "Final"
    }
    return round_map.get(stage_or_group, "Unknown Round")

def create_series_structure(data, stage_or_group):
    if not data['events']:
        return {}

    first_event = data['events'][0]
    slug = first_event.get('season', {}).get('slug', 'unknown')
    stage = extract_round_name(stage_or_group)

    group_letter = stage_or_group.split("-")[1].upper() if stage_or_group.startswith("group-") else None
    defined_teams = GROUP_TEAMS.get(group_letter, []) if group_letter else []

    all_teams = set(defined_teams) if group_letter else set()
    all_games = []
    team_logo_map = {}

    # Collect logos
    for event in data['events']:
        for comp in event.get('competitions', []):
            for competitor in comp.get('competitors', []):
                team = competitor['team']
                name = team['displayName']
                logo = team.get('logo', '')
                team_logo_map[name] = logo

    for event in data['events']:
        for comp in event.get('competitions', []):
            competitors = comp.get('competitors', [])
            if len(competitors) != 2:
                continue

            team1_data = competitors[0]
            team2_data = competitors[1]
            team1 = team1_data['team']['displayName']
            team2 = team2_data['team']['displayName']

            # For groups: skip if not involving defined teams (optional strictness)
            if group_letter and not (team1 in defined_teams and team2 in defined_teams):
                continue

            all_teams.add(team1)
            all_teams.add(team2)

            status_obj = comp.get('status', {}).get('type', {})
            completed = status_obj.get('completed', False)
            state = status_obj.get('state', 'scheduled')  # pre, in, post

            if completed:
                game_status = "full_time"
            elif state == "in":
                game_status = "live"
            else:
                game_status = "scheduled"

            broadcast = ", ".join(b.get('names', ['TBD'])[0] for b in comp.get('broadcasts', []) if b.get('names'))
            venue = comp.get('venue', {}).get('fullName', 'TBD')
            date = comp.get('date', 'TBD')

            # Order by name alphabetically for consistency (Lowest = earlier name)
            if team1 <= team2:
                low_team, high_team = team1, team2
                low_data, high_data = team1_data, team2_data
            else:
                low_team, high_team = team2, team1
                low_data, high_data = team2_data, team1_data

            game = {
                "gameNumber": len(all_games) + 1,
                "Date": date,
                "Lowest Seed": {   # just alphabetical, not actual seed
                    "Name": low_team,
                    "Score": str(low_data.get('score', 0)),
                    "Logo": team_logo_map.get(low_team, ''),
                    "Advance": low_data.get('advance', False)
                },
                "Highest Seed": {
                    "Name": high_team,
                    "Score": str(high_data.get('score', 0)),
                    "Logo": team_logo_map.get(high_team, ''),
                    "Advance": high_data.get('advance', False)
                },
                "Broadcast": broadcast or "TBD",
                "Status": game_status,
                "Venue": venue
            }
            all_games.append(game)

    # Calculate standings / advancing
    advancing_teams = set()

    if stage.startswith("Group"):
        # Group standings
        team_stats = {t: {"points": 0, "gf": 0, "ga": 0, "played": 0} for t in all_teams}

        for game in all_games:
            if game["Status"] != "full_time":
                continue
            t1 = game["Lowest Seed"]["Name"]
            t2 = game["Highest Seed"]["Name"]
            s1 = int(game["Lowest Seed"]["Score"])
            s2 = int(game["Highest Seed"]["Score"])

            team_stats[t1]["played"] += 1
            team_stats[t2]["played"] += 1
            team_stats[t1]["gf"] += s1
            team_stats[t1]["ga"] += s2
            team_stats[t2]["gf"] += s2
            team_stats[t2]["ga"] += s1

            if s1 > s2:
                team_stats[t1]["points"] += 3
            elif s2 > s1:
                team_stats[t2]["points"] += 3
            else:
                team_stats[t1]["points"] += 1
                team_stats[t2]["points"] += 1

        # Sort: points > GD > GF
        sorted_teams = sorted(
            team_stats.keys(),
            key=lambda t: (
                team_stats[t]["points"],
                team_stats[t]["gf"] - team_stats[t]["ga"],
                team_stats[t]["gf"]
            ),
            reverse=True
        )

        # Top 2 advance for sure
        advancing_teams = set(sorted_teams[:2])

        # For 3rd place (collect all 3rds across groups later if needed)
        # Here we just mark group 3rd if applicable
        if len(sorted_teams) >= 3:
            advancing_teams.add(sorted_teams[2])  # but best 8 only advance; full logic needs all groups

    else:
        # Knockout
        for game in all_games:
            if game["Status"] in ["full_time", "live"]:
                s1 = int(game["Lowest Seed"]["Score"])
                s2 = int(game["Highest Seed"]["Score"])
                low = game["Lowest Seed"]["Name"]
                high = game["Highest Seed"]["Name"]
                if s1 > s2 or game["Lowest Seed"]["Advance"]:
                    advancing_teams.add(low)
                elif s2 > s1 or game["Highest Seed"]["Advance"]:
                    advancing_teams.add(high)

    series_title = f"{stage} Matches"
    series_status = f"{stage} {'Standings' if stage.startswith('Group') else 'Matches'}"

    return {
        series_title: {
            "seriesTitle": series_title,
            "seriesStatus": series_status,
            "seriesDetails": {
                "stage": stage,
                "Teams": list(all_teams),
                "AdvancingTeams": list(advancing_teams),
                "seriesGames": all_games,
                "maxGames": 6 if stage.startswith("Group") else len(all_games),  # per group 6 matches (4 teams)
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
        print(f"Saved to {filename}")
    except IOError as e:
        print(f"Error saving {filename}: {e}")

if __name__ == "__main__":
    print("Fetching 2026 FIFA World Cup data...")

    world_cup_stages = [
        (f"group-{chr(65+i)}", f"/config/www/fifa_worldcup_group_{chr(65+i)}_gpt.json") for i in range(12)
    ] + [
        ("round-of-32", "/config/www/fifa_worldcup_round_of_32_gpt.json"),
        ("round-of-16", "/config/www/fifa_worldcup_round_of_16_gpt.json"),
        ("quarterfinals", "/config/www/fifa_worldcup_quarterfinals_gpt.json"),
        ("semifinals", "/config/www/fifa_worldcup_semifinals_gpt.json"),
        ("third-place", "/config/www/fifa_worldcup_third_place_gpt.json"),  # if exists
        ("final", "/config/www/fifa_worldcup_final_gpt.json")
    ]

    for stage_or_group, filename in world_cup_stages:
        print(f"Processing {stage_or_group}...")
        round_data = fetch_and_filter_data(stage_or_group)
        round_series = create_series_structure(round_data, stage_or_group)
        combined = merge_original_and_series(round_data, round_series)
        save_to_file(filename, combined)
