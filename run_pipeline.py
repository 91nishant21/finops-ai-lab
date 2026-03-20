import subprocess

print("Step 1: Analyzing VM cost data...")
subprocess.run(["python", "src/analyze_cost.py"])

print("\nStep 2: Generating AI summary...")
subprocess.run(["python", "src/ai_finops_summary.py"])

print("\nStep 3: Running FinOps Agent (Decision Engine)...")
subprocess.run(["python", "src/finops_agent.py"])

print("\nPipeline executed successfully.")

