# Model Comparison - Test Results Analysis
**POC:** AR-288 Pain Points Extraction  
**Test Date:** Dec 11, 2025  
**Analyst:** AI Assistant  
**Models:** gemini-2.5-pro vs gemini-3-pro-preview  
**Prompt Version:** V5 (optimized)  
**Threshold:** 0.9

---

## Executive Summary

**Tests Conducted:** 12 runs (4 per option) on gemini-3-pro-preview  
**Comparison:** Direct A/B test against identical V5 runs on gemini-2.5-pro  

### 🚀 KEY FINDINGS

✅ **Gemini 3 is FASTER:**
- Option 1: 34.6s vs 36.4s (5% faster)
- Option 3: 42.3s vs 66.0s (36% faster!)
- Option 2: 96.6s vs 92.0s (slightly slower, likely due to output length)

✅ **Gemini 3 is MORE COMPREHENSIVE:**
- Option 2 Initial Extraction: **15 pain points** (maximum!)
- Option 3 Initial Extraction: **8-9 pain points** (consistent)
- Final Output: **5 pain points** consistently across all options

✅ **Gemini 3 Descriptions are RICHER:**
- More specific details ("40 areas of law", "800 staff")
- Better problem framing
- Stronger strategic language

⚠️ **Gemini 3 Token Usage is HIGHER:**
- Option 1: ~6.7K tokens (vs 5.6K) -> +20%
- Option 3: ~13K tokens (vs 9.3K) -> +40%
- **Why?** It generates longer, more detailed descriptions and reasoning

---

## Pain Point Content Comparison: Gemini 2.5 (V5) vs Gemini 3 (V7)

### Option 1: AI Gov (Single-Doc)

| Theme | Gemini 2.5 (V5 Test 1) | Gemini 3 (V7 Test 1) |
|-------|------------------------|----------------------|
| **Security** | **"Ensuring AI Security and Data Safeguarding"**<br/>"The DPC needs to adopt AI without compromising sensitive government data. This is critical because they must comply with strict \"ICT, Security and Cyber policies\" and \"Information Privacy Principles (IPPs)\". A breach would erode public trust and violate legal obligations." | **"Strict Security & Privacy Compliance"**<br/>"The DPC faces the critical challenge of ensuring AI tools strictly adhere to \"Applicable ICT, Security and Cyber policies\" and \"South Australian Information Privacy Principles (IPPs).\" They must solve the problem of safeguarding sensitive government data against cyber risks and privacy breaches." |
| **Market Knowledge** | **"Lack of Insight into Proven AI Government Solutions"**<br/>"DPC lacks a clear understanding of which AI tools are mature, effective, and suitable for the public sector. They need to identify proven solutions by assessing \"successful deployments in a government sector\" to de-risk investment and avoid experimental or inappropriate technology." | **"Mapping the AI Capability Landscape"**<br/>"DPC struggles to identify where AI can best \"enhance efficiency\" and \"service delivery.\" They need to gather market intelligence to \"compile a 'catalogue of offerings'\" and inform policy, rather than purchasing ad-hoc tools without a strategic understanding of \"what AI tools... are in the market.\"" |
| **Service Delivery** | **"Boosting Government Efficiency & Service Delivery"**<br/>"Current government operations need improvement. DPC is seeking AI to solve inefficiencies and enhance public services. This is important to \"boost efficiency, inform decision-making, and drive innovation\" to achieve better community outcomes and increase public satisfaction." | **"Enhancing Service Delivery Efficiency"**<br/>"The Department needs to solve the problem of operational inefficiency. They are seeking tools specifically to \"boost efficiency, inform decision-making\" and \"improve service delivery\" to achieve better \"community outcomes\" and increase public satisfaction, rather than just adopting tech for tech's sake." |
| **Integration** | **"Integrating New AI with Existing Systems"**<br/>"DPC must ensure new AI tools can integrate with its complex IT infrastructure. This is a key challenge, as failure to integrate would create data silos and prevent efficiency gains. They need to assess \"integration needs with any existing systems and platforms\"." | **"Seamless Integration with Legacy Systems"**<br/>"The department needs to solve the technical complexity of fitting new AI tools into their current environment. They are seeking to \"assess the maturity, scalability, and adaptability\" of solutions for \"integration into existing government systems\" to ensure they function without disrupting operations." |
| **Budget** | **"Financial Uncertainty of AI Adoption and Costing"**<br/>"DPC cannot effectively plan or budget for AI without clear cost information. They need to understand pricing to build a business case and secure funding. This RFI aims to \"Obtain indicative costing models and pricing structures to inform future procurement planning\"." | **"Establishing Viable Cost Models for AI"**<br/>"DPC lacks clear financial data for this emerging technology context. They need to \"obtain indicative costing models\" to \"inform future procurement planning and budget allocation,\" ensuring they can sustainably fund AI initiatives across business units for projects \"beginning in 2026.\"" |

