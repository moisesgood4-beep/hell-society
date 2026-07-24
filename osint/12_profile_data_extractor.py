#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PROFILE DATA EXTRACTOR v2.0                                     ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Profile Data Extraction                       ║
║  Description: Extract maximum data from social media profiles   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re
import time
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗ ██╗   ██╗███████╗████████╗                            ║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔════╝╚══██╔══╝                            ║
║{Fore.CYAN}  ██████╔╝██║   ██║███████╗   ██║                               ║
║{Fore.CYAN}  ██╔══██╗██║   ██║╚════██║   ██║                               ║
║{Fore.CYAN}  ██║  ██║╚██████╔╝███████║   ██║                               ║
║{Fore.CYAN}  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝                               ║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Profile Data Extractor v2.0                    {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

class ProfileExtractor:
    def __init__(self, username):
        self.username = username
        self.data = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })

    def extract_github(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  GITHUB EXTRACTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = self.session.get(f'https://api.github.com/users/{self.username}', timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  {Fore.GREEN}[+] Profile found")
                print(f"  {Fore.WHITE}  ID: {data.get('id')}")
                print(f"  {Fore.WHITE}  Name: {data.get('name')}")
                print(f"  {Fore.WHITE}  Login: {data.get('login')}")
                print(f"  {Fore.WHITE}  Email: {data.get('email', 'hidden')}")
                print(f"  {Fore.WHITE}  Bio: {data.get('bio')}")
                print(f"  {Fore.WHITE}  Location: {data.get('location')}")
                print(f"  {Fore.WHITE}  Company: {data.get('company')}")
                print(f"  {Fore.WHITE}  Blog: {data.get('blog')}")
                print(f"  {Fore.WHITE}  Twitter: {data.get('twitter_username')}")
                print(f"  {Fore.WHITE}  Public repos: {data.get('public_repos')}")
                print(f"  {Fore.WHITE}  Followers: {data.get('followers')}")
                print(f"  {Fore.WHITE}  Following: {data.get('following')}")
                print(f"  {Fore.WHITE}  Created: {data.get('created_at')}")
                print(f"  {Fore.WHITE}  Avatar: {data.get('avatar_url')}")
                print(f"  {Fore.WHITE}  URL: {data.get('html_url')}")

                self.data['github'] = data

                # Extract emails from repos
                try:
                    repos_resp = self.session.get(f'https://api.github.com/users/{self.username}/repos?per_page=100', timeout=10)
                    if repos_resp.status_code == 200:
                        repos = repos_resp.json()
                        print(f"\n  {Fore.CYAN}  Repositories ({len(repos)}):")
                        for repo in repos[:10]:
                            print(f"    {Fore.WHITE}• {repo['name']} - {repo.get('description', 'No desc')}")
                except:
                    pass
            else:
                print(f"  {Fore.YELLOW}[-] No GitHub profile")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def extract_twitter(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TWITTER/X EXTRACTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f'https://nitter.net/{self.username}'
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                profile_name = soup.find('a', class_='profile-card-fullname')
                profile_handle = soup.find('span', class_='profile-card-username')
                profile_bio = soup.find('div', class_='profile-bio')

                print(f"  {Fore.GREEN}[+] Twitter data accessible")
                if profile_name:
                    print(f"  {Fore.WHITE}  Name: {profile_name.text}")
                if profile_handle:
                    print(f"  {Fore.WHITE}  Handle: @{profile_handle.text}")
                if profile_bio:
                    print(f"  {Fore.WHITE}  Bio: {profile_bio.text}")

                # Extract tweets
                tweets = soup.find_all('div', class_='tweet-content')
                if tweets:
                    print(f"\n  {Fore.CYAN}  Recent tweets ({len(tweets)}):")
                    for tweet in tweets[:5]:
                        print(f"    {Fore.WHITE}• {tweet.text[:100]}")

                self.data['twitter'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] Twitter not accessible")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def extract_instagram(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  INSTAGRAM EXTRACTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f'https://www.instagram.com/{self.username}/'
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                # Try to extract from JSON data
                json_match = re.search(r'"profilePage_[^"]*":\s*(\{.*?\})\s*\}', resp.text)
                if json_match:
                    try:
                        data = json.loads(json_match.group(1))
                        user = data.get('graphql', {}).get('user', {})
                        print(f"  {Fore.GREEN}[+] Instagram data extracted")
                        print(f"  {Fore.WHITE}  Username: {user.get('username')}")
                        print(f"  {Fore.WHITE}  Full name: {user.get('full_name')}")
                        print(f"  {Fore.WHITE}  Bio: {user.get('biography')}")
                        print(f"  {Fore.WHITE}  Posts: {user.get('edge_owner_to_timeline_media', {}).get('count')}")
                        print(f"  {Fore.WHITE}  Followers: {user.get('edge_followed_by', {}).get('count')}")
                        print(f"  {Fore.WHITE}  Following: {user.get('edge_follow', {}).get('count')}")
                        print(f"  {Fore.WHITE}  External URL: {user.get('external_url')}")
                        print(f"  {Fore.WHITE}  Business email: {user.get('business_email')}")
                        self.data['instagram'] = {'found': True, 'url': url}
                    except:
                        print(f"  {Fore.WHITE}  Profile accessible")
                        self.data['instagram'] = {'found': True, 'url': url}
                else:
                    print(f"  {Fore.WHITE}  Profile accessible")
                    self.data['instagram'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] Instagram not accessible")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def extract_linkedin(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  LINKEDIN EXTRACTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f'https://www.linkedin.com/in/{self.username}'
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                print(f"  {Fore.GREEN}[+] LinkedIn profile accessible")
                print(f"  {Fore.WHITE}  URL: {url}")

                # Extract visible data
                soup = BeautifulSoup(resp.text, 'html.parser')

                # Try to find name
                name = soup.find('h1')
                if name:
                    print(f"  {Fore.WHITE}  Name: {name.text.strip()}")

                # Try to find headline
                headline = soup.find('h2')
                if headline:
                    print(f"  {Fore.WHITE}  Headline: {headline.text.strip()}")

                self.data['linkedin'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] LinkedIn not accessible")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def extract_reddit(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  REDDIT EXTRACTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = self.session.get(
                f'https://www.reddit.com/user/{self.username}/about.json',
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get('data', {})
                print(f"  {Fore.GREEN}[+] Reddit data extracted")
                print(f"  {Fore.WHITE}  Username: {data.get('name')}")
                print(f"  {Fore.WHITE}  Created: {time.strftime('%Y-%m-%d', time.gmtime(data.get('created_utc', 0)))}")
                print(f"  {Fore.WHITE}  Link karma: {data.get('link_karma')}")
                print(f"  {Fore.WHITE}  Comment karma: {data.get('comment_karma')}")
                print(f"  {Fore.WHITE}  Total karma: {data.get('total_karma')}")

                # Get recent posts
                posts_resp = self.session.get(
                    f'https://www.reddit.com/user/{self.username}/submitted.json?limit=10',
                    timeout=10
                )
                if posts_resp.status_code == 200:
                    posts = posts_resp.json().get('data', {}).get('children', [])
                    print(f"\n  {Fore.CYAN}  Recent posts ({len(posts)}):")
                    for post in posts[:5]:
                        p = post.get('data', {})
                        print(f"    {Fore.WHITE}• r/{p.get('subreddit')} - {p.get('title', '')[:50]}")

                self.data['reddit'] = data
            else:
                print(f"  {Fore.YELLOW}[-] No Reddit profile")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def extract_other_platforms(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  OTHER PLATFORMS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        platforms = {
            'TikTok': f'https://www.tiktok.com/@{self.username}',
            'Twitch': f'https://www.twitch.tv/{self.username}',
            'Pinterest': f'https://www.pinterest.com/{self.username}/',
            'Tumblr': f'https://{self.username}.tumblr.com/',
            'Steam': f'https://steamcommunity.com/id/{self.username}',
            'Spotify': f'https://open.spotify.com/user/{self.username}',
            'Medium': f'https://{self.username}.medium.com/',
            'Dev.to': f'https://dev.to/{self.username}',
            'StackOverflow': f'https://stackoverflow.com/users/?tab=accounts&q={self.username}',
            'Keybase': f'https://keybase.io/{self.username}',
            'Patreon': f'https://www.patreon.com/{self.username}',
            'SoundCloud': f'https://soundcloud.com/{self.username}',
            'Vimeo': f'https://vimeo.com/{self.username}',
            'Flickr': f'https://www.flickr.com/people/{self.username}/',
            'Behance': f'https://www.behance.net/{self.username}',
            'Dribbble': f'https://dribbble.com/{self.username}',
            'SlideShare': f'https://www.slideshare.net/{self.username}',
            'Quora': f'https://www.quora.com/profile/{self.username}',
            'Facebook': f'https://www.facebook.com/{self.username}',
            'YouTube': f'https://www.youtube.com/@{self.username}',
        }

        found = []
        not_found = []

        for platform, url in platforms.items():
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    found.append(platform)
                    print(f"  {Fore.GREEN}[+] {platform}: FOUND")
                else:
                    not_found.append(platform)
                    print(f"  {Fore.YELLOW}[-] {platform}: Not found")
            except:
                not_found.append(platform)
                print(f"  {Fore.RED}[!] {platform}: Error")

        self.data['other_platforms'] = {'found': found, 'not_found': not_found}

        print(f"\n  {Fore.GREEN}[+] Platforms with profile: {len(found)}/{len(platforms)}")

    def extract_contact_info(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CONTACT INFORMATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Try to find email patterns in username
        print(f"  {Fore.WHITE}[*] Possible email addresses:")
        email_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com', 'icloud.com']
        for domain in email_domains:
            print(f"    {Fore.CYAN}• {self.username}@{domain}")

        # Try Gravatar
        for domain in email_domains:
            email = f'{self.username}@{domain}'
            hash_val = hashlib.md5(email.encode().strip().lower()).hexdigest()
            gravatar_url = f'https://www.gravatar.com/avatar/{hash_val}?d=404'
            try:
                resp = self.session.head(gravatar_url, timeout=5)
                if resp.status_code == 200:
                    print(f"  {Fore.GREEN}[+] Gravatar match: {email}")
                    self.data['verified_email'] = email
                    break
            except:
                pass

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.username}")
        print(f"{Fore.CYAN}  [*] Starting full profile extraction...\n")

        self.extract_github()
        self.extract_twitter()
        self.extract_instagram()
        self.extract_linkedin()
        self.extract_reddit()
        self.extract_other_platforms()
        self.extract_contact_info()

        # Save all data
        results_file = f'/tmp/profile_extract_{self.username}.json'
        with open(results_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Full data saved: {results_file}")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  PROFILE EXTRACTION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Profile Data Extractor')
    parser.add_argument('-u', '--username', required=True, help='Target username')
    args = parser.parse_args()

    extractor = ProfileExtractor(args.username)
    extractor.run()
