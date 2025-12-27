import sys
import os
import glob
import pandas as pd

# Add src and project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config
from infrastructure.mapping.team_name_matcher import TeamNameMatcher
from shared.ipc_messenger import IPCMessenger

from infrastructure.mapping.league_name_matcher import LeagueNameMatcher

def main():
    print("🚀 Starting Team Mapping Tool...")
    print("--------------------------------")
    
    files = glob.glob(os.path.join(config.DIR_DATA_CRAWLED_BETINFO, "betinfo_proto_rate_*.csv"))
    if not files:
        print(f"❌ No Betinfo CSV files found in {config.DIR_DATA_CRAWLED_BETINFO}")
        return

    league_matcher = LeagueNameMatcher()
    print("ℹ️ Loaded League Mappings. Only teams from mapped leagues will be processed.")

    unique_teams = set()
    print(f"📂 Found {len(files)} Betinfo files. Scanning for teams in mapped leagues...")
    
    for f in files:
        try:
            df = pd.read_csv(f)
            # Check for various column name possibilities
            league_col = next((col for col in ['리그명', '리그', 'league', 'League', 'competition'] if col in df.columns), None)
            home_col = next((col for col in ['홈', '홈팀', 'Home', 'home_team'] if col in df.columns), None)
            away_col = next((col for col in ['원정', '원정팀', 'Away', 'away_team'] if col in df.columns), None)
            
            if not league_col or not (home_col or away_col):
                continue
                
            # Iterate rows to check league mapping
            for _, row in df.iterrows():
                league_name = str(row[league_col]).strip()
                # Check if this league is mapped (either in aliases or master dict)
                league_id = league_matcher.get_id_by_alias(league_name)
                
                if league_id:
                   # League is mapped, add teams
                   if home_col and pd.notna(row[home_col]):
                       unique_teams.update([str(row[home_col]).strip()])
                   if away_col and pd.notna(row[away_col]):
                       unique_teams.update([str(row[away_col]).strip()])
                else:
                    # League not mapped, skip teams
                    pass

        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")

    print(f"📋 Found {len(unique_teams)} unique teams.")
    
    matcher = TeamNameMatcher()
    
    mapped_count = 0
    skipped_count = 0
    failed_count = 0
    
    sorted_teams = sorted(list(unique_teams))
    
    for i, team_name in enumerate(sorted_teams, 1):
        print(f"\n[{i}/{len(sorted_teams)}] Processing: {team_name}")
        
        if team_name in matcher.learned_mappings:
            fs_id = matcher.learned_mappings[team_name]
            print(f"  ✅ Already mapped: {fs_id}")
            mapped_count += 1
            continue
            
        result = matcher.match(team_name, interactive=True)
        
        if result:
            mapped_count += 1
        else:
            print(f"  ⏭️ Skipped")
            skipped_count += 1

    print("\n--------------------------------")
    print("🎉 Mapping Session Completed!")
    print(f"✅ Mapped: {mapped_count}")
    print(f"⏭️ Skipped: {skipped_count}")
    print("--------------------------------")

if __name__ == "__main__":
    main()
