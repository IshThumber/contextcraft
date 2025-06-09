from openai import OpenAI
from dotenv import load_dotenv
import os
import re
load_dotenv()

# Check if the API key is available
nebius_api_key = os.environ.get("NEBIUS_API_KEY")
if not nebius_api_key:
    print("Warning: NEBIUS_API_KEY not found in environment variables")

# Initialize the client
client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=nebius_api_key
)

def generate_draft_from_topic(topic: str, memory: list, extra_instructions: str = ""):
    """Generate a blog post draft based on a topic and memory of previous posts"""
    memory_context = "\n\n".join(f"Title: {b['title']}\nContent: {b['content']}" for b in memory)

    prompt = f"""
You are a blog writing assistant. The user has written previous blogs like:

{memory_context}

Now write a full blog post in the same style for the topic:
"{topic}"

{f"Extra instructions: {extra_instructions}" if extra_instructions else ""}

Use a friendly, clear tone. Structure the blog with a strong introduction, clear body, and a thoughtful conclusion.

Important: Do NOT include any <think> or thinking process sections in your response. Only provide the final blog post.
"""

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        # Get the raw content
        draft = response.choices[0].message.content.strip()
        
        # Remove any thinking process sections
        draft = remove_thinking_sections(draft)
        
        return draft
        
    except Exception as e:
        print(f"Error generating draft: {e}")
        return f"Error generating draft: {str(e)}"

def remove_thinking_sections(text):
    """Remove any thinking process sections from the generated text"""
    # Remove <think>...</think> sections
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Remove lines that look like thinking markers
    lines = text.split('\n')
    cleaned_lines = []
    in_thinking = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Skip thinking markers and sections
        if line_lower.startswith('<think') or line_lower == '<think>':
            in_thinking = True
            continue
        if line_lower.startswith('</think') or line_lower == '</think>':
            in_thinking = False
            continue
        if in_thinking:
            continue
            
        cleaned_lines.append(line)
    
    # Join the cleaned lines back together
    return '\n'.join(cleaned_lines)
