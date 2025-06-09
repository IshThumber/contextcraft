from openai import OpenAI
from dotenv import load_dotenv
import os
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

def generate_blog_topics(similar_blogs: list, user_input: str = ""):
    """Generate blog topic suggestions based on similar blogs and optional user input"""
    try:
        # Create examples from the user's previous blogs
        examples = "\n\n".join(f"Title: {b['title']}\nContent: {b['content']}" for b in similar_blogs)

        prompt = f"""
Based on the following blog history and trends:

{examples}

Suggest 5 new blog topics I could write about. {f"Also consider this input: {user_input}" if user_input else ""}
Only return the list of titles.
"""

        # Use the chat completions API, not embeddings API
        response = client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Parse the response into a list of topics
        topics_text = response.choices[0].message.content.strip()
        
        # Remove any thinking process sections
        if "<think>" in topics_text and "</think>" in topics_text:
            think_start = topics_text.find("<think>")
            think_end = topics_text.find("</think>") + len("</think>")
            topics_text = topics_text[:think_start] + topics_text[think_end:].strip()
        
        # Split by newlines
        topics_list = topics_text.split("\n")
        
        # Clean up the topics (remove numbering, quotes, etc.)
        cleaned_topics = []
        for t in topics_list:
            t = t.strip()
            if not t:
                continue
                
            # Remove numbering (like "1. " or "1) ")
            t = t.lstrip("0123456789.) ")
            
            # Remove quotes if present
            t = t.strip('"\'')
            
            # Skip any remaining thinking markers
            if t == "<think>" or t == "</think>" or t.startswith("<") and t.endswith(">"):
                continue
                
            # Add to clean list
            cleaned_topics.append(t)
        
        # Ensure we have a reasonable number of topics
        return cleaned_topics[:5]  # Return at most 5 topics
        
    except Exception as e:
        print(f"Error generating topics: {e}")
        # Return fallback topics if API fails
        return [
            "5 Ways to Improve Your Productivity",
            "The Future of AI in Everyday Life",
            "How to Balance Technology and Wellbeing",
            "Smart Tools for Better Time Management",
            "Automation Tips for Busy Professionals"
        ]


# Response from API: ChatCompletion(id='chatcmpl-047bcd4810bb4c22891cd30ee9469ca1', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='<think>\nOkay, let\'s see. The user has a blog history with multiple entries all titled "The Future of AI Agents" and the content is the same each time: "AI agents are evolving to become deeply personal..." They want five new blog topics about AI agents and their future impact.\n\nFirst, I need to figure out what\'s missing here. The current blogs seem repetitive, so the new topics should offer different angles. The key points from the history are personalization and evolution. The user\'s input mentions wanting to focus on AI agents and their future impact.\n\nSo, I should brainstorm topics that explore various aspects of AI agents beyond just personalization. Maybe ethical considerations, different industries they\'ll impact, collaboration between humans and AI, societal changes, or challenges in development.\n\nLet me list possible areas: ethics, industry applications (like healthcare, education), human-AI interaction, societal transformation, technical challenges. Each of these can be turned into a title that emphasizes the future impact.\n\nNeed to ensure the titles are unique and not repeating the same phrase. Use action verbs or questions to make them engaging. Also, check if the user might want to cover both positive impacts and potential issues. Maybe include a mix of opportunities and challenges.\n\nPossible titles:\n\n1. Ethical Implications of Personalized AI Agents in Daily Life\n2. How AI Agents Will Revolutionize Healthcare and Education\n3. The Rise of Collaborative Intelligence: Humans and AI Working Together\n4. AI Agents and the Future of Work: Transforming Industries and Job Roles\n5. Overcoming Technical Hurdles in Developing Autonomous AI Systems\n\nWait, does that cover different angles? Let me check. Ethics, specific industries (healthcare/education), collaboration, workforce impact, technical challenges. Yes, each is a unique angle. Make sure they tie back to future impact. The titles should be catchy but clear. Maybe use terms like "transforming," "revolutionize," "rise of," "overcoming." That should work.\n</think>\n\n1. Ethical Dilemmas in the Age of Hyper-Personalized AI Agents  \n2. AI Agents and the Workplace of Tomorrow: Collaboration or Replacement?  \n3. How AI Agents Will Reshape Mental Health and Personal Wellness  \n4. The Dark Side of Personalization: Privacy Risks in Autonomous AI Systems  \n5. AI Agents as Societal Architects: Bridging Gaps in Education and Accessibility', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[], reasoning_content=None), stop_reason=None)], created=1747559110, model='Qwen/Qwen3-235B-A22B', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=488, prompt_tokens=205, total_tokens=693, completion_tokens_details=None, prompt_tokens_details=None), prompt_logprobs=None)