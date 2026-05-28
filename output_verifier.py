import ollama
import json

def inspect_generated_response(trusted_context: str, generated_answer: str) -> dict:
    """
    Compares the generated answer against trusted context rules. 
    Flags any unverified claims or policy violations instantly.
    """
    auditor_policy = """
    You are a strict, literal Corporate Quality Assurance Auditor. Your task is to verify if a 'GENERATED ANSWER' is fully supported by the 'TRUSTED CONTEXT'.
    
    CRITERIA:
    - If the GENERATED ANSWER states ANY rule, date, pricing, or service option NOT explicitly found in the TRUSTED CONTEXT, return 'HALLUCINATION_DETECTED'.
    - If the text is perfectly safe and factual to the context, return 'PASS'.
    
    Output strictly a single JSON object with exactly two keys:
    - 'verdict': Either 'PASS' or 'HALLUCINATION_DETECTED'
    - 'notes': A brief overview of your inspection.
    
    Only output the raw JSON object. No markdown tags, no conversational filler.
    """
    
    combined_prompt = f"TRUSTED CONTEXT:\n{trusted_context}\n\nGENERATED ANSWER TO INSPECT:\n{generated_answer}"
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': auditor_policy},
                {'role': 'user', 'content': combined_prompt}
            ]
        )
        raw_output = response['message']['content'].strip()
        
        # Clean up any potential string wrapping artifacts
        start_idx = raw_output.find('{')
        end_idx = raw_output.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            raw_output = raw_output[start_idx:end_idx]
            
        return json.loads(raw_output)
    except Exception:
        return {"verdict": "FAIL", "notes": "Output compliance checkpoint failure."}