import queue
import threading
import time
import random

# --- Simulated Inter-Cloud Message Bus ---
# These queues represent communication channels between different cloud environments.
# In a real multi-cloud setup, these would be actual message queues (e.g., AWS SQS, Azure Service Bus, GCP Pub/Sub)
# or direct API calls, potentially routed through a central gateway.
aws_to_azure_queue = queue.Queue()
azure_to_gcp_queue = queue.Queue()

# --- Cloud Agent Functions ---

def aws_inventory_service(name="AWS Inventory Service"):
    """
    Simulates an AWS service managing inventory.
    It initiates an order event and sends it to the Azure payment service.
    """
    print(f"[{name}] Starting...")
    for i in range(3):
        order_id = f"ORDER-{random.randint(1000, 9999)}"
        item = f"Item-{random.choice(['A', 'B', 'C'])}"
        print(f"[{name}] Processing inventory for {order_id} ({item})...")
        time.sleep(random.uniform(0.5, 1.5)) # Simulate work

        message = {
            "source_cloud": "AWS",
            "destination_cloud": "Azure",
            "event_type": "ORDER_PLACED",
            "order_id": order_id,
            "item": item,
            "amount": round(random.uniform(10.0, 100.0), 2)
        }
        aws_to_azure_queue.put(message) # Simulate sending message to Azure
        print(f"[{name}] Sent ORDER_PLACED for {order_id} to Azure.")
        time.sleep(random.uniform(1.0, 2.0))
    print(f"[{name}] Finished sending orders.")

def azure_payment_service(name="Azure Payment Service"):
    """
    Simulates an Azure service handling payments.
    It receives order events from AWS, processes payment, and sends confirmation to GCP.
    """
    print(f"[{name}] Starting, waiting for orders from AWS...")
    processed_count = 0
    while processed_count < 3: # Expect 3 messages from AWS
        try:
            message = aws_to_azure_queue.get(timeout=5) # Simulate receiving message from AWS
            processed_count += 1
            print(f"[{name}] Received ORDER_PLACED for {message['order_id']} from AWS.")
            
            # Simulate payment processing
            payment_status = random.choice(["SUCCESS", "FAILED"])
            time.sleep(random.uniform(0.8, 2.0)) # Simulate work
            
            response_message = {
                "source_cloud": "Azure",
                "destination_cloud": "GCP",
                "event_type": "PAYMENT_PROCESSED",
                "order_id": message['order_id'],
                "amount": message['amount'],
                "payment_status": payment_status
            }
            azure_to_gcp_queue.put(response_message) # Simulate sending message to GCP
            print(f"[{name}] Processed payment for {message['order_id']}: {payment_status}. Sent to GCP.")
        except queue.Empty:
            print(f"[{name}] No messages from AWS for a while, exiting.")
            break
    print(f"[{name}] Finished processing payments.")

def gcp_analytics_service(name="GCP Analytics Service"):n    """
    Simulates a GCP service for analytics and logging.
    It receives payment confirmations from Azure and logs them.
    """
    print(f"[{name}] Starting, waiting for payment confirmations from Azure...")
    processed_count = 0
    while processed_count < 3: # Expect 3 messages from Azure
        try:
            message = azure_to_gcp_queue.get(timeout=5) # Simulate receiving message from Azure
            processed_count += 1
            print(f"[{name}] Received PAYMENT_PROCESSED for {message['order_id']} from Azure.")
            
            # Simulate analytics logging
            time.sleep(random.uniform(0.3, 1.0)) # Simulate work
            print(f"[{name}] Logged payment for {message['order_id']}: Status={message['payment_status']}, Amount={message['amount']}.")
        except queue.Empty:
            print(f"[{name}] No messages from Azure for a while, exiting.")
            break
    print(f"[{name}] Finished logging analytics.")

# --- Main Execution ---

def main():
    print("--- Starting Multi-Cloud A2A Communication Simulation ---")

    # Create threads for each cloud agent
    aws_thread = threading.Thread(target=aws_inventory_service)
    azure_thread = threading.Thread(target=azure_payment_service)
    gcp_thread = threading.Thread(target=gcp_analytics_service)

    # Start the threads
    aws_thread.start()
    azure_thread.start()
    gcp_thread.start()

    # Wait for all threads to complete
    aws_thread.join()
    azure_thread.join()
    gcp_thread.join()

    print("--- Multi-Cloud A2A Communication Simulation Finished ---")

if __name__ == "__main__":
    main()
