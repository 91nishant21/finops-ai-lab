import csv

input_file = "data/optimization_candidates.csv"
output_file = "data/agent_recommendations.csv"

# Simple resize map for demo purposes
resize_map = {
    "D16s_v3": "D8s_v3",
    "D8s_v3": "D4s_v3",
    "D4s_v3": "D2s_v3"
}

def classify_severity(cpu_percent: float) -> str:
    if cpu_percent < 10:
        return "High"
    elif cpu_percent < 15:
        return "Medium"
    return "Low"

def recommend_action(vm_size: str, cpu_percent: float):
    severity = classify_severity(cpu_percent)
    target_size = resize_map.get(vm_size, vm_size)
    action = "Resize" if target_size != vm_size else "Review Manually"
    issue = "Low CPU utilization"
    return issue, severity, action, target_size

with open(input_file, mode="r") as infile, open(output_file, mode="w", newline="") as outfile:
    reader = csv.DictReader(infile)

    fieldnames = reader.fieldnames + [
        "issue",
        "severity",
        "recommended_action",
        "recommended_vm_size"
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    print("Generating agent recommendations...\n")

    for row in reader:
        cpu_percent = float(row["cpu_avg_percent"])
        vm_size = row["vm_size"]

        issue, severity, action, target_size = recommend_action(vm_size, cpu_percent)

        row["issue"] = issue
        row["severity"] = severity
        row["recommended_action"] = action
        row["recommended_vm_size"] = target_size

        writer.writerow(row)

        print(
            f"VM: {row['vm_name']} | "
            f"Issue: {issue} | "
            f"Severity: {severity} | "
            f"Action: {action} | "
            f"Target Size: {target_size} | "
            f"Savings: ${row['estimated_monthly_savings']}"
        )

print(f"\nAgent recommendations file created: {output_file}")