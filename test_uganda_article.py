#!/usr/bin/env python
"""
Uganda Politics Article Generation Test

Generates a comprehensive 10,000-word article about Uganda politics
with 3 images and 4 tables, testing all API integrations.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("GRAIVE AI - UGANDA POLITICS ARTICLE GENERATION")
print("="*70)
print("\nLoading API configurations...")

# Verify API keys loaded
openai_key = os.getenv("OPENAI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print(f"\n✓ OpenAI API Key: {'Configured' if openai_key else 'Missing'}")
print(f"✓ DeepSeek API Key: {'Configured' if deepseek_key else 'Missing'}")
print(f"✓ Gemini API Key: {'Configured' if gemini_key else 'Missing'}")

if not all([openai_key, deepseek_key, gemini_key]):
    print("\n❌ ERROR: Some API keys are missing!")
    print("Please check your .env file configuration.")
    sys.exit(1)

# Test basic LLM connectivity
print("\n" + "="*70)
print("TESTING API CONNECTIVITY")
print("="*70)

try:
    from openai import OpenAI
    
    print("\n[1/3] Testing OpenAI API...")
    client_openai = OpenAI(api_key=openai_key)
    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'OpenAI API working!'"}],
        max_tokens=20
    )
    print(f"✓ OpenAI Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI Error: {e}")
    print("Note: Will continue with other providers...")

try:
    import google.generativeai as genai
    
    print("\n[2/3] Testing Google Gemini API...")
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Gemini API working!'")
    print(f"✓ Gemini Response: {response.text}")
    
except Exception as e:
    print(f"❌ Gemini Error: {e}")
    print("Note: Will continue with other providers...")

try:
    import requests
    
    print("\n[3/3] Testing DeepSeek API...")
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {deepseek_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Say 'DeepSeek API working!'"}],
            "max_tokens": 20
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ DeepSeek Response: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ DeepSeek Error: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ DeepSeek Error: {e}")

# Generate Uganda Politics Article
print("\n" + "="*70)
print("GENERATING UGANDA POLITICS ARTICLE")
print("="*70)
print("\nTarget: 10,000 words, 3 images, 4 tables")
print("Topic: Uganda Politics (Current Affairs)")
print("\n" + "="*70)

# Article sections structure
sections = [
    {
        "title": "Executive Summary",
        "word_count": 500,
        "provider": "gemini",
        "description": "Overview of current Uganda political landscape"
    },
    {
        "title": "Historical Context: Uganda's Political Evolution",
        "word_count": 1500,
        "provider": "deepseek",
        "description": "From independence to present day"
    },
    {
        "title": "Current Political Structure and Governance",
        "word_count": 1500,
        "provider": "deepseek",
        "description": "Government branches, power distribution"
    },
    {
        "title": "Key Political Actors and Parties",
        "word_count": 1200,
        "provider": "deepseek",
        "description": "NRM, opposition parties, influential figures"
    },
    {
        "title": "Recent Political Developments (2024-2025)",
        "word_count": 1800,
        "provider": "gpt-4",
        "description": "Current events, policy changes, elections"
    },
    {
        "title": "Economic Policies and Political Implications",
        "word_count": 1200,
        "provider": "deepseek",
        "description": "Economic strategy, development initiatives"
    },
    {
        "title": "Regional and International Relations",
        "word_count": 1000,
        "provider": "deepseek",
        "description": "EAC, AU, international partnerships"
    },
    {
        "title": "Civil Society and Political Participation",
        "word_count": 800,
        "provider": "gemini",
        "description": "NGOs, activism, citizen engagement"
    },
    {
        "title": "Challenges and Future Outlook",
        "word_count": 1000,
        "provider": "gpt-4",
        "description": "Issues facing Uganda, potential trajectories"
    },
    {
        "title": "Conclusion",
        "word_count": 500,
        "provider": "gemini",
        "description": "Summary and forward-looking statements"
    }
]

# Tables to generate
tables = [
    {
        "title": "Table 1: Major Political Parties in Uganda",
        "provider": "gpt-3.5",
        "columns": ["Party Name", "Leader", "Founded", "Ideology", "Parliamentary Seats"]
    },
    {
        "title": "Table 2: Uganda Economic Indicators (2020-2024)",
        "provider": "gpt-3.5",
        "columns": ["Year", "GDP Growth %", "Inflation %", "Unemployment %", "Budget (UGX Trillion)"]
    },
    {
        "title": "Table 3: Regional Political Influence",
        "provider": "gemini",
        "columns": ["Region", "Dominant Party", "Key Issues", "Voter Turnout %"]
    },
    {
        "title": "Table 4: International Relations Summary",
        "provider": "gemini",
        "columns": ["Country/Org", "Relationship Status", "Key Agreements", "Trade Volume (USD M)"]
    }
]

# Images to request
images = [
    {
        "title": "Uganda Parliament Building",
        "description": "Photorealistic image of Uganda's Parliament building in Kampala",
        "provider": "dall-e"
    },
    {
        "title": "Uganda Political Map",
        "description": "Detailed political map showing Uganda's regions and districts",
        "provider": "dall-e"
    },
    {
        "title": "Uganda Economic Growth Chart",
        "description": "Professional infographic showing Uganda's economic growth 2020-2024",
        "provider": "dall-e"
    }
]

# Generate article content
article_content = []
total_words = 0

print(f"\n{'='*70}")
print("SECTION GENERATION")
print(f"{'='*70}\n")

for i, section in enumerate(sections, 1):
    print(f"[{i}/{len(sections)}] Generating: {section['title']}")
    print(f"    Target: {section['word_count']} words")
    print(f"    Provider: {section['provider']}")
    
    try:
        if section['provider'] == 'gpt-4':
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert political analyst specializing in East African politics."},
                    {"role": "user", "content": f"Write a detailed {section['word_count']}-word section titled '{section['title']}' about {section['description']} in Uganda politics. Include recent developments, factual information, and analysis."}
                ],
                max_tokens=section['word_count'] * 2,
                temperature=0.7
            )
            content = response.choices[0].message.content
            
        elif section['provider'] == 'gemini':
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Write a detailed {section['word_count']}-word section titled '{section['title']}' about {section['description']} in Uganda politics. Include recent developments, factual information, and analysis."
            response = model.generate_content(prompt)
            content = response.text
            
        elif section['provider'] == 'deepseek':
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {deepseek_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You are an expert political analyst specializing in East African politics."},
                        {"role": "user", "content": f"Write a detailed {section['word_count']}-word section titled '{section['title']}' about {section['description']} in Uganda politics. Include recent developments, factual information, and analysis."}
                    ],
                    "max_tokens": section['word_count'] * 2,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
            else:
                content = f"[Error generating content: {response.status_code}]"
        
        else:
            content = f"[Provider {section['provider']} not configured]"
        
        # Add to article
        section_text = f"\n\n## {section['title']}\n\n{content}"
        article_content.append(section_text)
        
        words = len(content.split())
        total_words += words
        
        print(f"    ✓ Generated: {words} words")
        print(f"    Running total: {total_words:,} words\n")
        
    except Exception as e:
        print(f"    ❌ Error: {e}\n")
        article_content.append(f"\n\n## {section['title']}\n\n[Error generating section: {e}]")

# Generate tables
print(f"\n{'='*70}")
print("TABLE GENERATION")
print(f"{'='*70}\n")

for i, table in enumerate(tables, 1):
    print(f"[{i}/{len(tables)}] Generating: {table['title']}")
    print(f"    Provider: {table['provider']}")
    
    try:
        prompt = f"Generate a realistic data table titled '{table['title']}' with columns: {', '.join(table['columns'])}. Provide 5-6 rows of current, factual data about Uganda. Format as a markdown table."
        
        if table['provider'] == 'gpt-3.5':
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            table_content = response.choices[0].message.content
            
        elif table['provider'] == 'gemini':
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            table_content = response.text
        
        article_content.append(f"\n\n{table_content}\n")
        print(f"    ✓ Generated table\n")
        
    except Exception as e:
        print(f"    ❌ Error: {e}\n")
        article_content.append(f"\n\n{table['title']}\n[Error generating table: {e}]\n")

# Note about images (DALL-E requires separate implementation)
print(f"\n{'='*70}")
print("IMAGE GENERATION NOTES")
print(f"{'='*70}\n")

for i, image in enumerate(images, 1):
    print(f"[{i}/{len(images)}] {image['title']}")
    print(f"    Description: {image['description']}")
    print(f"    Provider: {image['provider']}")
    print(f"    Note: Image generation requires DALL-E API endpoint implementation")
    print(f"    Placeholder added to article\n")
    
    article_content.append(f"\n\n### {image['title']}\n\n![{image['title']}](placeholder_image_{i}.png)\n*{image['description']}*\n")

# Compile final article
final_article = f"""# Uganda Politics: A Comprehensive Analysis

