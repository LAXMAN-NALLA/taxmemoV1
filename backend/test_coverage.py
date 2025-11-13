import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# --- CONFIGURATION ---

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = "netherlands_pilot"

# --- Queries to test your AI's brain ---

test_queries = [

    # Test 1: For the "Tech" user

    "What are the WBSO R&D tax credit rates for 2025?",

    # Test 2: For the "Hiring" user

    "What are the GDPR (AVG) requirements for small businesses?",

    # Test 3: For the "Holding Co" user

    "Explain the participation exemption (deelningsvrijstelling) for holding companies.",

    # Test 4: For the "Baseline" user

    "What is the difference between a BV and NV legal structure?",

    # Test 5: For the "Baseline" user

    "What are the current 2025 Corporate Income Tax (VPB) rates?"

]

def run_gap_analysis():

    print("Starting Gap Analysis Test Coverage...")

    print("================================================================================")

    

    try:

        print("Initializing embeddings...")

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        

        print("Connecting to Qdrant...")

        if QDRANT_API_KEY:
            client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            client = QdrantClient(url=QDRANT_URL)

        

        qdrant = QdrantVectorStore(

            client=client,

            collection_name=COLLECTION_NAME,

            embedding=embeddings,

        )

        print(f"Connected to Qdrant collection: {COLLECTION_NAME}\n")

        for i, query in enumerate(test_queries, 1):

            print("================================================================================")

            print(f"TEST {i}/{len(test_queries)}")

            print("================================================================================")

            print(f"Query: {query}")

            print("--------------------------------------------------------------------------------")

            try:

                # Perform the search

                results = qdrant.similarity_search_with_score(query, k=2)

                

                if not results:

                    print("❌ NO RELEVANT DOCUMENTS FOUND.")

                    continue

                for j, (doc, score) in enumerate(results, 1):

                    print(f"Match #{j} (Score: {score:.4f})")

                    if 'source' in doc.metadata:

                         # Updated key to match the new loader's metadata

                        print(f"  Source: {doc.metadata.get('source', 'Unknown')}")

                    else:

                        print("  Source: Unknown (Metadata 'source' key not found)")

                        

                    # Clean the preview text to avoid encoding errors

                    preview = doc.page_content.replace('\n', ' ').strip()[:200]

                    print(f"  Preview: {preview}...")

                    print()

            except Exception as e:

                print(f"ERROR: Error processing query: {e}")

    except Exception as e:

        print(f"FATAL ERROR: Could not connect to Qdrant or initialize embeddings.")

        print(f"Details: {e}")

        return

    print("================================================================================")

    print("Gap Analysis Complete!")

    print("================================================================================")

if __name__ == "__main__":

    # This ensures the script runs when called directly

    run_gap_analysis()
