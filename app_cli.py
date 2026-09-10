import sys
from database import SessionLocal, Task

def display_menu():
    print(" 1. 📋 List All Tasks")
    print(" 2. ➕ Add a Task")
    print(" 3. 🔄 Update a Task")
    print(" 4. ❌ Remove a Task")
    print(" 5. 🚪 Exit")
    print("═"*40)

def list_tasks(db):
    tasks = db.query(Task).order_by(Task.id).all()
    if not tasks:
        print("\n[!] No tasks found in the database.")
        return False
    
    print("\nID   | Status | Title & Description")
    print("-" * 55)
    for task in tasks:
        status = "✅ Done" if task.completed else "⏳ Pending"
        desc_str = f" - {task.description}" if task.description else ""
        print(f"{task.id:<4} | {status:<6} | {task.title}{desc_str}")
    return True

def add_task(db):
    title = input("\nEnter task title: ").strip()
    if not title:
        print("Error: Task title cannot be empty.")
        return
    description = input("Enter task description (optional): ").strip()
    
    new_task = Task(title=title, description=description if description else None)
    db.add(new_task)
    db.commit()
    print(f"\n Task '{title}' added successfully!")

def update_task(db):
    if not list_tasks(db):
        return
    try:
        task_id = int(input("\nEnter the ID of the task to update: "))
    except ValueError:
        print("Error: Invalid numeric ID.")
        return

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        print("Error: Task ID not found.")
        return

    print(f"\nEditing Task #{task.id}: '{task.title}'")
    new_title = input(f"New title [{task.title}]: ").strip()
    new_desc = input(f"New description [{task.description or 'None'}]: ").strip()
    status_toggle = input(f"Mark as completed? (y/n) [{'y' if task.completed else 'n'}]: ").strip().lower()

    if new_title:
        task.title = new_title
    if new_desc:
        task.description = new_desc
    if status_toggle in ['y', 'n']:
        task.completed = (status_toggle == 'y')

    db.commit()
    print("✨ Task updated successfully!")

def remove_task(db):
    if not list_tasks(db):
        return
    try:
        task_id = int(input("\nEnter the ID of the task to remove: "))
    except ValueError:
        print("Error: Invalid numeric ID.")
        return

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        print("Error: Task ID not found.")
        return

    db.delete(task)
    db.commit()
    print(f"🗑️ Task #{task_id} successfully deleted.")

def main():
    db = SessionLocal()
    count = 0
    try:
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
                    list_tasks(db)
                elif choice == "2":
                    add_task(db)
                elif choice == "3":
                    update_task(db)
                elif choice == "4":
                    remove_task(db)
                elif choice == "5":
                    print("\nGoodbye!")
                    break
                else:
                    print("\nInvalid selection. Choose a number between 1 and 5.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
