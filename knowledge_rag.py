import os

def retrieve_domain_context(user_query: str) -> str:
    """
    Simulates a high-performance RAG context extractor. Scans the local policy 
    manifest file to isolate paragraphs matching key terms in the query.
    """
    policy_path = "core_policy.txt"
    
    if not os.path.exists(policy_path):
        return "Error: Domain knowledge base manual ('core_policy.txt') is missing."
        
    with open(policy_path, "r", encoding="utf-8") as f:
        policy_lines = f.readlines()
        
    # Split keywords to locate semantic overlap loops
    keywords = [word.lower().strip(",?.!") for word in user_query.split() if len(word) > 3]
    relevant_chunks = []
    
    for line in policy_lines:
        # Match keywords against lines in our core domain policy file
        if any(keyword in line.lower() for keyword in keywords):
            relevant_chunks.append(line.strip())
            
    if relevant_chunks:
        print("   🗄️  [RAG Activation] Found relevant domain rules inside manual.")
        return "\n".join(relevant_chunks)
    
    # Clean baseline default fallback if query words don't map explicitly
    return "Standard corporate guidelines apply. Reference the core policy file for details."

# Quick verification test
if __name__ == "__main__":
    test_search = "What is the return window for a VIP member?"
    print(f"Testing retrieval for: '{test_search}'")
    context = retrieve_domain_context(test_search)
    print(f"Retrieved Context:\n{context}")