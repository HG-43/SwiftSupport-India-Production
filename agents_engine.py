import base64
import json
from openai import OpenAI
import knowledge_rag

TEXT_MODEL = "meta-llama/llama-3.3-70b-instruct"
VISION_MODEL = "meta-llama/llama-3.2-11b-vision-instruct"

def get_client(api_key):
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def process_agent_workflow(api_key, user_query, uploaded_image_file=None):
    client = get_client(api_key)
    
    # TRACK 1: VISUAL EVIDENCE ASSESSMENT
    if uploaded_image_file is not None:
        base64_image = base64.b64encode(uploaded_image_file.read()).decode('utf-8')
        mime = uploaded_image_file.type
        
        vision_prompt = (
            "You are the Visual Triage Agent for SwiftSupport India. "
            "Analyze the image provided and discuss any packaging or product damage with the user "
            "in a professional and conversational manner."
        )
        
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": vision_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"User query: {user_query}"},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64_image}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content

    # TRACK 2: STRUCTURED AUTO-ROUTING (JSON MODE)
    router_prompt = (
        "Classify user intent into this exact JSON schema: {\"agent\": \"LOGISTICS\" or \"FINANCE\"}.\n"
        "Logistics = courier tracking, shipping timelines, transit delays, package states.\n"
        "Finance = refunds, costs, calculations, processing/restocking fees."
    )
    
    try:
        route_response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "system", "content": router_prompt}, {"role": "user", "content": user_query}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        route_decision = json.loads(route_response.choices[0].message.content).get("agent", "LOGISTICS").upper()
    except Exception:
        route_decision = "LOGISTICS"

    # Fetch semantic policy context from ChromaDB
    semantic_context = knowledge_rag.retrieve_domain_context(user_query)

    if "FINANCE" in route_decision:
        agent_system = (
            "You are the Finance Agent for SwiftSupport India. Be conversational, polite, and brief (max 3 sentences). "
            "Help the user address their monetary or refund question naturally using this policy manual context:\n"
            f"{semantic_context}\n\n"
            "CRITICAL RULE: Do NOT automatically bring up a late 30-day return window penalty unless the user explicitly "
            "states they are trying to return an old item."
        )
        agent_label = "💰 Finance Agent"
    else:
        agent_system = (
            "You are the Logistics Agent for SwiftSupport India. Be conversational, polite, and brief (max 3 sentences). "
            "Help the user address their shipment delivery tracking status or transit delays naturally using this context:\n"
            f"{semantic_context}\n\n"
            "CRITICAL RULE: If the user says 'it is late' or 'delayed', assume they are asking about an active shipping arrival transit hold, "
            "not a product return timeframe rule."
        )
        agent_label = "🚚 Logistics Agent"

    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "system", "content": agent_system}, {"role": "user", "content": user_query}],
        temperature=0.5
    )
    
    return f"**[{agent_label}]**\n\n{response.choices[0].message.content}"