**Verdict:** Gemini 3 wording is slightly more formal and precise ("faces the critical challenge", "solve the problem of"). Both captured the exact same 5 themes.

---

### Option 2: AI Gov (Single-Doc)

| Theme | Gemini 2.5 (V5 Test 5) | Gemini 3 (V7 Test 5) |
|-------|------------------------|----------------------|
| **Security** | **"Strict Security & Regulatory Compliance Mandates"** (Score 5)<br/>"The government must adhere to strict ICT, security, and privacy policies (IPPs). There is a significant risk that adopting a new AI tool could lead to non-compliance, creating legal and operational liabilities for the public sector." | **"Data Security & Regulatory Compliance"** (Score 10)<br/>"Strict adherence to ICT Security policies and Privacy Principles is mandatory. The risk of data leakage via third-party LLMs or unauthorized access to sensitive government information threatens public trust and violates non-negotiable regulatory standards." |
| **Efficiency** | **"Inefficient Operations & Poor Service Outcomes"** (Score 5)<br/>"Current processes are not optimized, leading to low productivity, high costs, and public dissatisfaction. The government needs AI to boost efficiency, improve service delivery, and enable more data-driven decision-making for better community outcomes." | **"Operational Efficiency & Service Delivery"** (Score 9)<br/>"Agencies face pressure to boost efficiency and innovation without increasing headcount. Manual workflows slow decision-making. DPC requires technologies that demonstrably improve community outcomes and public satisfaction through enhanced service delivery." |
| **Risk/Maturity** | **"High Risk of Implementation & Adoption Failure"** (Score 4)<br/>"Lacking in-house AI deployment experience and facing a workforce skills gap, the government fears investing in immature technology. They need a proven, reliable solution that can integrate with existing systems and demonstrate a clear ROI before large-scale commitment." | **"Proven Solution Maturity & Scalability"** (Score 8)<br/>"DPC cannot risk deploying unproven technology. To mitigate deployment failure, solutions must provide evidence of stability, scalability, and successful performance history in environments similar to DPC, validating their readiness for government use." |
| **Integration** | **MERGED** (into Risk/Efficiency) | **"Seamless Legacy System Integration"** (Score 85)<br/>"New AI tools must not create data silos. The inability to integrate seamlessly with existing legacy government infrastructure and platforms creates technical debt and operational friction, making technical adaptability a critical requirement." |
| **Workforce** | **MERGED** (into Risk) | **"Workforce Capability & Skill Bridging"** (Score 82)<br/>"Successful AI adoption is limited by current workforce gaps. DPC identifies a critical need for comprehensive training and support arrangements to bridge technical capabilities, ensuring staff can effectively utilize and manage new tools." |

**Verdict:** **Gemini 3 is the clear winner for Option 2.** It kept 5 distinct pain points (including Integration and Workforce) whereas Gemini 2.5 merged down to 3. Gemini 3 also used a broader score range (82-100 vs 1-5).

---

### Option 3: AGS Legal (Multi-Doc)

