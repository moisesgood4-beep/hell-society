#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Social Engineering Framework                   ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests, random
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

BANNER=f"""{BR}
███████╗██████╗  █████╗ ██╗    ██╗███╗   ██╗███████╗██████╗
██╔════╝██╔══██╗██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗
███████╗██████╔╝███████║██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝
╚════██║██╔═══╝ ██╔══██║██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████║██║     ██║  ██║╚███╔███╔╝██║ ╚████║███████╗██║  ██║
╚══════╝╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{Y}  Created by: HELL SOCIETY{RS}
"""

class SocialEngineering:
    def __init__(self, target_name=None, target_email=None, target_company=None):
        self.name = target_name or ""
        self.email = target_email or ""
        self.company = target_company or ""
        self.results = {}

    def generate_email_templates(self):
        print(f"\n{G}[+] Method 1: Email Templates{RS}")
        templates = {
            'phishing_urgent': f"""Subject: URGENT: Your account needs verification

Dear {self.name},

We noticed unusual activity on your account. Please verify your identity
by clicking the link below within 24 hours:

{f'https://{self.company.replace(" ","")}-verify.example.com/login' if self.company else 'https://verify.example.com/login'}

Failure to verify will result in account suspension.

Security Team""",

            'credential_reset': f"""Subject: Password Reset Required

Hello {self.name},

A password reset was requested for your account at {self.company or 'our service'}.
If you did not request this, please ignore this email.

Reset Link: {f'https://{self.company.replace(" ","")}-reset.example.com/reset' if self.company else 'https://reset.example.com/reset'}

This link expires in 2 hours.""",

            'it_support': f"""Subject: IT Support - System Update Required

Dear {self.name},

The IT department is performing mandatory updates to all workstations.
Please download and run the attached security patch.

If you have any questions, contact IT Support at:
{f'support@{self.company.replace(" ","").lower()}.com' if self.company else 'support@example.com'}

IT Department""",

            'hr_benefits': f"""Subject: Updated Benefits Package - Action Required

Dear {self.name},

HR has updated the benefits package. Please review and confirm your
selections by clicking below:

{f'https://hr.{self.company.replace(" ","").lower()}.com/benefits' if self.company else 'https://hr.example.com/benefits'}

Human Resources""",
        }

        for name, template in templates.items():
            print(f"\n  {C}=== {name.upper()} ==={RS}")
            for line in template.split('\n'):
                print(f"  {W}{line}")
        self.results['templates'] = templates

    def generate_credentials(self):
        print(f"\n{G}[+] Method 2: Password Generation (Based on target info){RS}")
        if self.name:
            name_parts = self.name.lower().split()
            first = name_parts[0] if name_parts else "user"
            last = name_parts[1] if len(name_parts) > 1 else "123"

            common_patterns = [
                f"{first}{last}",
                f"{first}.{last}",
                f"{first}{last}123",
                f"{first}{last}!",
                f"{first}{last}@2024",
                f"{first[0]}{last}",
                f"{first}{last[0]}!",
                f"{first.upper()}{last}!",
                f"{first}12345",
                f"{first.lower()}2024",
            ]

            for p in common_patterns:
                strength = len(p)
                print(f"  {Y}[~] {p} (length: {strength})")
            self.results['credential_patterns'] = common_patterns

    def gather_target_info(self):
        print(f"\n{G}[+] Method 3: Target Information Gathering{RS}")
        if self.name:
            # Search for target on social media
            search_queries = [
                f"site:linkedin.com \"{self.name}\"",
                f"site:twitter.com \"{self.name}\"",
                f"site:facebook.com \"{self.name}\"",
                f"site:instagram.com \"{self.name}\"",
                f"site:github.com \"{self.name}\"",
            ]
            print(f"  {Y}[i] Search queries:")
            for q in search_queries:
                print(f"  {C}  {q}")
            self.results['search_queries'] = search_queries

        if self.company:
            print(f"\n  {Y}[i] Company research:")
            print(f"  {C}  site:linkedin.com/company \"{self.company}\"")
            print(f"  {C}  site:glassdoor.com \"{self.company}\"")
            print(f"  {C}  site:linkedin.com inurl:company \"{self.company}\" employees")
            self.results['company_queries'] = [f"\"{self.company}\""]

    def voice_pretext(self):
        print(f"\n{G}[+] Method 4: Voice Pretext Scripts{RS}")
        pretexts = [
            f"""IT Support Call Script:
"Hello, this is IT Support from {self.company or 'the company'}.
I'm calling because we detected suspicious activity on the account
belonging to {self.name}. I need to verify some information
to secure the account."
""",
            f"""HR Verification Call Script:
"Hi, this is HR from {self.company or 'the company'}.
We're conducting annual verification of employee records.
Could you confirm your current address and phone number?"
""",
            f"""Bank/Finance Call Script:
"Good afternoon, this is the security department.
We need to verify your identity regarding a recent transaction
under the name {self.name}."
""",
        ]

        for p in pretexts:
            print(f"\n  {R}{p}{RS}")
        self.results['pretexts'] = pretexts

    def generate_phishing_page(self):
        print(f"\n{G}[+] Method 5: Phishing Page Generator{RS}")
        html = f"""<!DOCTYPE html>
<html>
<head><title>Login - {self.company or 'Secure Portal'}</title>
<style>body{{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh}}
.form{{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);width:350px}}
h2{{text-align:center;color:#1a73e8}}input{{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px}}
button{{width:100%;padding:12px;background:#1a73e8;color:white;border:none;border-radius:4px;cursor:pointer;font-size:16px}}
</style></head>
<body><div class="form">
<h2>{self.company or 'Sign In'}</h2>
<form action="capture.php" method="POST">
<input type="text" name="username" placeholder="Email or Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form>
<p style="text-align:center;color:#666;font-size:12px;margin-top:20px">
By signing in, you agree to our Terms of Service</p>
</div></body></html>"""
        outfile = "phishing_page.html"
        with open(outfile, 'w') as f:
            f.write(html)
        print(f"  {G}[✓] Phishing page saved: {outfile}")
        self.results['phishing_page'] = outfile

    def save_results(self):
        outfile = "social_engineering_results.json"
        with open(outfile, 'w') as f:
            json.dump({'target': self.name, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target Name:    {W}{self.name}")
        print(f"{B}[*] Target Email:   {W}{self.email}")
        print(f"{B}[*] Target Company: {W}{self.company}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.generate_email_templates()
        self.generate_credentials()
        self.gather_target_info()
        self.voice_pretext()
        self.generate_phishing_page()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Social Engineering Complete   ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Target name')
    parser.add_argument('-e', '--email', help='Target email')
    parser.add_argument('-c', '--company', help='Target company')
    args = parser.parse_args()
    se = SocialEngineering(args.name, args.email, args.company)
    se.run_all()

if __name__ == "__main__":
    main()
