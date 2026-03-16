import csv

summary_file = "data/finops_summary.csv"
candidates_file = "data/optimization_candidates.csv"
output_file = "docs/ai_finops_summary.txt"

with open(summary_file, mode="r") as sfile:
    reader = csv.DictReader(sfile)
    summary = next(reader)

total_vms = summary["total_vms"]
optimization_candidates = summary["optimization_candidates"]
estimated_savings = summary["estimated_total_monthly_savings"]
savings_opportunity = summary["savings_opportunity_pct"]

candidate_names = []

with open(candidates_file, mode="r") as cfile:
    reader = csv.DictReader(cfile)
    for row in reader:
        candidate_names.append(row["vm_name"])

top_candidates = ", ".join(candidate_names[:3])

report = f"""
FinOps Executive Summary
------------------------
The environment contains {total_vms} VMs.
A total of {optimization_candidates} VMs are identified as optimization candidates.
Estimated monthly savings are ${estimated_savings}.
This represents a savings opportunity of {savings_opportunity}%.
Top optimization candidates include: {top_candidates}.
"""

with open(output_file, mode="w") as outfile:
    outfile.write(report.strip())

print("AI-style summary generated successfully.")
print(f"Output file created: {output_file}")