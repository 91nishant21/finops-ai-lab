import csv

input_file = "data/vm_cost_data.csv"
output_file = "data/optimization_candidates.csv"
summary_file = "data/finops_summary.csv"

print("Reading VM cost data...\n")

total_savings = 0
candidate_count = 0
total_vms = 0

with open(input_file, mode="r") as infile, open(output_file, mode="w", newline="") as outfile:
    reader = csv.DictReader(infile)

    fieldnames = reader.fieldnames + ["estimated_monthly_savings"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    print("Oversized VM candidates (CPU < 20%):\n")

    for row in reader:
        total_vms += 1

        cpu = float(row["cpu_avg_percent"])
        monthly_cost = float(row["monthly_cost"])

        if cpu < 20:
            candidate_count += 1

            estimated_savings = round(monthly_cost * 0.30, 2)
            total_savings += estimated_savings

            row["estimated_monthly_savings"] = estimated_savings
            writer.writerow(row)

            print(
                f"VM Name: {row['vm_name']} | "
                f"CPU Avg: {cpu}% | "
                f"Monthly Cost: ${monthly_cost} | "
                f"Estimated Savings: ${estimated_savings}"
            )

with open(summary_file, mode="w", newline="") as sfile:
    fieldnames = ["total_vms", "optimization_candidates", "estimated_total_monthly_savings"]
    writer = csv.DictWriter(sfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({
        "total_vms": total_vms,
        "optimization_candidates": candidate_count,
        "estimated_total_monthly_savings": round(total_savings, 2)
    })

print("\n----------------------------------")
print(f"Total VMs: {total_vms}")
print(f"Total Optimization Candidates: {candidate_count}")
print(f"Estimated Monthly Savings: ${round(total_savings, 2)}")
print("----------------------------------")

print("\nOptimization file created:", output_file)
print("Summary file created:", summary_file)