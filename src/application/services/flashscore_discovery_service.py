import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from config import FLASHSCORE_BASE_URL, USER_AGENT

class FlashscoreDiscoveryService:
    BASE_URL = FLASHSCORE_BASE_URL

    def discover_leagues(self, country: str) -> List[Dict[str, str]]:
        country_slug = country.lower().replace(" ", "-")
        url = f"{self.BASE_URL}/soccer/{country_slug}/"
        
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        try:
            print(f"🔍 Fetching leagues for '{country}' from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            leagues = []
            seen_slugs = set()  
            candidates = soup.select(f"a[href*='/soccer/{country_slug}/']")
            
            for link in candidates:
                href = link.get('href')
                name = link.get_text(strip=True)
                
                if not href or not name:
                    continue
                
                parts = [p for p in href.split('/') if p]
                
                if len(parts) == 3 and parts[0] == 'soccer' and parts[1] == country_slug:
                    league_slug = parts[2]
                    
                    if league_slug in ['results', 'fixtures', 'standings', 'teams', 'squad']:
                        continue
                        
                    if league_slug in seen_slugs:
                        continue
                        
                    seen_slugs.add(league_slug)
                    leagues.append({
                        "name": name,
                        "slug": league_slug
                    })
            
            return leagues[:15]

        except Exception as e:
            print(f"❌ Error discovering leagues: {e}")
            return []

    def discover_countries(self) -> List[Dict[str, str]]:
        url = self.BASE_URL
        headers = {
            'User-Agent': USER_AGENT,
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        }
        
        try:
            print(f"🔍 Fetching country list from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            countries = []
            seen_slugs = set()
            
            region_links = soup.select(".lmc__block a[href^='/soccer/']")
            for link in region_links:
                href = link.get('href')
                
                name_span = link.select_one(".lmc__elementName")
                name = name_span.get_text(strip=True) if name_span else link.get_text(strip=True)
                
                if not href or not name:
                    continue
                    
                parts = [p for p in href.split('/') if p]
                if len(parts) == 2 and parts[0] == 'soccer':
                    slug = parts[1]
                    if slug not in seen_slugs and slug not in ['favorites', 'standing', 'results', 'fixtures']:
                        seen_slugs.add(slug)
                        countries.append({"name": name, "slug": slug})

            general_links = soup.select("a[href^='/soccer/']")
            
            for link in general_links:
                href = link.get('href')
                name = link.get_text(strip=True)
                
                if not href or not name:
                    continue
                
                parts = [p for p in href.split('/') if p]
                if len(parts) == 2 and parts[0] == 'soccer':
                    slug = parts[1]
                    
                    if slug in seen_slugs:
                        continue
                        
                    if slug in ['favorites', 'standing', 'results', 'fixtures', 'live']:
                        continue
                        
                    seen_slugs.add(slug)
                    
                    if len(name) > 50: 
                        continue
                        
                    countries.append({
                        "name": name,
                        "slug": slug
                    })
            
            print(f"✅ Found {len(countries)} countries/regions")
            return countries

        except Exception as e:
            print(f"❌ Error discovering countries: {e}")
            return []
