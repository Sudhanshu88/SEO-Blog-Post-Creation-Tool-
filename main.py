#!/usr/bin/env python3
"""
SEO Blog Generator with Ubersuggest Keyword Scraping
Generates 150-200 word SEO blog posts using template-based approach
"""

import requests
from bs4 import BeautifulSoup
import random
import time
from urllib.parse import quote_plus
import re
from typing import List, Dict

class SEOBlogGenerator:
    def _init_(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_keywords_from_ubersuggest(self, product_name: str) -> List[str]:
        """
        Extract keywords from Ubersuggest for the given product name
        Returns 3-4 relevant keywords
        """
        try:
            # Format the search URL
            encoded_product = quote_plus(product_name)
            search_url = f"https://neilpatel.com/ubersuggest/?keyword={encoded_product}"
            
            print(f"Fetching keywords from: {search_url}")
            
            # Add delay to be respectful
            time.sleep(2)
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            keywords = []
            
            # Try multiple selectors to find keyword suggestions
            selectors = [
                '.keyword-suggestion',
                '.keyword-item',
                '[data-keyword]',
                '.suggestion-item',
                '.related-keyword'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    keyword_text = None
                    
                    # Try different ways to extract keyword text
                    if element.get('data-keyword'):
                        keyword_text = element.get('data-keyword')
                    elif element.text:
                        keyword_text = element.text.strip()
                    
                    if keyword_text and len(keyword_text) > 3:
                        # Clean the keyword
                        keyword_text = re.sub(r'[^\w\s]', '', keyword_text).strip()
                        if keyword_text and keyword_text.lower() not in [k.lower() for k in keywords]:
                            keywords.append(keyword_text)
                            
                    if len(keywords) >= 4:
                        break
                        
                if len(keywords) >= 4:
                    break
            
            # If we couldn't scrape enough keywords, generate some based on the product
            if len(keywords) < 3:
                print("Couldn't scrape enough keywords, generating fallback keywords...")
                keywords = self.generate_fallback_keywords(product_name)
            
            return keywords[:4]  # Return max 4 keywords
            
        except Exception as e:
            print(f"Error scraping Ubersuggest: {e}")
            print("Using fallback keyword generation...")
            return self.generate_fallback_keywords(product_name)
    
    def generate_fallback_keywords(self, product_name: str) -> List[str]:
        """
        Generate fallback keywords when scraping fails
        """
        product_lower = product_name.lower()
        
        # Common keyword patterns
        patterns = [
            f"best {product_lower}",
            f"affordable {product_lower}",
            f"top {product_lower}",
            f"{product_lower} reviews",
            f"cheap {product_lower}",
            f"{product_lower} deals",
            f"premium {product_lower}",
            f"{product_lower} guide",
            f"{product_lower} comparison",
            f"buy {product_lower}"
        ]
        
        # Shuffle and return 4 keywords
        random.shuffle(patterns)
        return patterns[:4]
    
    def generate_blog_post(self, product_name: str, keywords: List[str]) -> str:
        """
        Generate SEO blog post using template-based approach
        """
        if len(keywords) < 3:
            raise ValueError("Please provide at least 3 keywords.")
        
        # Assign individual keywords
        k1, k2, k3 = keywords[0], keywords[1], keywords[2]
        k4 = keywords[3] if len(keywords) > 3 else None
        
        # Template variations for dynamic content
        intro_templates = [
            f"In the world of modern technology, {product_name} have become a must-have for anyone seeking convenience and performance. Whether you're a student, professional, or casual user, these products are changing the way we experience the digital world.",
            f"Today's market for {product_name} is more competitive than ever, offering consumers incredible choices for their daily needs. From budget-friendly options to premium models, there's something for everyone looking to upgrade their tech arsenal.",
            f"The demand for {product_name} continues to grow as more people discover their versatility and value. These innovative products are transforming how we work, play, and stay connected in our fast-paced digital lives."
        ]
        
        features_templates = [
            f"One of the most searched terms today is \"{k1}\" — a clear sign that users want top-notch performance. Alongside that, many shoppers are looking for \"{k2}\" and \"{k3}\" when making a purchase decision.",
            f"Market research shows that \"{k1}\" is trending among consumers who prioritize quality and value. Similarly, \"{k2}\" and \"{k3}\" are frequently searched terms that indicate what buyers really want.",
            f"Consumer behavior analysis reveals that \"{k1}\" remains a top priority for smart shoppers. The growing interest in \"{k2}\" and \"{k3}\" also demonstrates the evolving needs of today's tech-savvy users."
        ]
        
        benefits_templates = [
            f"{product_name} often combine cutting-edge features with sleek design, offering something for everyone. With strong battery life, noise isolation, and seamless connectivity, they're redefining portable audio and productivity.",
            f"What makes {product_name} stand out is their perfect balance of functionality and style. Modern versions feature enhanced durability, improved performance, and user-friendly interfaces that make them ideal for daily use.",
            f"The latest {product_name} showcase remarkable innovation in both design and technology. From extended battery life to superior build quality, these products deliver exceptional value for money."
        ]
        
        conclusion_templates = [
            f"If you're in the market for a new gadget or accessory, consider exploring options that match these trending needs. {product_name} continue to impress users and reviewers alike, making them a smart investment in 2025.",
            f"With so many excellent options available, now is the perfect time to invest in quality {product_name}. Their combination of affordability and advanced features makes them an excellent choice for any budget.",
            f"The future looks bright for {product_name} as manufacturers continue to innovate and improve. Whether you're upgrading or buying for the first time, you can't go wrong with today's top-rated models."
        ]
        
        # Randomly select templates for variety
        intro = random.choice(intro_templates)
        features = random.choice(features_templates)
        benefits = random.choice(benefits_templates)
        conclusion = random.choice(conclusion_templates)
        
        # Add the fourth keyword if available
        if k4:
            features += f" Not to mention, \"{k4}\" is gaining popularity for those seeking extra value."
        
        # Combine all sections
        blog_post = f"{intro}\n\n{features}\n\n{benefits}\n\n{conclusion}"
        
        return blog_post
    
    def get_word_count(self, text: str) -> int:
        """Count words in the generated blog post"""
        return len(text.split())
    
    def run_generator(self, product_name: str) -> Dict[str, any]:
        """
        Main function to run the complete blog generation process
        """
        print(f"🚀 Starting SEO blog generation for: {product_name}")
        print("=" * 50)
        
        # Step 1: Extract keywords
        print("📝 Step 1: Extracting keywords from Ubersuggest...")
        keywords = self.extract_keywords_from_ubersuggest(product_name)
        print(f"✅ Found keywords: {keywords}")
        
        # Step 2: Generate blog post
        print("\n📝 Step 2: Generating SEO blog post...")
        blog_post = self.generate_blog_post(product_name, keywords)
        word_count = self.get_word_count(blog_post)
        
        print(f"✅ Blog post generated successfully!")
        print(f"📊 Word count: {word_count} words")
        
        return {
            'product_name': product_name,
            'keywords': keywords,
            'blog_post': blog_post,
            'word_count': word_count
        }

def main():
    """
    Main function to run the SEO blog generator
    """
    generator = SEOBlogGenerator()
    
    # Get product name from user
    product_name = input("Enter the product name: ").strip()
    
    if not product_name:
        print("❌ Product name cannot be empty!")
        return
    
    try:
        # Generate the blog post
        result = generator.run_generator(product_name)
        
        # Display results
        print("\n" + "=" * 50)
        print("🎉 GENERATED SEO BLOG POST")
        print("=" * 50)
        print(f"Product: {result['product_name']}")
        print(f"Keywords: {', '.join(result['keywords'])}")
        print(f"Word Count: {result['word_count']}")
        print("\n" + "-" * 50)
        print("BLOG POST CONTENT:")
        print("-" * 50)
        print(result['blog_post'])
        print("\n" + "=" * 50)
        
        # Save to file
        filename = f"seo_blog_{product_name.replace(' ', '_').lower()}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Product: {result['product_name']}\n")
            f.write(f"Keywords: {', '.join(result['keywords'])}\n")
            f.write(f"Word Count: {result['word_count']}\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*50 + "\n")
            f.write(result['blog_post'])
        
        print(f"💾 Blog post saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()