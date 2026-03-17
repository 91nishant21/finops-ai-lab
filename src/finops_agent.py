import csv

input_file = "data/optimization_candidates.csv"
output_file = "data/agent_recommendations.csv"
top_actions_file = "data/top_actions.csv"

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

def severity_score(severity: str) -> int:
    scores = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }
    return scores.get(severity, 1)

def savings_score(estimated_savings: float) -> int:
    if estimated_savings >= 150:
        return 3
    elif estimated_savings >= 100:
        return 2
    return 1

def recommend_action(vm_size: str, cpu_percent: float):
    severity = classify_severity(cpu_percent)
    target_size = resize_map.get(vm_size, vm_size)
    action = "Resize" if target_size != vm_size else "Review Manually"
    issue = "Low CPU utilization"
    return issue, severity, action, target_size

recommendations = []

with open(input_file, mode="r") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        cpu_percent = float(row["cpu_avg_percent"])
        vm_size = row["vm_size"]
        estimated_savings = float(row["estimated_monthly_savings"])

        issue, severity, action, target_size = recommend_action(vm_size, cpu_percent)

        sev_score = severity_score(severity)
        save_score = savings_score(estimated_savings)
        priority_score = sev_score + save_score

        row["issue"] = issue
        row["severity"] = severity
        row["recommended_action"] = action
        row["recommended_vm_size"] = target_size
        row["severity_score"] = sev_score
        row["savings_score"] = save_score
        row["priority_score"] = priority_score

        recommendations.append(row)

# Sort by priority score, then estimated savings descending
recommendations.sort(
    key=lambda x: (int(x["priority_score"]), float(x["estimated_monthly_savings"])),
    reverse=True
)

# Assign rank
for index, row in enumerate(recommendations, start=1):
    row["rank"] = index

# Write full recommendations
fieldnames = list(recommendations[0].keys()) if recommendations else []

with open(output_file, mode="w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(recommendations)

# Write top 3 actions
with open(top_actions_file, mode="w", newline="") as topfile:
    top_fieldnames = [
        "rank",
        "vm_name",
        "severity",
        "recommended_action",
        "recommended_vm_size",
        "estimated_monthly_savings",
        "priority_score"
    ]
    writer = csv.DictWriter(topfile, fieldnames=top_fieldnames)
    writer.writeheader()

    for row in recommendations[:3]:
        writer.writerow({
            "rank": row["rank"],
            "vm_name": row["vm_name"],
            "severity": row["severity"],
            "recommended_action": row["recommended_action"],
            "recommended_vm_size": row["recommended_vm_size"],
            "estimated_monthly_savings": row["estimated_monthly_savings"],
            "priority_score": row["priority_score"]
        })

print("Agent v2 recommendations generated.\n")

for row in recommendations:
    print(
        f"Rank: {row['rank']} | "
        f"VM: {row['vm_name']} | "
        f"Severity: {row['severity']} | "
        f"Action: {row['recommended_action']} | "
        f"Target: {row['recommended_vm_size']} | "
        f"Savings: ${row['estimated_monthly_savings']} | "
        f"Priority Score: {row['priority_score']}"
    )

print(f"\nFull recommendations file created: {output_file}")
print(f"Top actions file created: {top_actions_file}")