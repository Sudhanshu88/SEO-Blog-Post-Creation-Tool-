# example_usage.py
# Demonstration script for the SEO Blog Creation Tool

import os
import sys
from datetime import datetime

# Import our main tool (assuming it's in the same directory)
from seo_blog_tool import SEOBlogTool

def demo_basic_usage():
    """Demonstrate basic usage of the SEO Blog Tool"""
    print("=== SEO Blog Tool - Basic Usage Demo ===\n")
    
    # Initialize the tool
    tool = SEOBlogTool()
    
    # Run the pipeline with basic settings
    print("Starting blog creation pipeline...")
    results = tool.run_pipeline(
        category="electronics",
        max_products=3,
        publish_config=None  # No publishing, just local files
    )
    
    # Display results
    print(f"\n✅ Successfully created {len(results)} blog posts!")
    
    for i, result in enumerate(results, 1):
        product = result['product']
        blog_data = result['blog_data']
        print(f"\n--- Blog Post {i} ---")
        print(f"Product: {product.title}")
        print(f"Blog Title: {blog_data['title']}")
        print(f"Word Count: {blog_data['word_count']}")
        print(f"Keywords: {', '.join(blog_data['keywords'])}")
        print(f"Local File: {result['local_file']}")
    
    # Generate reports
    print("\nGenerating reports...")
    report_file = tool.generate_report()
    csv_file = tool.export_results_csv()
    
    print(f"📊 HTML Report: {report_file}")
    print(f"📈 CSV Export: {csv_file}")

def demo_advanced_usage():
    """Demonstrate advanced usage with publishing configuration"""
    print("\n=== SEO Blog Tool - Advanced Usage Demo ===\n")
    
    # Initialize the tool
    tool = SEOBlogTool()
    
    # Configure publishing (Note: Use real credentials in production)
    publish_config = {
        'wordpress': {
            'url': 'https://yourblog.wordpress.com',
            'username': 'your_username',
            'password': 'your_app_password'
        },
        'medium': 'your_medium_integration_token'
    }
    
    # Run with different categories
    categories = ["electronics", "home"]
    all_results = []
    
    for category in categories:
        print(f"Processing {category} category...")
        results = tool.run_pipeline(
            category=category,
            max_products=2,
            publish_config=None  # Set to publish_config to enable publishing
        )
        all_results.extend(results)
    
    print(f"\n✅ Created {len(all_results)} blog posts across {len(categories)} categories!")
    
    # Generate comprehensive report
    tool.generate_report("comprehensive_report.html")
    tool.export_results_csv("comprehensive_results.csv")

def demo_custom_workflow():
    """Demonstrate custom workflow with individual components"""
    print("\n=== SEO Blog Tool - Custom Workflow Demo ===\n")
    
    from seo_blog_tool import ProductScraper, KeywordResearcher, BlogContentGenerator
    
    # Initialize components individually
    scraper = ProductScraper()
    keyword_researcher = KeywordResearcher()
    content_generator = BlogContentGenerator()
    
    # Step 1: Scrape products
    print("Step 1: Scraping products...")
    products = scraper.scrape_amazon_bestsellers("electronics", 2)
    print(f"Found {len(products)} products")
    
    # Step 2: Process each product individually
    for product in products:
        print(f"\nProcessing: {product.title}")
        
        # Research keywords
        keywords = keyword_researcher.research_keywords(product.title)
        print(f"Keywords: {[kw.keyword for kw in keywords]}")
        
        # Generate content
        blog_data = content_generator.generate_blog_post(product, keywords)
        print(f"Generated: {blog_data['title']} ({blog_data['word_count']} words)")
        
        # Save to file
        filename = f"custom_blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {blog_data['title']}\n\n")
            f.write(blog_data['content'])
        print(f"Saved to: {filename}")

def demo_batch_processing():
    """Demonstrate batch processing for multiple categories"""
    print("\n=== SEO Blog Tool - Batch Processing Demo ===\n")
    
    tool = SEOBlogTool()
    
    # Configuration for batch processing
    batch_config = {
        "electronics": 3,
        "home": 2,
        "books": 2
    }
    
    total_posts = 0
    
    for category, count in batch_config.items():
        print(f"Processing {count} products from {category} category...")
        
        results = tool.run_pipeline(
            category=category,
            max_products=count
        )
        
        total_posts += len(results)
        print(f"Created {len(results)} blog posts for {category}")
    
    print(f"\n🎉 Batch processing complete! Total posts created: {total_posts}")
    
    # Generate final reports
    tool.generate_report("batch_processing_report.html")
    tool.export_results_csv("batch_processing_results.csv")

def demo_error_handling():
    """Demonstrate error handling capabilities"""
    print("\n=== SEO Blog Tool - Error Handling Demo ===\n")
    
    tool = SEOBlogTool()
    
    # Test with invalid configuration
    invalid_config = {
        'wordpress': {
            'url': 'https://invalid-url.com',
            'username': 'invalid_user',
            'password': 'invalid_pass'
        }
    }
    
    print("Testing error handling with invalid configuration...")
    
    try:
        results = tool.run_pipeline(
            category="electronics",
            max_products=1,
            publish_config=invalid_config
        )
        print("✅ Error handling worked! Blog posts created locally despite publishing failures.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function to run all demonstrations"""
    print("🚀 SEO Blog Creation Tool - Demonstration Script")
    print("=" * 50)
    
    # Create output directory
    os.makedirs("demo_output", exist_ok=True)
    os.chdir("demo_output")
    
    try:
        # Run demonstrations
        demo_basic_usage()
        demo_advanced_usage()
        demo_custom_workflow()
        demo_batch_processing()
        demo_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 All demonstrations completed successfully!")
        print("Check the demo_output directory for generated files.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("This might be due to network issues or missing dependencies.")
        print("Please check your internet connection and installed packages.")
    
    finally:
        # Return to original directory
        os.chdir("..")

if __name__ == "__main__":
    main()