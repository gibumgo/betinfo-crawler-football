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

def run_mapping_logic(interactive: bool = True):
    IPCMessenger.log(f"🚀 Starting Team Mapping Tool (Interactive: {interactive})...", level="INFO")
    
    files = glob.glob(os.path.join(config.DIR_DATA_CRAWLED_BETINFO, "betinfo_proto_rate_*.csv"))
    if not files:
        IPCMessenger.send_error(404, f"No Betinfo CSV files found in {config.DIR_DATA_CRAWLED_BETINFO}")
        return

    league_matcher = LeagueNameMatcher()
    IPCMessenger.log("ℹ️ Loaded League Mappings. Only teams from mapped leagues will be processed.", level="INFO")

    unique_teams = set()
    skipped_leagues = set()
    IPCMessenger.log(f"📂 Found {len(files)} Betinfo files. Scanning...", level="INFO")
    IPCMessenger.send_progress(10)
    
    for f in files:
        try:
            df = pd.read_csv(f)
            league_col = next((col for col in ['리그명', '리그', 'league', 'League', 'competition'] if col in df.columns), None)
            home_col = next((col for col in ['홈', '홈팀', 'Home', 'home_team'] if col in df.columns), None)
            away_col = next((col for col in ['원정', '원정팀', 'Away', 'away_team'] if col in df.columns), None)
            
            if not league_col or not (home_col or away_col):
                continue
                
            for _, row in df.iterrows():
                league_name = str(row[league_col]).strip()
                league_id = league_matcher.get_id_by_alias(league_name)
                
                if league_id:
                   if home_col and pd.notna(row[home_col]):
                       unique_teams.update([str(row[home_col]).strip()])
                   if away_col and pd.notna(row[away_col]):
                       unique_teams.update([str(row[away_col]).strip()])
                else:
                    if league_name not in skipped_leagues:
                        skipped_leagues.add(league_name)
                        print(f"⚠️ [DEBUG] Skipped League: '{league_name}' (Not mapped)")

        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")

    if skipped_leagues:
        IPCMessenger.log(f"⚠️ Skipped {len(skipped_leagues)} unmapped leagues: {', '.join(skipped_leagues)}", level="WARN")

    IPCMessenger.log(f"📋 Found {len(unique_teams)} unique teams.", level="INFO")
    IPCMessenger.send_progress(30)
    
    matcher = TeamNameMatcher()
    
    mapped_count = 0
    skipped_count = 0
    auto_count = 0
    
    sorted_teams = sorted(list(unique_teams))
    total_teams = len(sorted_teams)
    
    for i, team_name in enumerate(sorted_teams, 1):
        progress = 30 + (i / total_teams * 70)
        IPCMessenger.send_status("MAPPING", f"{team_name} ({i}/{total_teams})")
        IPCMessenger.send_progress(progress)

        if team_name in matcher.knowledge_base:
            mapped_count += 1
            continue
            
        result = matcher.match(team_name, interactive=interactive)
        
        if result:
            mapped_count += 1
            if not interactive:
                auto_count += 1
                IPCMessenger.log(f"✅ Auto-mapped: {team_name} -> {result}", level="INFO")
        else:
            skipped_count += 1

    IPCMessenger.log(f"🎉 Mapping Completed! Mapped: {mapped_count} (New Auto: {auto_count}), Skipped: {skipped_count}", level="INFO")
    IPCMessenger.send_progress(100)

def run_auto_mode(args):
    """Entry point for Electron auto-mapping mode"""
    run_mapping_logic(interactive=False)

def main():
    run_mapping_logic(interactive=True)

if __name__ == "__main__":
    main()