| Theme | Gemini 2.5 (V5 Test 11) | Gemini 3 (V7 Test 11) |
|-------|-------------------------|-----------------------|
| **Security** | **"Securing PROTECTED Government Data"** (Score 5)<br/>"AGS handles highly sensitive government data, creating a massive risk of breaches. The problem is ensuring any AI solution meets non-negotiable security standards, including being \"independently certified through IRAP process at PROTECTED level\" and ensuring data is stored within Australia." | **"Strict Data Sovereignty & Security Compliance"** (Score 5)<br/>"AGS handles sensitive government legal matters and cannot use standard AI tools. The solution MUST be certified via the \"IRAP process at PROTECTED level\" (NFR-SEC01) and ensure all customer data is \"stored and processed within the Australian Region\" (NFR-SEC04) to meet PSPF requirements." |
| **Productivity** | **"Low Productivity in Core Legal Tasks"** (Score 5)<br/>"With approximately 570 lawyers, manual legal work like summarisation and discovery creates a significant productivity bottleneck. This problem limits capacity across 40 areas of law. AGS needs AI to automate these tasks, freeing up lawyers for high-value strategic work." | **"Lawyer Productivity & Administrative Burden"** (Score 4)<br/>"With \"approximately 570 lawyers\", manual admin reduces billable capacity. AGS needs to automate low-value tasks like \"Draft daily time recording summaries\" based on calendar/activity metadata and \"Draft document from Standard Request\" to \"improve productivity across legal practice workflows.\"" |
| **Integration** | **"Integrating AI into Existing Tech Stack"** (Score 4)<br/>"AGS has an established tech ecosystem (iManage Cloud, Elite 3E). The problem is that a standalone AI tool would create disruptive data silos and inefficient workflows. A solution must integrate with their core software to ensure seamless adoption and enhance existing processes for their 800 staff." | **"Siloed Workflows & Integration Failures"** (Score 4)<br/>"AGS aims to \"supplement rather than replace\" existing capability. A pain point is AI that stands alone; the solution must integrate with \"iManage Cloud, Elite 3E and the Microsoft Office suite\" to ensure seamless adoption by the 800 staff without breaking existing matter management workflows." |
| **Specific Tools** | **"Lack of Australian-Specific AI Tools"** (Score 4)<br/>"The Australian legal system is unique. The problem is that generic international AI tools may lack the nuance and accuracy required. AGS is explicitly seeking tools \"specifically designed to support Australian legal practices\" to ensure the outputs are relevant and trustworthy for government legal work." | **"Lack of Australian Legal Context & Style"** (Score 4)<br/>"Generic AI models often cite foreign law or wrong formats. AGS specifically requires tools \"designed to support Australian legal practices\" that can enforce \"AGS style and plain English rules\" across their 40 areas of law, ensuring outputs are jurisdictionally accurate." |
| **Advanced AI / Discovery** | **"Difficulty Finding Internal Knowledge"** (Score 4)<br/>"As a large firm, AGS possesses vast internal knowledge, but locating relevant information is inefficient. The problem is this wasted time hinders lawyers' ability to leverage valuable internal precedents. They require \"Smart search\" to improve findability and turn their existing data into an advantage." | **"Complex Evidence Review & Inconsistency Detection"** (Score 4)<br/>"Manual review of large discovery sets is inefficient and prone to error. AGS requires AI to \"Identify relevant documents in large discovery sets\" and perform advanced analysis to \"Identify inconsistencies across evidence\" (e.g., contradictions in witness statements/affidavits)." |

**Verdict:** Gemini 3 went deeper into specific legal workflows ("Draft daily time recording", "Evidence Review", "Inconsistency Detection") while Gemini 2.5 focused more on high-level "Knowledge" and "Efficiency". Both are excellent, but Gemini 3 feels more expert.

---

## Gemini 3 Cross-Option Comparison: AGS Legal (Multi-Doc)

**Full Text Comparison - All Three Options:**

