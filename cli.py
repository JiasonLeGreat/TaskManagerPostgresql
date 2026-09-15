import sys
import requests

API_URL = "http://localhost:8000/tasks"

def display_menu():
    print(" 1. 📋 List All Tasks")
    print(" 2. ➕ Add a Task")
    print(" 3. 🔄 Update a Task")
    print(" 4. ❌ Remove a Task")
    print(" 5. 🚪 Exit")
    print("═"*40)

def list_tasks() -> bool:
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"\n[!] Error fetching tasks: {response.text}")
            return False
        
        tasks = response.json()
        if not tasks:
            print("\n[!] No tasks found in the database.")
            return False
        
        print("\nID   | Status | Title & Description")
        print("-" * 55)
        for task in tasks:
            status = "✅ Done" if task["completed"] else "⏳ Pending"
            desc_str = f" - {task['description']}" if task["description"] else ""
            print(f"{task['id']:<4} | {status:<6} | {task['title']}{desc_str}")
        return True
    except requests.exceptions.ConnectionError:
        print("\n[!] Error: Cannot connect to FastAPI server. Is it running?")
        return False

def add_task() -> None:
    title = input("\nEnter task title: ").strip()
    if not title:
        print("Error: Task title cannot be empty.")
        return
    description = input("Enter task description (optional): ").strip()
    
    payload = {"title": title, "description": description if description else None}
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 201:
        print(f"\n Task '{title}' added successfully via API!")
    else:
        print(f"\n[!] Failed to add task: {response.text}")

def update_task() -> None:
    if not list_tasks():
        return
    try:
        task_id = int(input("\nEnter the ID of the task to update: "))
    except ValueError:
        print("Error: Invalid numeric ID.")
        return

    print(f"\nEditing Task #{task_id}")
    new_title = input("New title (leave blank to keep current): ").strip()
    new_desc = input("New description (leave blank to keep current): ").strip()
    status_toggle = input("Mark as completed? (y/n or blank to keep current): ").strip().lower()

    payload = {}
    if new_title:
        payload["title"] = new_title
    if new_desc:
        payload["description"] = new_desc
    if status_toggle in ['y', 'n']:
        payload["completed"] = (status_toggle == 'y')

    response = requests.put(f"{API_URL}/{task_id}", json=payload)
    if response.status_code == 200:
        print("✨ Task updated successfully via API!")
    elif response.status_code == 404:
        print("Error: Task ID not found.")
    else:
        print(f"Error: {response.text}")

def remove_task() -> None:
    if not list_tasks():
        return
    try:
        task_id = int(input("\nEnter the ID of the task to remove: "))
    except ValueError:
        print("Error: Invalid numeric ID.")
        return

    response = requests.delete(f"{API_URL}/{task_id}")
    if response.status_code == 204:
        print(f"🗑️ Task #{task_id} successfully deleted via API.")
    elif response.status_code == 404:
        print("Error: Task ID not found.")
    else:
        print(f"Error: {response.text}")

def main():
    count = 0
    while True:
        if count == 0:
            display_menu()
            count += 1
        else:
            print("\n" + "═"*40)
            print("   Welcome to your Taskmanager!")
            print("═"*40)
            display_menu()
            choice = input("Select an option (1-5): ").strip()
            if choice == "1":
                list_tasks()
            elif choice == "2":
                add_task()
            elif choice == "3":
                update_task()
            elif choice == "4":
                remove_task()
            elif choice == "5":
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("\nInvalid selection. Choose a number between 1 and 5.")

if __name__ == "__main__":
    main()
