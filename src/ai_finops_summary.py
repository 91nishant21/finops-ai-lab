import csv
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

prompt = f"""
You are a FinOps cloud cost optimization expert.

Create a short executive summary for leadership based on this data:

Total VMs: {total_vms}
Optimization Candidates: {optimization_candidates}
Estimated Monthly Savings: ${estimated_savings}
Savings Opportunity: {savings_opportunity}%
Top candidate VMs: {top_candidates}

Keep it concise and professional.
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

summary_text = response.output[0].content[0].text

with open(output_file, "w") as outfile:
    outfile.write(summary_text)

print("AI FinOps summary generated.")