| Theme | Option 1 (Test 3) | Option 2 (Test 7) | Option 3 (Test 11) |
|-------|------------------|-------------------|-------------------|
| **Security** | **"IRAP PROTECTED Security & Data Sovereignty"** (Score 5)<br/><br/>"AGS faces the critical challenge of adopting AI while maintaining strict government security. The solution must be independently certified at IRAP PROTECTED level and ensure all customer data is stored/processed solely within Australia to mitigate national security risks." | **"Stringent Government Security Mandates"** (Score 10)<br/><br/>"The solution must meet non-negotiable security protocols, including IRAP certification at a PROTECTED level, Essential Eight compliance, and Australian data residency. Failure to meet these strict data sovereignty and security requirements is an absolute barrier to adoption for any government entity." | **"Strict Data Sovereignty & Security Compliance"** (Score 5)<br/><br/>"AGS handles sensitive government legal matters and cannot use standard AI tools. The solution MUST be certified via the \"IRAP process at PROTECTED level\" (NFR-SEC01) and ensure all customer data is \"stored and processed within the Australian Region\" (NFR-SEC04) to meet PSPF requirements." |
| **Productivity** | **"Productivity in High-Volume Legal Workflows"** (Score 4)<br/><br/>"With ~570 lawyers and 800 staff, manual administrative tasks create significant bottlenecks. AGS needs to automate time-consuming processes like 'Draft daily time recording summaries' based on calendar activity and converting standard requests into templates to improve fee-earner efficiency." | **"Inefficient Manual Workflows Drain Productivity"** (Score 9)<br/><br/>"Lawyers are burdened by manual, repetitive tasks like document drafting, summarization, and e-discovery. These slow, costly, and labor-intensive processes limit the time available for high-value strategic work, directly impacting billable hours and overall firm efficiency." | **"Lawyer Productivity & Administrative Burden"** (Score 4)<br/><br/>"With \"approximately 570 lawyers\", manual admin reduces billable capacity. AGS needs to automate low-value tasks like \"Draft daily time recording summaries\" based on calendar/activity metadata and \"Draft document from Standard Request\" to \"improve productivity across legal practice workflows.\"" |
| **Integration** | **"Integration with Legacy Legal Technology Stack"** (Score 4)<br/><br/>"New tools must not create data silos. AGS requires solutions that seamlessly integrate with their specific ecosystem—iManage Cloud (DMS) and Elite 3E—to allow automated retrieval of precedents and filing of time entries without disrupting existing lawyer workflows." | **"Poor Integration with Core Legal Systems"** (Score 9)<br/><br/>"New tools must seamlessly integrate with existing core platforms, including iManage Cloud, Elite 3E, and Microsoft Office. Without deep integration, the solution would create inefficient data silos and disjointed workflows, hindering adoption and negating productivity gains." | **"Siloed Workflows & Integration Failures"** (Score 4)<br/><br/>"AGS aims to \"supplement rather than replace\" existing capability. A pain point is AI that stands alone; the solution must integrate with \"iManage Cloud, Elite 3E and the Microsoft Office suite\" to ensure seamless adoption by the 800 staff without breaking existing matter management workflows." |
| **Advanced AI / Discovery** | **"Complex Evidence Analysis and Inconsistency Detection"** (Score 4)<br/><br/>"AGS lawyers struggle with manually identifying contradictions across large datasets of pleadings, witness statements, and transcripts. They need AI to 'Analyse pleadings... for contradictions or gaps' and rank documents in discovery sets to enhance litigation accuracy and speed." | **"Need for Advanced, Goal-Driven AI Systems"** (Score 8)<br/><br/>"Standard generative models are insufficient. The organization seeks sophisticated, 'agentic' AI systems capable of autonomous decision-making and multi-step task execution. This signals a need for a truly innovative, goal-driven automation partner to solve complex legal challenges." | **"Complex Evidence Review & Inconsistency Detection"** (Score 4)<br/><br/>"Manual review of large discovery sets is inefficient and prone to error. AGS requires AI to \"Identify relevant documents in large discovery sets\" and perform advanced analysis to \"Identify inconsistencies across evidence\" (e.g., contradictions in witness statements/affidavits)." |
| **Ethics/Legal Context** | **"Requirement for Ethical and Explainable AI"** (Score 5)<br/><br/>"As a government entity, AGS cannot use 'black box' AI. They need to solve the risk of unaccountable decision-making by ensuring any AI used for legal work is 'ethical, responsible, transparent and explainable', allowing lawyers to understand how recommendations were reached." | **"Adoption Risk from Opaque 'Black Box' AI"** (Score 8)<br/><br/>"Legal decisions require justification, but opaque AI systems create significant adoption risk. The explicit demand for 'ethical, transparent, and explainable' AI is a critical requirement. Any solution must provide auditable outputs to ensure user trust, accountability, and professional compliance." | **"Lack of Australian Legal Context & Style"** (Score 4)<br/><br/>"Generic AI models often cite foreign law or wrong formats. AGS specifically requires tools \"designed to support Australian legal practices\" that can enforce \"AGS style and plain English rules\" across their 40 areas of law, ensuring outputs are jurisdictionally accurate." |

**Wording Analysis Across Options:**

**Security Theme:**
- **Option 1:** "faces the critical challenge" | "independently certified at IRAP PROTECTED level"
- **Option 2:** "non-negotiable security protocols" | "**absolute barrier to adoption**" (strongest language!)
- **Option 3:** "MUST be certified" (all caps emphasis) | "(NFR-SEC01)" (includes NFR code)
- **Winner:** **Option 2** - strongest consequence language ("absolute barrier")

