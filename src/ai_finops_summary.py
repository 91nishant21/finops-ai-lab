import csv
import os
from openai import OpenAI

summary_file = "data/finops_summary.csv"
candidates_file = "data/optimization_candidates.csv"
text_output_file = "docs/ai_finops_summary.txt"
csv_output_file = "data/ai_finops_summary.csv"

# Read summary data
with open(summary_file, mode="r") as sfile:
    reader = csv.DictReader(sfile)
    summary = next(reader)

total_vms = summary["total_vms"]
optimization_candidates = summary["optimization_candidates"]
estimated_savings = summary["estimated_total_monthly_savings"]
savings_opportunity = summary["savings_opportunity_pct"]
total_monthly_cost = summary["total_monthly_cost"]

# Read optimization candidates
candidate_rows = []
candidate_names = []

with open(candidates_file, mode="r") as cfile:
    reader = csv.DictReader(cfile)
    for row in reader:
        candidate_names.append(row["vm_name"])
        candidate_rows.append(
            f"{row['vm_name']} | {row['subscription']} | {row['region']} | "
            f"{row['vm_size']} | cost ${row['monthly_cost']} | savings ${row['estimated_monthly_savings']}"
        )

candidate_text = "\n".join(candidate_rows)
top_candidates = ", ".join(candidate_names[:3])

# Default fallback summary
fallback_report = f"""
Executive Summary

The environment contains {total_vms} virtual machines.
A total of {optimization_candidates} VMs have been identified as optimization candidates.
Estimated monthly savings are ${estimated_savings}, representing a savings opportunity of {savings_opportunity}% of the total monthly cost (${total_monthly_cost}).

Recommendations
- Review and resize underutilized VMs such as {top_candidates}
- Validate sizing policies across subscriptions to reduce overprovisioning
- Implement periodic utilization monitoring to track optimization opportunities
""".strip()

report = fallback_report
generation_mode = "Fallback"

# Try OpenAI first
try:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a FinOps analyst. Write a short executive summary in simple professional language.

Environment Data:
Total VMs: {total_vms}
Optimization Candidates: {optimization_candidates}
Total Monthly Cost: ${total_monthly_cost}
Estimated Monthly Savings: ${estimated_savings}
Savings Opportunity: {savings_opportunity}%

Optimization candidates:
{candidate_text}

Write:
1. A short executive summary paragraph
2. 3 bullet point optimization recommendations
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    report = response.output_text.strip()
    generation_mode = "OpenAI"

except Exception as e:
    print("OpenAI generation failed. Using fallback summary instead.")
    print(f"Reason: {e}")

# Save TXT output
with open(text_output_file, mode="w", encoding="utf-8") as outfile:
    outfile.write(report)

# Save CSV output for Power BI
lines = [line.strip() for line in report.splitlines() if line.strip()]

with open(csv_output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["section", "content"])

    current_section = "AI Summary"
    for line in lines:
        if line.lower().startswith("recommendations"):
            current_section = "Recommendation Header"
            writer.writerow([current_section, line])
        elif line.startswith("-") or line.startswith("•"):
            writer.writerow(["Recommendation", line.lstrip("-• ").strip()])
        elif line.lower().startswith("executive summary"):
            writer.writerow(["Summary Header", line])
        else:
            writer.writerow(["AI Summary", line])

print(f"Summary generation mode: {generation_mode}")
print(f"Text output: {text_output_file}")
print(f"CSV output: {csv_output_file}")