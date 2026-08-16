import re
from typing import List

DIVERSITY_PATTERNS = {
    "BIPOC / Underrepresented Minorities": [
        r'\bbipoc\b', r'underrepresented minorities', r'people of color', r'racial equity', 
        r'minority-owned', r'black in tech', r'afro-descendant'
    ],
    "Women in Tech Initiatives": [
        r'women in tech', r'female engineers', r'women in stem', r'gender equality', 
        r'female leadership', r'women-led', r'maternity leave', r'equal pay'
    ],
    "African Diaspora Talent Programs": [
        r'african diaspora', r'diaspora talent', r'pan-african', r'africa tech', 
        r'emerging market talent', r'sub-saharan tech', r'returnee initiative'
    ],
    "Disability-Inclusive Opportunities": [
        r'disability-inclusive', r'accessibility', r'equal opportunity employer for individuals with disabilities', 
        r'reasonable accommodation', r'neurodiverse', r'neurodiversity'
    ],
    "LGBTQ+ Friendly Workplace Badges": [
        r'lgbtq\+?', r'lgbt', r'equal employment opportunity', r'inclusive workplace', 
        r'pride in tech', r'inclusive benefits'
    ],
    "DEI Commitment": [
        r'diversity, equity, and inclusion', r'diversity & inclusion', r'equal opportunity employer', 
        r'inclusive environment', r'belonging'
    ]
}

def extract_diversity_badges(text: str) -> List[str]:
    text_lower = text.lower()
    detected_badges = []
    
    for category, patterns in DIVERSITY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                if category not in detected_badges:
                    detected_badges.append(category)
                break
                
    return detected_badges
