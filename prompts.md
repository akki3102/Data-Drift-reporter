# Prompts Used in Data Drift Reporter

This file documents all prompts used in the AI narration module (`narrator.py`).

---

## 1. Main Drift Narration Prompt

Used in `narrator.py` → `_generate_with_llm()` function.

```
You are a senior business data analyst. Write a concise, professional
data quality / drift report for the dataset '{dataset_name}'.

Drift level: {drift_level} (score: {drift_score})
Row count change: {row_count_change_pct}%
Overall null rate change: {null_rate_change_pct}%
Overall mean change: {mean_change_pct}%

Key observations:
- {event_1}
- {event_2}
- {event_3}

Write 3-5 short sentences in plain business language, like an analyst
summarizing this week's data health to a non-technical stakeholder.
Mention specific numbers. End with a one-sentence recommendation if
drift is Medium or High.
```

### Example Input:
```
Dataset: Orders Dataset
Drift level: High (score: 21.5)
Row count change: 15.0%
Overall null rate change: 23.53%
Overall mean change: 18.3%

Key observations:
- Row count decreased from 20 to 17 (15.0% change).
- 'customer_email' null rate increased from 0.00% to 29.41%.
- Average 'order_amount' decreased by 18.3% (from 154.62 to 126.18).
```

### Example Output:
```
Data Quality Report for 'Orders Dataset': overall drift level is High
(drift score: 21.5%). Row count decreased by 15.0%, now totaling 17
records. The customer_email null rate jumped from 0% to 29.4%,
indicating a CRM integration failure. Average order amount dropped
18.3% from $154.62 to $126.18.
Recommendation: Investigate the upstream data pipeline immediately —
the combination of missing emails and revenue drop suggests a data
extraction error, not a genuine business decline.
```

---

## 2. Basic Prompt Template (Guideline Format)

```
You are an AI assistant helping build a prototype for Data Drift Reporter.

Input data:
<PASTE DRIFT METRICS SUMMARY>

Task:
1. Analyze the drift metrics.
2. Produce a business-friendly summary in structured format.
3. Give a short explanation of what changed.
4. Mention assumptions and limitations.

Return output in this format:
- Result: (Low / Medium / High drift with score)
- Reasoning: (what drove the drift score)
- Recommended Action: (what the data team should do)
- Output Markdown Table: (key metrics comparison)
```

---

## 3. Offline Rule-Based Fallback Template

Used in `narrator.py` → `_generate_with_template()` when no API key is set.

```
Data Quality Report for '{dataset_name}': overall drift level is
{level} (drift score: {score:.1f}%).

Row count changed by {rc_change:.1f}%, now totaling {row_count} records.
The overall null rate shifted by {null_change:.1f}%, now sitting at
{null_rate:.2f}% of all values.
Average values across numeric fields shifted by {mean_change:.1f}%
week-over-week.

Key observations:
  • {event_1}
  • {event_2}
  • {event_3}

Recommendation: {recommendation based on drift level}
```

---

## What Worked Well
- Asking the LLM to act as a "senior business analyst" produced more
  professional and non-technical language.
- Including specific numbers (percentages, before/after values) in the
  prompt ensured the output was factual and grounded.
- Asking for a single recommendation sentence at the end made the output
  actionable.

## What the AI Got Wrong
- Occasionally the LLM added extra caveats or disclaimers not needed for
  a business report — had to prompt it to "be concise".
- Without explicit instruction to mention specific numbers, it sometimes
  produced vague summaries like "values changed significantly".

## Best Prompt Tip
Always include before/after values in the prompt, not just percentage
changes. "order_amount dropped 18.3% (from $154.62 to $126.18)" produces
a much better narrative than "order_amount dropped 18.3%".
