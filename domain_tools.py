def calculate_restocking_fee(item_price: float, is_box_damaged: bool) -> float:
    """Calculates the 15% restocking deduction fee if the original product packaging box is damaged or missing."""
    price = float(item_price)
    if is_box_damaged:
        # 15% fee applied based on ACME logistics policy rule 3
        return round(price * 0.15, 2)
    return 0.0

def evaluate_shipping_carrier(destination_country: str) -> str:
    """Determines the exclusive courier routing provider based on global shipping geography."""
    destination = destination_country.strip().lower()
    
    if any(region in destination for region in ["europe", "germany", "france", "italy", "poland"]):
        return "DHL Express (International Hub Router)"
    return "FedEx Home Delivery (Standard Domestic Router)"

# Quick verification matrix test
if __name__ == "__main__":
    print("🔧 Testing restocking calculation tool on a $200 damaged return item...")
    fee = calculate_restocking_fee(200.00, is_box_damaged=True)
    print(f"   Calculated Fee: ${fee}")
    
    print("\n📦 Testing logistics route lookup tool for destination: 'France'...")
    carrier = evaluate_shipping_carrier("France")
    print(f"   Assigned Carrier: {carrier}")