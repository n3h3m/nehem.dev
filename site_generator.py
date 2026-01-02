import os
import json
import glob
import re
import markdown
import shutil
from datetime import datetime

# Configuration
SETTINGS_FILE = 'settings.json'
TEMPLATE_FILE = 'themes/template.html'
POSTS_DIR = 'posts'
OUTPUT_DIR = 'docs' # Output directory

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        print(f"Error: {SETTINGS_FILE} not found.")
        return {}
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def load_template():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: {TEMPLATE_FILE} not found.")
        return ""
    with open(TEMPLATE_FILE, 'r') as f:
        return f.read()

def parse_post_dir(dirname):
    # Expected format: YYYY-MM-DD Title of Post
    # We need to handle potential colons or special chars in directory names
    basename = os.path.basename(dirname)
    match = re.match(r'(\d{4}-\d{2}-\d{2})\s+(.+)', basename)
    if match:
        return match.group(1), match.group(2)
    return None, basename

def process_markdown(content):
    # Extract tags if present (first line starting with "tags:")
    lines = content.split('\n')
    tags = ""
    start_idx = 0
    if lines and lines[0].lower().startswith('tags:'):
        tags = lines[0].split(':', 1)[1].strip()
        start_idx = 1
        # Skip empty lines after tags
        while start_idx < len(lines) and not lines[start_idx].strip():
            start_idx += 1
    
    body_md = '\n'.join(lines[start_idx:])
    
    # Auto-fix: Convert 3-space indentation to 4-space for list items
    # This fixes issues where some editors/users use 3 spaces which generic markdown parsers
    # might treat as top-level instead of nested.
    body_md = re.sub(r'^ {3}([-*+])', r'    \1', body_md, flags=re.MULTILINE)
    
    html_content = markdown.markdown(body_md, extensions=['fenced_code', 'tables'])
    return tags, html_content

def generate_site():
    settings = load_settings()
    template = load_template()
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    site_title = settings.get('site', {}).get('title', 'My Site')
    author_name = settings.get('author', {}).get('name', 'Author')
    author_bio = settings.get('author', {}).get('bio', '')

    posts_data = []

    # Find all post directories
    post_dirs = glob.glob(os.path.join(POSTS_DIR, '*'))
    
    for p_dir in post_dirs:
        if not os.path.isdir(p_dir):
            continue
        
        date_str, title = parse_post_dir(p_dir)
        if not date_str:
            print(f"Skipping {p_dir}: invalid directory name format.")
            continue

        # Find markdown file
        md_files = glob.glob(os.path.join(p_dir, '*.md'))
        if not md_files:
            continue
        
        post_file = md_files[0] # Assume one post per dir
        with open(post_file, 'r') as f:
            content = f.read()
        
        tags, html_content = process_markdown(content)
        
        # Create Slug
        slug = title.lower().replace(' ', '-').replace(':', '').replace('/', '') + '.html'
        
        posts_data.append({
            'title': title,
            'date': date_str,
            'url': slug,
            'content': html_content,
            'tags': tags
        })

    # Sort posts by date desc
    posts_data.sort(key=lambda x: x['date'], reverse=True)

    # Generate Sidebar Links (Top 5 recent)
    sidebar_links_html = ""
    for p in posts_data[:5]:
        sidebar_links_html += f'<li><a href="{p["url"]}">{p["title"]}</a></li>\n'
    
    # Search Index JS
    # We want format: { title: "...", url: "#" }
    # Using json.dumps to handle escaping safely
    search_objects = [{'title': p['title'], 'url': p['url']} for p in posts_data]
    search_index_js = ",\n".join([json.dumps(obj) for obj in search_objects])

    # Generate Individual Pages
    for i, post in enumerate(posts_data):
        # Calculate Previous (Older) and Next (Newer)
        # posts_data is desc (Newest first). 
        # Next Post (Newer) is i-1
        # Prev Post (Older) is i+1
        next_post = posts_data[i-1] if i > 0 else None
        prev_post = posts_data[i+1] if i < len(posts_data) - 1 else None
        
        nav_html = '<nav class="post-nav">'
        # Previous Node
        if prev_post:
            nav_html += f'''
            <a href="{prev_post['url']}" class="nav-btn">
                <span class="nav-label">Previous Node</span>
                <span class="nav-title">{prev_post['title']}</span>
            </a>'''
        else:
             nav_html += '''
            <div class="nav-btn disabled">
                <span class="nav-label">Previous Node</span>
                <span class="nav-title">/// NULL ///</span>
            </div>'''
        
        # Next Node
        if next_post:
            nav_html += f'''
            <a href="{next_post['url']}" class="nav-btn" style="text-align: right">
                <span class="nav-label">Next Node</span>
                <span class="nav-title">{next_post['title']}</span>
            </a>'''
        else:
             nav_html += '''
            <div class="nav-btn disabled" style="text-align: right">
                <span class="nav-label">Next Node</span>
                <span class="nav-title">/// NULL ///</span>
            </div>'''
        nav_html += '</nav>'
        # Simple string replacement (safe enough for this)
        page_html = template
        page_html = page_html.replace('{{ title }}', post['title'])
        page_html = page_html.replace('{{ site_title }}', site_title)
        page_html = page_html.replace('{{ content }}', post['content'])
        page_html = page_html.replace('{{ date }}', post['date'])
        page_html = page_html.replace('{{ author_name }}', author_name)
        page_html = page_html.replace('{{ author_bio }}', author_bio)
        page_html = page_html.replace('{{ tags }}', post['tags'])
        page_html = page_html.replace('{{ sidebar_links }}', sidebar_links_html)
        page_html = page_html.replace('{{ search_index_js }}', search_index_js)
        page_html = page_html.replace('{{ post_nav }}', nav_html)

        output_path = os.path.join(OUTPUT_DIR, post['url'])
        with open(output_path, 'w') as f:
            f.write(page_html)
        print(f"Generated {post['url']}")

    # Generate Index Page (Home)
    # Re-using template but replacing content with a list of posts
    index_content = "<h1>Recent Posts</h1><div class='technical-ruler'></div>"
    for post in posts_data:
        index_content += f"""
        <div style="margin-bottom: 2rem;">
            <h2><a href="{post['url']}">{post['title']}</a></h2>
            <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                {post['date']} | {post['tags']}
            </div>
            <p>{post['content'][:200]}...</p>
            <a href="{post['url']}">Read more -></a>
        </div>
        """
    
    index_html = template
    index_html = index_html.replace('{{ title }}', "Home")
    index_html = index_html.replace('{{ site_title }}', site_title)
    index_html = index_html.replace('{{ content }}', index_content)
    # Index meta
    index_html = index_html.replace('{{ date }}', datetime.now().strftime('%Y-%m-%d'))
    index_html = index_html.replace('{{ author_name }}', author_name)
    index_html = index_html.replace('{{ author_bio }}', author_bio)
    index_html = index_html.replace('{{ tags }}', "INDEX")
    index_html = index_html.replace('{{ sidebar_links }}', sidebar_links_html)
    index_html = index_html.replace('{{ search_index_js }}', search_index_js)
    index_html = index_html.replace('{{ post_nav }}', "")
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)
    print("Generated index.html")

if __name__ == "__main__":
    generate_site()
