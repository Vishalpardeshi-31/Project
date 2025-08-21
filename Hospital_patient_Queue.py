import heapq
from collections import deque


# Data Structures

priority_queue = []   # emergency patients -> (priority, patient_name)
regular_queue = deque()  # normal patients -> patient_name

SERVICE_TIME = 15  # minutes per patient


# Core Functions

def add_patient():
    name = input("Enter patient name: ")
    patient_type = input("Is it emergency? (y/n): ").lower()

    if patient_type == 'y':
        severity = int(input("Enter severity (1=critical, 5=less severe): "))
        heapq.heappush(priority_queue, (severity, name))
        print(f"Emergency patient {name} added with severity {severity}.")
    else:
        regular_queue.append(name)
        print(f"Regular patient {name} added to queue.")


def view_queues():
    print("\n--- Emergency Patients ---")
    if priority_queue:
        for s, n in sorted(priority_queue):
            print(f"{n} (Severity {s})")
    else:
        print("No emergency patients.")

    print("\n--- Regular Patients ---")
    if regular_queue:
        for n in regular_queue:
            print(n)
    else:
        print("No regular patients.")


def next_patient():
    if priority_queue:
        severity, name = heapq.heappop(priority_queue)
        print(f"Next patient (Emergency): {name} (Severity {severity})")
    elif regular_queue:
        name = regular_queue.popleft()
        print(f"Next patient (Regular): {name}")
    else:
        print("No patients in queue.")


def estimated_wait_time(name):
    # Check emergency patients first
    emergency_list = sorted(priority_queue)
    for i, (s, n) in enumerate(emergency_list):
        if n == name:
            return i * SERVICE_TIME

    # Then check regular patients
    for i, n in enumerate(regular_queue):
        if n == name:
            wait_before = len(priority_queue) * SERVICE_TIME  # all emergencies first
            return wait_before + i * SERVICE_TIME

    return None


def check_wait_time():
    name = input("Enter patient name: ")
    wait = estimated_wait_time(name)
    if wait is not None:
        print(f"Estimated wait time for {name}: {wait} minutes")
    else:
        print("Patient not found in queue.")


# Main Menu


def main():
    while True:
        print("\n==== Hospital Patient Queue ====")
        print("1. Add Patient")
        print("2. View Queues")
        print("3. Call Next Patient")
        print("4. Check Patient Wait Time")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_queues()
        elif choice == "3":
            next_patient()
        elif choice == "4":
            check_wait_time()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
