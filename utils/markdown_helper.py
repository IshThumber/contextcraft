import re
import os
from slugify import slugify  # pip install python-slugify

def clean_and_save_draft(draft_response, output_dir="blog_drafts"):
    """
    Clean up a blog draft API response and save it as a Markdown file.
    
    Args:
        draft_response (dict): The API response containing the draft content
        output_dir (str): Directory where to save the markdown files
    
    Returns:
        str: Path to the saved markdown file
    """
    # Extract the raw content from the API response
    if isinstance(draft_response, dict) and "draft" in draft_response:
        content = draft_response["draft"]
    else:
        content = str(draft_response)
    
    # Remove any thinking process sections
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    
    # Remove extra newlines and whitespace
    content = content.strip()
    
    # Extract the title from the content
    title_match = re.search(r'\*\*(.*?)\*\*', content) or re.search(r'# (.*?)(\n|$)', content)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = "Untitled Blog Post"
    
    # Create a slug from the title for the filename
    filename = f"{slugify(title)}.md"
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the content to a markdown file
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Successfully saved: {file_path}")
    return file_path