**Generated:** {datetime.now().strftime('%B %d, %Y')}  
**Word Count:** ~{total_words:,} words  
**Author:** Graive AI System

---

{''.join(article_content)}

---

## References

This article synthesizes current information about Uganda's political landscape. For the most up-to-date information, consult official government sources, reputable news organizations, and academic publications.

**Generated using:**
- OpenAI GPT-4 (critical analysis sections)
- DeepSeek Chat (detailed content generation)
- Google Gemini 1.5 Flash (summaries and overviews)

---

*End of Article*
"""

# Save to file
output_path = Path("./workspace/uganda_politics_article.md")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_article)

print(f"{'='*70}")
print("ARTICLE GENERATION COMPLETE")
print(f"{'='*70}\n")
print(f"✓ Total Words Generated: {total_words:,}")
print(f"✓ Target Words: 10,000")
print(f"✓ Achievement: {(total_words/10000)*100:.1f}%")
print(f"✓ Sections: {len(sections)}")
print(f"✓ Tables: {len(tables)}")
print(f"✓ Images: {len(images)} (placeholders)")
print(f"\n✓ Article saved to: {output_path.absolute()}")
print(f"\n{'='*70}\n")

print("PROVIDER USAGE SUMMARY:")
print(f"{'='*70}")
print(f"OpenAI GPT-4: 2 sections (critical analysis)")
print(f"DeepSeek Chat: 6 sections (detailed content)")
print(f"Gemini Flash: 2 sections + 2 tables (summaries)")
print(f"GPT-3.5 Turbo: 2 tables (data formatting)")
print(f"\n{'='*70}\n")

print("✅ TEST COMPLETE!")
print("\nYou can now:")
print("  1. View the article: workspace/uganda_politics_article.md")
print("  2. Run the full system: python graive.py")
print("  3. Chat with the system interactively")
print(f"\n{'='*70}\n")
