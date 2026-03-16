


# AI FinOps Lab

A hands-on personal lab project combining Python, Power BI, GitHub, and OpenAI for FinOps-style cloud cost analysis.

## Architecture

VM Cost Data (CSV)
        ↓
Python Analysis Engine
        ↓
Optimization Candidates + FinOps Summary
        ↓
Power BI Dashboard
        ↓
OpenAI Executive Summary

## Features
- Reads VM cost and utilization data
- Identifies low-utilization VMs
- Estimates monthly savings opportunities
- Generates summary datasets for reporting
- Builds a Power BI dashboard
- Uses OpenAI to generate an executive FinOps summary

## Project Structure
- `data/` → source and output CSV files
- `src/` → Python scripts
- `docs/` → generated summaries
- `powerbi/` → dashboard file
- `terraform/` → reserved for infra-as-code work

## Current Workflow
1. Run `python src/analyze_cost.py`
2. Refresh Power BI dashboard
3. Run `python src/ai_finops_summary.py`

## Outputs
- Optimization candidate dataset
- FinOps summary dataset
- Power BI dashboard
- AI-generated executive summary

## Tech Stack
- Python
- Power BI
- OpenAI API
- GitHub
- Terraform