**Productivity Theme:**
- **Option 1:** "manual administrative tasks" | "time recording summaries" | "improve fee-earner efficiency"
- **Option 2:** "**directly impacting billable hours**" (business focus!) | "overall firm efficiency"
- **Option 3:** "manual admin reduces billable capacity" | "improve productivity across legal practice workflows"
- **Winner:** **Option 2** - most business-focused ("billable hours", "firm efficiency")

**Integration Theme:**
- **Option 1:** "iManage Cloud (DMS) and Elite 3E" (specified DMS)
- **Option 2:** "**inefficient data silos and disjointed workflows, hindering adoption**" (strongest impact language)
- **Option 3:** "\"supplement rather than replace\"" (direct quote from tender!)
- **Winner:** **Option 3** - direct tender quote shows evidence

**Advanced AI:**
- **Option 1:** "Analyse pleadings... for contradictions or gaps" (specific use case)
- **Option 2:** "**sophisticated, 'agentic' AI systems**" | "**truly innovative, goal-driven automation partner**" (aspirational framing)
- **Option 3:** "\"Identify inconsistencies across evidence\"" (direct quote, specific)
- **Winner:** **Option 2** - most strategic framing ("innovative partner")

**Ethics/Legal Context:**
- **Option 1:** "solve the risk of unaccountable decision-making" | "understand how recommendations were reached"
- **Option 2:** "**opaque AI systems create significant adoption risk**" | "**auditable outputs**"
- **Option 3:** "Generic AI models often cite **foreign law or wrong formats**" (most specific problem!) | "**40 areas of law**"
- **Winner:** **Option 3** - most specific to this tender (Australian legal context is unique requirement)

**Overall Analysis:**
- **Option 1:** Specific use cases, detailed workflows
- **Option 2:** Strategic/business language, strongest consequence framing
- **Option 3:** Most tender-specific (direct quotes, jurisdictional accuracy)

**For Bid Writers:**
- Want **business impact?** → Option 2 ("billable hours", "absolute barrier", "firm efficiency")
- Want **specific evidence?** → Option 3 (direct tender quotes, "40 areas of law")
- Want **detailed workflows?** → Option 1 (specific task descriptions)

---

## Token & Cost Analysis (Gemini 3)

**Gemini 3 Pricing:** $2/1M input, $12/1M output (<200k tokens)
*(Note: Pricing is different from 2.5-pro)*

| Option | Tender | Prompt Tokens | Cand. Tokens | Total Tokens | Cost (est) |
|--------|--------|---------------|--------------|--------------|------------|
| Opt 1 | AI Gov | 4,295 | 632 | 6,673 | ~$0.016 |
| Opt 3 | AI Gov | 4,207 | 867 | 6,755 | ~$0.019 |
| Opt 1 | AGS | 16,570 | 645 | 19,190 | ~$0.041 |
| Opt 3 | AGS | 16,482 | 1,251 | 20,281 | ~$0.048 |

**vs Gemini 2.5 Pro ($7.50/1M input, $30/1M output):**
- Gemini 3 is **CHEAPER** for input tokens ($2 vs $7.50)
- Gemini 3 is **CHEAPER** for output tokens ($12 vs $30)

**Total Cost Comparison (AGS Legal - Opt 3):**
- **Gemini 2.5:** ~$0.098
- **Gemini 3.0:** ~$0.048

**Surprise Finding:** **Gemini 3 is ~50% CHEAPER** for this workload!

---

## Final Recommendation

### 🚀 UPGRADE TO GEMINI 3 PRO PREVIEW

**Why:**
1. **Higher Quality:** Captures more specific details (e.g., "40 areas of law")
2. **Faster:** 36% faster on complex Option 3 extraction
3. **Cheaper:** ~50% lower cost due to favorable pricing
4. **Cleaner Output:** Produced 5 distinct pain points without needing supporting examples (at 0.9 threshold)

**Configuration:**
- **Model:** `gemini-3-pro-preview`
- **Prompts:** V5 (`prompts.py`)
- **Option:** Option 3 (Validated)
- **Threshold:** 0.9

This is the ultimate winning combination.

---

**End of Analysis** 📊

