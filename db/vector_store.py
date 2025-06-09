from db.supabase_client import supabase
from openai import OpenAI
import os
import numpy as np
from dotenv import load_dotenv
from sklearn.decomposition import PCA

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

# Set a consistent dimension for all embeddings
EMBEDDING_DIMENSION = 3584

def dimension_reduction(embedding, target_dim=EMBEDDING_DIMENSION):
    """Reduce the dimensionality of an embedding vector"""
    if len(embedding) <= target_dim:
        # If the embedding is already smaller than target, pad with zeros
        return embedding + [0] * (target_dim - len(embedding))
        
    # Use PCA for dimension reduction of larger vectors
    try:
        # Reshape for PCA
        embedding_array = np.array(embedding).reshape(1, -1)
        pca = PCA(n_components=target_dim)
        reduced = pca.fit_transform(embedding_array)[0].tolist()
        return reduced
    except Exception as e:
        print(f"Error in dimension reduction: {e}")
        # Fallback: simple truncation
        return embedding[:target_dim]

def embed_text(text: str):
    """Generate embeddings for the input text"""
    try:
        response = client.embeddings.create(
            model="BAAI/bge-multilingual-gemma2",
            input=text
        )
        embedding = response.data[0].embedding
        
        # Check if the dimension matches our expected dimension
        if len(embedding) != EMBEDDING_DIMENSION:
            print(f"Warning: API returned embedding with dimension {len(embedding)}, but we expected {EMBEDDING_DIMENSION}")
            # Perform dimension reduction to match our expected dimension
            embedding = dimension_reduction(embedding)
            print(f"Reduced embedding dimension to {len(embedding)}")
            
        return embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return a mock embedding for development purposes
        # return mock_embed_text(text)
        return dimension_reduction([0] * EMBEDDING_DIMENSION)

# def mock_embed_text(text: str):
#     """Generate a mock embedding for development purposes"""
#     print("Using mock embeddings since API call failed")
#     # Create a deterministic vector based on the hash of the text
#     np.random.seed(hash(text) % 2**32)
#     # Use the consistent dimension
#     return np.random.uniform(-1, 1, EMBEDDING_DIMENSION).tolist()

def store_blog_memory(user_id: str, title: str, content: str):
    """Store a blog post in the vector database"""
    embedding = embed_text(content)
    try:
        result = supabase.table("blog_memory").insert({
            "user_id": user_id,
            "title": title,
            "content": content,
            "embedding": embedding
        }).execute()
        return result.data
    except Exception as e:
        print(f"Error storing blog: {e}")
        return {"error": str(e)}

def retrieve_user_blogs(user_id: str):
    """Retrieve all blog entries for a specific user from the database"""
    try:
        response = supabase.table("blog_memory").select("title, content").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving blogs: {e}")
        return []


def search_similar_blogs(user_id: str, input_text: str, top_k: int = 5):
    """Search for similar blogs using vector similarity"""
    try:
        query_embedding = embed_text(input_text)
        result = supabase.rpc("match_blogs", {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "user_id": user_id
        }).execute()
        return result.data
    except Exception as e:
        print(f"Error searching for similar blogs: {e}")
        # Fall back to returning most recent blogs if vector search fails
        try:
            response = supabase.table("blog_memory") \
                .select("title, content") \
                .eq("user_id", user_id) \
                .order("created_at", desc=True) \
                .limit(top_k) \
                .execute()
            return response.data
        except Exception as fallback_error:
            print(f"Fallback retrieval also failed: {fallback_error}")
            return []
