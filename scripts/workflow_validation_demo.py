from synthetic_onboarding_data import generate_dataset


DEPENDENCIES = {
    "Setup Google Workspace": ["Provision Slack Account"],
    "Submit 30-Day Goals": ["Schedule 1-on-1 With Manager"],
}


def build_task_lookup(tasks):
    lookup = {}

    for task in tasks:
        lookup[task["task_name"]] = task["status"]

    return lookup


def validate_dependencies(tasks):
    task_lookup = build_task_lookup(tasks)

    validation_results = []

    for task_name, prerequisites in DEPENDENCIES.items():
        for prerequisite in prerequisites:
            prerequisite_status = task_lookup.get(prerequisite)

            if prerequisite_status != "completed":
                validation_results.append({
                    "task": task_name,
                    "blocked_by": prerequisite,
                    "status": "blocked",
                })

    return validation_results


def run_validation():
    workflows = generate_dataset()

    for workflow in workflows:
        print("\n========================")
        print(f"Validating workflow for: {workflow['employee']}")

        blocked_tasks = validate_dependencies(workflow["tasks"])

        if not blocked_tasks:
            print("No blocked tasks detected.")
            continue

        for blocked in blocked_tasks:
            print(
                f"Task '{blocked['task']}' "
                f"is blocked by '{blocked['blocked_by']}'"
            )


if __name__ == "__main__":
    run_validation()
