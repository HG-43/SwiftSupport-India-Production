import time
import json
import os
import ollama

# Import your custom standalone modules
import input_guardrail
import knowledge_rag
import domain_tools
import output_verifier
import telemetry_router

# Define the Tool Manifest so Llama knows it has structural actions available
tools_manifest = [
    {
        'type': 'function',
        'function': {
            'name': 'calculate_restocking_fee',
            'description': 'Calculates the 15% restocking fee if a return product box is damaged or missing.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'item_price': {'type': 'number', 'description': 'The original retail price of the item.'},
                    'is_box_damaged': {'type': 'boolean', 'description': 'True if the packaging box is missing or damaged.'}
                },
                'required': ['item_price', 'is_box_damaged']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'evaluate_shipping_carrier',
            'description': 'Determines whether a shipment routes via DHL Express or FedEx based on destination country.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'destination_country': {'type': 'string', 'description': 'The destination country name.'}
                },
                'required': ['destination_country']
            }
        }
    }
]

print("========================================================================")
print("🌟 ACME OMNISCIENT: DEPLOYING DOMAIN-FOCUSED ENTERPRISE APPARATUS")
print("========================================================================")
print("🛡️  Perimeter Firewall: ACTIVE")
print("🗄️  RAG Knowledge Matrix: SYNCED")
print("⚙️  Logistics Toolbelt: CONNECTED")
print("🔍 Output Auditor Node: ACTIVE")
print("ℹ️  Type 'exit' or 'quit' to shutdown the runtime environment.\n")

while True:
    user_query = input("👤 User: ").strip()
    if user_query.lower() in ['exit', 'quit']:
        print("\n👋 Deactivating system cores. Telemetry storage committed. Goodbye!")
        break
    if not user_query:
        continue
        
    turn_start_time = time.time()
    pipeline_status = "SUCCESS"
    final_display_text = ""
    estimated_tokens = 0
    
    print("\n--- 🔄 INBOUND TRANSACTION INITIALIZED ---")
    
    # ------------------------------------------------------------------
    # STAGE 1: FRONT-DOOR SECURITY FILTER (INPUT GUARDRAIL)
    # ------------------------------------------------------------------
    guard_result = input_guardrail.scan_inbound_prompt(user_query)
    
    if guard_result.get("status") == "BLOCKED":
        print("🚨 [PERIMETER ALERT] Malicious prompt signature isolated! Dropping payload.")
        final_display_text = f"Security Exception: Request Rejected. Reason: {guard_result.get('reason')}"
        pipeline_status = "THREAT_BLOCKED"
        estimated_tokens = len(final_display_text) / 4
        
        # Log telemetry and skip to next turn immediately
        latency = time.time() - turn_start_time
        telemetry_router.commit_telemetry_trace(latency, estimated_tokens, pipeline_status)
        print(f"\n🤖 Agent: {final_display_text}\n" + "="*72 + "\n")
        continue

    print("🟢 [SECURITY PASS] Prompt cleared perimeter network vetting.")
    
    # ------------------------------------------------------------------
    # STAGE 2: LIVE KNOWLEDGE EXTRACTION (LOCAL RAG)
    # ------------------------------------------------------------------
    ground_truth_context = knowledge_rag.retrieve_domain_context(user_query)
    
    # PERFORMANCE PROTECTION GATE: If the security check already took too long,
    # or you want to simulate a rapid failover, trigger the cloud proxy.
    guard_latency = time.time() - turn_start_time
    if guard_latency > 120.0:  # SLA threshold: 15 seconds
        final_display_text = telemetry_router.simulate_cloud_failover(user_query)
        pipeline_status = "CLOUD_FAILOVER"
        estimated_tokens = len(final_display_text) / 4
        latency = time.time() - turn_start_time
        telemetry_router.commit_telemetry_trace(latency, estimated_tokens, pipeline_status)
        print(f"\n🤖 Agent: {final_display_text}\n" + "="*72 + "\n")
        continue

    # ------------------------------------------------------------------
    # STAGE 3: EXECUTION & GENERATION LAYER (AGENT + TOOLS)
    # ------------------------------------------------------------------
    print("🧠 [Agent Core] Processing query context arrays...")
    
    system_instruction = f"""
    You are the elite ACME Logistics Assistant chatbot. You solve customer problems using your tools and the provided data.
    
    CURRENT DOMAIN KNOWLEDGE BASE RULES:
    {ground_truth_context}
    
    INSTRUCTIONS:
    - If the user asks about restocking fees or shipping destinations, call the matching tool immediately.
    - If the tool outputs an answer, synthesize that exact number/string into your final sentence.
    """
    
    # Invoke the model with tools enabled
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': user_query}
        ],
        tools=tools_manifest
    )
    
    assistant_msg = response['message']
    
    # Check if the agent decided to execute a system tool
    if assistant_msg.get('tool_calls'):
        print("🎯 [Tool Router] Agent requested programmatic system execution.")
        for call in assistant_msg['tool_calls']:
            func_name = call['function']['name']
            args = call['function']['arguments']
            
            if func_name == 'calculate_restocking_fee':
                # Force defensive typing variables
                price = float(args.get('item_price', 0))
                damaged = bool(args.get('is_box_damaged', False))
                tool_output = domain_tools.calculate_restocking_fee(price, damaged)
                tool_feedback = f"Calculation Result: The 15% restocking fee for this item is ${tool_output} USD."
                
            elif func_name == 'evaluate_shipping_carrier':
                country = str(args.get('destination_country', ''))
                tool_output = domain_tools.evaluate_shipping_carrier(country)
                tool_feedback = f"Logistics Mapping: Shipments to this region route exclusively via {tool_output}."
            else:
                tool_feedback = "Error: Requested tool execution pathway not found."
                
            print(f"   ⚙️  Running Tool [{func_name}] -> Captured: '{tool_feedback}'")
            
            # Feed tool results back into the loop for final phrasing
            final_pass = ollama.chat(
                model='llama3.2',
                messages=[
                    {'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': user_query},
                    assistant_msg,
                    {'role': 'tool', 'content': tool_feedback}
                ]
            )
            raw_generation = final_pass['message']['content']
    else:
        # No tools needed; standard contextual sentence construction
        raw_generation = assistant_msg['content']

    # ------------------------------------------------------------------
    # STAGE 4: BACK-DOOR COMPLIANCE GATE (OUTPUT AUDITOR)
    # ------------------------------------------------------------------
    audit_check = output_verifier.inspect_generated_response(ground_truth_context, raw_generation)
    
    if audit_check.get("verdict") == "HALLUCINATION_DETECTED":
        print("🚨 [QA ALERT] Hallucination or policy fabrication intercepted! Quarantining response.")
        final_display_text = "Operational Notice: The generated response failed corporate factual compliance checks. Retrying transaction query parameters."
        pipeline_status = "COMPLIANCE_REJECTED"
    else:
        print("🔍 [QA PASS] Generation verified as factually aligned with domain manual.")
        final_display_text = raw_generation

    # ------------------------------------------------------------------
    # STAGE 5: SYSTEM TELEMETRY LOGGER
    # ------------------------------------------------------------------
    estimated_tokens = len(final_display_text) / 4
    total_turnaround_latency = time.time() - turn_start_time
    
    telemetry_router.commit_telemetry_trace(total_turnaround_latency, estimated_tokens, pipeline_status)
    
    print(f"\n🤖 Agent: {final_display_text}")
    print("="*72 + "\n")