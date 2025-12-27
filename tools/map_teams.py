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

def main():
    print("🚀 Starting Team Mapping Tool...")
    print("--------------------------------")
    
    files = glob.glob(os.path.join(config.DIR_DATA_CRAWLED_BETINFO, "betinfo_proto_rate_*.csv"))
    if not files:
        print(f"❌ No Betinfo CSV files found in {config.DIR_DATA_CRAWLED_BETINFO}")
        return

    unique_teams = set()
    print(f"📂 Found {len(files)} Betinfo files. Scanning for teams...")
    
    for f in files:
        try:
            df = pd.read_csv(f)
            if '홈팀' in df.columns:
                unique_teams.update(df['홈팀'].dropna().unique())
            if '원정팀' in df.columns:
                unique_teams.update(df['원정팀'].dropna().unique())
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
