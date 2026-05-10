import random
from datetime import datetime, timedelta

EMPLOYEES = [
    "Avery Leaf",
    "Marcus Delgado",
    "Yuna Castellanos",
    "Priya Patel",
]

WORKFLOW_TEMPLATES = [
    "General Employee Onboarding",
    "Product Team Onboarding",
    "IT Provisioning",
]

TASK_STATUSES = [
    "pending",
    "in_progress",
    "completed",
    "blocked",
]

OWNERS = [
    "HR",
    "Manager",
    "Ops",
    "Employee",
]


def generate_task(task_name, day_offset):
    return {
        "task_name": task_name,
        "status": random.choice(TASK_STATUSES),
        "owner": random.choice(OWNERS),
        "days_due_after_start": day_offset,
    }


def generate_workflow(employee_name):
    start_date = datetime.now()

    tasks = [
        generate_task("Complete Direct Deposit Form", 0),
        generate_task("Provision Slack Account", 1),
        generate_task("Setup Google Workspace", 1),
        generate_task("Schedule 1-on-1 With Manager", 7),
        generate_task("Submit 30-Day Goals", 30),
    ]

    return {
        "employee": employee_name,
        "workflow": random.choice(WORKFLOW_TEMPLATES),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "tasks": tasks,
    }


def generate_dataset():
    dataset = []

    for employee in EMPLOYEES:
        dataset.append(generate_workflow(employee))

    return dataset


if __name__ == "__main__":
    workflows = generate_dataset()

    for workflow in workflows:
        print("\n========================")
        print(f"Employee: {workflow['employee']}")
        print(f"Workflow: {workflow['workflow']}")

        for task in workflow["tasks"]:
            print(
                f"- {task['task_name']} "
                f"[{task['status']}] "
                f"(Owner: {task['owner']})"
            )
