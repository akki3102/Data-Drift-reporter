# AI Usage Note — Data Drift Reporter

## What AI Helped With

### 1. Narration Generation (narrator.py)
- Used Claude (Anthropic) API to convert structured drift metrics
  (row count change %, null rate change %, mean shift %) into
  business-friendly plain English summaries.
- AI produced analyst-style reports with specific numbers and
  recommendations — e.g. "Average order value dropped 12% on 5 Nov,
  suggesting reduced purchasing activity or a data pipeline issue."

### 2. Offline Rule-Based Fallback
- AI was used to design the template structure for the offline fallback
  so it mirrors the same output format as the LLM version.
- This means the app produces consistent output whether or not an API
  key is available.

### 3. Drift Event Detection
- AI helped design the logic for identifying which column-level changes
  are "narration-worthy" (e.g. null rate jump ≥ 1%, mean shift ≥ 5%)
  vs. noise.

### 4. Code Assistance
- AI assisted in writing boilerplate Flask routes, SQLAlchemy model
  definitions, and Pandas statistical computation functions.
- AI suggested the JSON blob approach for storing per-column stats in
  the snapshots table, enabling flexible future comparisons.

---

## What AI Got Wrong

### 1. Version-Specific Errors
- AI suggested some library versions (e.g. pandas==2.2.2) that required
  C build tools on Windows — had to fall back to installing without
  version pins on some machines.

### 2. Over-Complicated Solutions
- AI initially suggested using Redis for caching snapshot comparisons —
  this was overkill for a prototype. Simplified to direct SQLite queries.

### 3. Verbose Narratives
- Without explicit length constraints in the prompt, the LLM sometimes
  produced 8-10 sentence reports instead of the requested 3-5 sentences.
  Fixed by adding "Write 3-5 short sentences" to the prompt.

### 4. Hallucinated Column Names
- In early testing, when column names weren't explicitly included in the
  prompt, the LLM sometimes invented column names. Fixed by always
  passing exact column names and values in the prompt context.

---

## Best Prompts Used

### Most Effective Prompt Pattern:
```
You are a senior business data analyst. Write a concise, professional
data quality report for '{dataset_name}'. Drift level: {level}.
Key observations: {bullet list of specific changes with numbers}.
Write 3-5 sentences in plain business language. End with one
recommendation sentence.
```

### Why It Worked:
- Role assignment ("senior business data analyst") set the tone
- Specific numbers in the context prevented vague outputs
- Explicit sentence count kept responses concise
- "Plain business language" prevented technical jargon

---

## Tools Used for AI Integration

| Tool | Purpose | Free/Paid |
|---|---|---|
| Anthropic Claude API | LLM narration generation | Paid (optional) |
| Rule-based template | Offline fallback narration | Free / No API needed |

> Note: The app is fully functional without any API key. The AI narration
> is an enhancement, not a requirement. The rule-based fallback produces
> output in the same format and style.

---

## AI Capability Demonstrated

- **LLM Structured Output**: Drift metrics passed as structured JSON context;
  LLM returns a fixed-format business narrative with Result, Reasoning,
  and Recommended Action.
- **Agent Loop**: read CSV → compute stats → compare snapshots → call LLM
  → validate output → save to DB → display on dashboard.
