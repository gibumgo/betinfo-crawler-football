import sys
import os
import glob
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config
from infrastructure.mapping.league_name_matcher import LeagueNameMatcher
from shared.ipc_messenger import IPCMessenger

def run_mapping_logic(interactive: bool = True):
    IPCMessenger.log(f"🚀 Starting League Mapping Tool (Interactive: {interactive})...", level="INFO")
    
    files = glob.glob(os.path.join(config.DIR_DATA_CRAWLED_BETINFO, "betinfo_proto_rate_*.csv"))
    unique_leagues = set()
    
    IPCMessenger.log(f"📂 Found {len(files)} Betinfo files. Scanning for leagues...", level="INFO")
    IPCMessenger.send_progress(10)
    
    for f in files:
        try:
            df = pd.read_csv(f)
            possible_cols = ['리그명', '리그', 'league', 'League', 'competition']
            for col in possible_cols:
                if col in df.columns:
                    unique_leagues.update(df[col].dropna().unique())
        except Exception as e:
            IPCMessenger.log(f"⚠️ Error reading {f}: {e}", level="WARN")

    IPCMessenger.log(f"📋 Found {len(unique_leagues)} unique leagues.", level="INFO")
    IPCMessenger.send_progress(30)
    
    matcher = LeagueNameMatcher()
    
    mapped_count = 0
    skipped_count = 0
    
    sorted_leagues = sorted(list(unique_leagues))
    total = len(sorted_leagues)
    
    for i, league_name in enumerate(sorted_leagues, 1):
        progress = 30 + (i / total * 70)
        IPCMessenger.send_status("MAPPING", f"{league_name} ({i}/{total})")
        IPCMessenger.send_progress(progress)
        
        if league_name in matcher.knowledge_base:
             mapped_count += 1
             continue

        result = matcher.match(league_name, interactive=interactive)
        
        if result:
            mapped_count += 1
            if not interactive:
                 IPCMessenger.log(f"✅ Auto-mapped: {league_name} -> {result}", level="INFO")
        else:
            skipped_count += 1

    IPCMessenger.log(f"🎉 League Mapping Completed! Mapped: {mapped_count}, Skipped: {skipped_count}", level="INFO")
    IPCMessenger.send_progress(100)

def run_auto_mode(args):
    """Entry point for Electron auto-mapping mode"""
    run_mapping_logic(interactive=False)

def main():
    run_mapping_logic(interactive=True)

if __name__ == "__main__":
    main()
