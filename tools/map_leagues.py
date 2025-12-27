import sys
import os
import glob
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config
from infrastructure.mapping.league_name_matcher import LeagueNameMatcher

def main():
    print("🚀 Starting League Mapping Tool...")
    print("--------------------------------")
    
    files = glob.glob(os.path.join(config.DIR_DATA_CRAWLED_BETINFO, "betinfo_proto_rate_*.csv"))
    unique_leagues = set()
    
    print(f"📂 Found {len(files)} Betinfo files. Scanning for leagues...")
    
    for f in files:
        try:
            df = pd.read_csv(f)
            possible_cols = ['리그명', '리그', 'league', 'League', 'competition']
            for col in possible_cols:
                if col in df.columns:
                    unique_leagues.update(df[col].dropna().unique())
        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")

    print(f"📋 Found {len(unique_leagues)} unique leagues.")
    
    matcher = LeagueNameMatcher()
    
    mapped_count = 0
    skipped_count = 0
    
    sorted_leagues = sorted(list(unique_leagues))
    
    for i, league_name in enumerate(sorted_leagues, 1):
        print(f"\n[{i}/{len(sorted_leagues)}] Processing: {league_name}")
        
        if league_name in matcher.learned_mappings:
             lid = matcher.learned_mappings[league_name]
             print(f"  ✅ Already mapped: {lid}")
             mapped_count += 1
             continue

        result = matcher.match(league_name, interactive=True)
        
        if result:
            mapped_count += 1
        else:
            print(f"  ⏭️ Skipped")
            skipped_count += 1

    print("\n--------------------------------")
    print("🎉 League Mapping Session Completed!")
    print(f"✅ Mapped: {mapped_count}")
    print(f"⏭️ Skipped: {skipped_count}")
    print("--------------------------------")

if __name__ == "__main__":
    main()
