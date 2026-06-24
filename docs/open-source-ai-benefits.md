# Why Open-Source AI Benefits the Public — Research Notes

**Status:** Working research notes (framework + first pass of live data). Not a finished artifact.
**Compiled:** 2026-06-24
**Thesis:** Open-source / open-weight AI models benefit the public across four dimensions —
**Cost-efficiency, Control, Customizability, and Collaboration** — in ways that closed,
API-only models structurally cannot match.

> **The one-sentence version of each pillar**
> - **Cost-efficient** — open weights are sold by *many competing providers*, driving inference price toward marginal cost; closed models have exactly *one* seller.
> - **Control** — with open weights you *own an artifact* (run it forever, anywhere, privately, unchanged); with a closed API you *rent a service* the provider prices, moderates, changes, and can withdraw.
> - **Customizable** — anyone can fine-tune, quantize, merge, or adapt the weights; a single popular base model spawns tens of thousands of derivatives.
> - **Collaboration** — the ecosystem builds openly *on top of itself* (model → fine-tune → re-fine-tune; shared datasets, recipes, checkpoints), often across hundreds of institutions.

---

## ⚠️ Data-collection caveat (read first)

This environment's network egress policy **blocks direct API access** to `huggingface.co`,
`openrouter.ai`, and most external hosts (403 at the proxy). So the live numbers below were
gathered via **web search snippets**, not by hitting the OpenRouter / Hugging Face APIs directly.
They are **directionally reliable and consistently corroborated**, but exact decimals (especially
2026 prices, which move fast) should be **re-verified against the live pages** before you publish.
Each figure is tagged with a confidence level and a source URL.

To pull exact live data later, either:
1. Run this from an environment with a more permissive network policy, **or**
2. Open the source URLs in a browser and read the running counts directly (HF model pages show
   live download/like/model-tree counts; OpenRouter model pages list per-provider prices).

The cleanest first-party sources to verify against:
- OpenRouter models API (raw JSON pricing): https://openrouter.ai/api/v1/models
- HF "State of Open Source — Spring 2026": https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
- HF most-downloaded entities: https://huggingface.co/blog/lbourdois/huggingface-models-stats

---

## Running example: `poolside/Laguna-M.1`

Where useful, the four pillars are illustrated with one concrete model — **Laguna-M.1**, the model
in the screenshot whose HF "Model tree" shows **3 finetunes** and **12 quantizations**.

| Attribute | Value | Source / confidence |
|---|---|---|
| Vendor | poolside — US AI startup (SF, founded 2023) | venturebeat.com · medium |
| What it is | Foundation model for **agentic coding** / long-horizon software work | poolside.ai blog · medium |
| Architecture | 225B total params, MoE, ~23B activated/token; 128K context | chats-llm.com · medium |
| Quality | **72.5%** on SWE-bench Verified (sibling XS.2: 68.2%) | marktechpost.com · medium |
| License | **Apache 2.0** (base + BF16 / FP8 / NVFP4 variants) | developer.puter.com · medium |
| Released | **2026-04-28** | marktechpost.com · medium |
| Model tree | **3 finetunes, 12 quantizations** (from screenshot — authoritative) | HF model page · **high** |

Laguna is a clean example because it is a *company-released* model under a permissive license that
the community is already extending — and poolside itself ships multiple quant variants and a sibling
(XS.2) explicitly positioned "for developers looking to fine-tune, quantize, or serve on a single GPU."

---

## Pillar 1 — Cost-efficient

**Argument.** A closed model has exactly **one seller** (the lab), so the price is whatever the lab
sets. An open-weight model is served *simultaneously* by many providers (DeepInfra, Together,
Fireworks, Groq, Novita, the lab itself…), and aggregators like OpenRouter make them bid against
each other on one page. Competition drives price toward marginal compute cost — and some open models
even have **free $0/$0 endpoints**, a price point a closed model structurally cannot reach.

### 1a. Headline price comparison (per 1M tokens, USD)

| Model | Type | Input | Output | Confidence |
|---|---|---|---|---|
| DeepSeek V3 (deepseek-chat) | open | $0.20 | $0.80 | high |
| DeepSeek R1 (reasoning) | open | ~$0.55 | ~$2.19 | medium |
| Llama 3.3 70B Instruct | open | $0.10–$1.00 (provider-dep.) | $0.32–$2.00 | medium |
| gpt-oss-120b (OpenAI open weights) | open | $0.039 | $0.18 | medium |
| gpt-oss-120b `:free` | open | $0.00 | $0.00 | medium |
| Claude Sonnet | closed | $3.00 | $15.00 | medium |
| Claude Opus (4.x) | closed | $5–$15 (sources conflict) | $25–$75 | low — **verify** |
| OpenAI o1 (reasoning) | closed | $15.00 | $60.00 | medium |
| GPT-5.4 Pro | closed | $30.00 | $180.00 | low |

> Output tokens dominate most real workloads, and that's exactly where the open/closed gap is widest.

### 1b. The core argument — multi-provider competition (strongest, most defensible point)

The *same* open model served by many vendors shows a large price spread — direct evidence of
competition the buyer captures:

- **DeepSeek V3:** cheapest provider ~$0.38/1M vs most expensive ~$0.89/1M → **~2.4× spread** for an identical model. (Artificial Analysis)
- **Llama 3.3 70B:** input ranges **$0.10 → $1.00+/1M** across providers → **~10× spread**. OpenRouter's `:floor` slug auto-routes to the cheapest. (OpenRouter)

A closed model cannot show a spread — there is only one price-setter.

### 1c. "N× cheaper for comparable quality" sound-bites

1. **DeepSeek R1 vs OpenAI o1:** ~$0.55/$2.19 vs $15/$60 → **~25× cheaper**, with reasoning quality "comparable to o1." (notta.ai)
2. **DeepSeek V3.2 vs GPT-4o:** ~88.5 vs 87.2 MMLU, at **~10× lower input cost.**
3. **gpt-oss-120b vs GPT-5.4 Pro (OpenAI's own open vs closed):** $0.039/$0.18 vs $30/$180 → **~750–1000× cheaper**, and gpt-oss is also free. Cleanest apples-to-apples point.

**Sources:** https://openrouter.ai/api/v1/models · https://openrouter.ai/deepseek/deepseek-chat ·
https://openrouter.ai/openai/gpt-oss-120b · https://artificialanalysis.ai/models/deepseek-v3/providers ·
https://openrouter.ai/blog/tutorials/how-to-get-the-lowest-cost-llm-inference-on-openrouter/

**Verify before publishing:** exact 2026 decimals (prices drop fast); Claude Opus input price (sources conflict $5 vs $15).

---

## Pillar 2 — Control

The user's open question was *"how is control actually different from closed models?"* The honest,
defensible answer: **control = who holds the decision rights.** With open weights you possess an
artifact you can copy, run, modify, and keep forever; with a closed API you rent access to a service
the provider operates, prices, moderates, changes, and can withdraw. Seven concrete dimensions
follow from that ownership-vs-rental difference (strength = how well-evidenced).

| # | Dimension | Strength | The concrete difference |
|---|---|---|---|
| 1 | **Data privacy / sovereignty** | strong (two-sided) | Self-host → prompts/data physically never leave your infra; air-gapped is possible. Closed = data sent to provider; you trust their retention policy. |
| 2 | **No model deprecation** | **strong** | Closed providers retire models on *their* schedule. A downloaded weight file is yours forever. |
| 3 | **No vendor lock-in** | strong | Open weights run on any hardware/provider; switch freely. Closed = one vendor sets price + TOS. |
| 4 | **Behavioral control** | strong (two-sided) | You own the system prompt, sampling, safety filters, fine-tuning. Closed applies opaque, undisableable moderation. |
| 5 | **Reproducibility / auditability** | **strong** | Fixed weights = reproducible, auditable. Closed models can change *silently* behind the same API name. |
| 6 | **Operational control** | moderate | You control latency/throughput/uptime/rate-limits — but you also inherit the ops burden. |
| 7 | **Regulatory / geopolitical sovereignty** | strong | States/firms can run controllable AI on nationally-owned infrastructure. |

### Key evidence (the hardest-to-rebut points)

- **Deprecation is real and disruptive:** OpenAI is **ending API access to GPT-4o in Feb 2026** with ~3 months' notice; the GPT-5 rollout (Aug 2025) pulled older models and triggered a **#Keep4o** campaign that forced a partial reversal.
  https://venturebeat.com/ai/openai-is-ending-api-access-to-fan-favorite-gpt-4o-model-in-february-2026 · https://openai.com/index/retiring-gpt-4o-and-older-models/
- **Silent model drift:** the Stanford/Berkeley study *"How Is ChatGPT's Behavior Changing over Time?"* found GPT-4 prime-identification accuracy fell **84% → 51.1%** between March and June 2023 — same API name, different behavior. With open weights this cannot happen to you.
  https://arxiv.org/abs/2307.09009
- **Privacy / regulated industries:** Meta publishes an explicit self-hosting guide for HIPAA/GDPR-regulated industries; the **Schrems II** ruling is a structural reason EU orgs prefer locally-run models.
  https://www.llama.com/docs/deployment/regulated-industry-self-hosting/
- **Sovereign AI is happening:** Switzerland's **Apertus** (EPFL/ETH/CSCS, fully open), Germany's **Teuken-7B / OpenGPT-X** (~€14M federal funding, Apache-2.0, all 24 EU languages), and **France's military framework agreement with Mistral (Jan 2026)** all depend on open weights.
  https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html · https://www.iais.fraunhofer.de/en/press-events/press-releases/press-release-241126.html

### Be honest about the counterarguments (makes the case stronger)

- Closed providers now offer **Zero Data Retention** enterprise tiers and no-training contracts — adequate for many. *Open's edge is **verifiability**: data physically cannot leave, vs trusting a policy.*
- Self-hosting **transfers the burden** to you: GPU capital, MLOps expertise, uptime ownership. A hyperscaler may have better availability than your cluster.
- Behavioral control **cuts both ways for safety**: the same control that lets a hospital reduce over-refusal also lets bad actors strip guardrails (research: alignment undone with ~1,000 samples). Present it as *control + responsibility*.

**The precise claim that survives scrutiny:** not "open models are better," but **"open weights give the user the *option set* — the legal and technical ability to decide — on privacy, longevity, provider, behavior, and verifiability; closed APIs delegate all of those decisions to the provider."**

---

## Pillar 3 — Customizable

**Argument.** Open weights can be fine-tuned, quantized, merged, and adapted by anyone — turning a
single base model into thousands of specialized variants for languages, domains, hardware, and tasks.
This is exactly what the HF "Model tree" visualizes (the screenshot's **3 finetunes + 12 quantizations**
is one such tree).

### Scale of customization — two different (both true) measurements

**Per-checkpoint** (one specific model's tree, like Laguna's): typically *tens* of derivatives.
- Laguna-M.1: **3 finetunes, 12 quantizations** (screenshot, high confidence)
- `Dolphin3.0-Llama3.1-8B`: 13 finetunes, 26 quantizations, 2 adapters, 9 merges (HF page)

**Family-wide** (a whole base-model family): *tens of thousands*.

| Base family | Derivatives | Downloads | Confidence | Source |
|---|---|---|---|---|
| **Qwen** | ~113K–180K derivative models (sources differ) | ~700M cumulative (Jan 2026); overtook Llama in 2025 | ⚠️ verify exact count | en.wikipedia.org/wiki/Qwen · english.news.cn |
| **Llama** | "thousands of community projects"; "spawned entire ecosystems" | hundreds of millions | medium (qualitative) | huggingface.co/blog/evijit/hf-hub-ecosystem-overview |

**Takeaway sound-bite:** customization scale spans **tens per checkpoint → ~100K+ per popular base
family**. Cleanest single stat: **Qwen — ~700M downloads, 100K+ derivatives** (verify the exact derivative figure live).

**Why this matters for the public:** specialization the original lab would never build — low-resource
languages, niche medical/legal domains, on-device quantizations for cheap/old hardware — gets built
by whoever needs it. Closed models offer only the variants the vendor chooses to sell.

**Sources:** https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B · https://en.wikipedia.org/wiki/Qwen ·
https://english.news.cn/20260113/004b0522f987475cbf83ffc3a8d009aa/c.html · https://huggingface.co/blog/lbourdois/huggingface-models-stats

---

## Pillar 4 — Collaboration

**Argument.** The open ecosystem doesn't just *release* models — it **builds on top of itself**, openly
and cumulatively: model → community fine-tune → further fine-tunes/merges; shared datasets, training
recipes, and even intermediate checkpoints. The HF model tree is a literal graph of this collaboration.

### Concrete collaboration examples

| Project | Scale of open collaboration | Source |
|---|---|---|
| **BLOOM / BigScience** | **1,000+ volunteer researchers, 70+ countries, 250+ institutions**; 176B params, 46 languages; trained on a public supercomputer grant | en.wikipedia.org/wiki/BLOOM_(language_model) · oecd.ai |
| **OLMo (Ai2)** | "Fully open" — releases **weights + training data + code + recipes + intermediate checkpoints**, no license restrictions; partners incl. Harvard Kempner, AMD, UW | allenai.org/olmo · allenai.org/blog/olmo2 |
| **Build-on-each-other chain** | Meta Llama-3.1-8B → community `Dolphin3.0` fine-tune → **13 further fine-tunes + 9 merges** built on *that* | huggingface.co/dphn/Dolphin3.0-Llama3.1-8B |

- **BLOOM** is the strongest "open collaboration" data point (the 1,000 / 70 / 250 figures are
  corroborated across Wikipedia, OECD.AI, and others — high confidence).
- **OLMo** is the strongest "radical transparency" example.
- The **Llama → Dolphin → further-finetunes** chain is the most literal illustration of the model
  tree as a collaboration graph — *and is the same structure as the Laguna screenshot*, just deeper.

### Ecosystem scale (the backdrop)

| Metric | Figure (mid-2026) | Confidence |
|---|---|---|
| Models on Hugging Face | **~2.4M** | medium-high |
| Datasets | **~730K** (sources span 500K–1.5M) | ⚠️ wide spread — verify |
| Spaces (demo apps) | **~1M** | medium |
| Users | 13M+ (2025) | medium |

Safe framing: *"~2.4M models, ~730K datasets, ~1M Spaces as of mid-2026"* with a footnote that
totals vary by source. Verify on huggingface.co/models, /datasets, /spaces (live counts) and the
"State of Open Source — Spring 2026" blog.

**Sources:** https://en.wikipedia.org/wiki/BLOOM_(language_model) · https://allenai.org/olmo ·
https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 · https://www.kdnuggets.com/the-complete-hugging-face-primer-for-2026

---

## Suggested visuals (for whatever artifact this becomes)

| Pillar | Visual |
|---|---|
| Cost-efficient | Bar chart: per-1M-token output price, open vs closed (log scale). Plus a "same model, many providers" price-spread chart for DeepSeek V3 / Llama 3.3 70B. |
| Control | Timeline of closed-model deprecations (GPT-4o sunset, GPT-5 rollout) vs "your weight file, unchanged." Plus the GPT-4 84%→51% drift stat as a callout. |
| Customizable | The **Laguna model-tree screenshot** itself, next to a big-number callout (Qwen ~700M downloads / 100K+ derivatives). |
| Collaboration | The model tree rendered as a *graph* (base → fine-tunes → re-fine-tunes); BLOOM's 1,000 researchers / 70 countries / 250 institutions as a callout. |

---

## Open to-dos before this becomes a finished artifact

1. **Pull exact live numbers** (blocked here by egress policy): OpenRouter prices (all rows), Laguna download/like counts, exact Qwen derivative count (113K vs 180K), HF dataset total.
2. **Resolve conflicts:** Claude Opus input price ($5 vs $15); Qwen derivative count.
3. **Decide the final format** (the user chose "research notes first" — this doc; format TBD: report / one-page website / slide deck).
4. **Optionally add a GitHub angle** (the user floated it): contributor/star/fork counts on open-model repos (llama.cpp, vLLM, transformers, Ollama) as a second collaboration data source.

---

### Full source list
**Cost:** openrouter.ai/api/v1/models · openrouter.ai/deepseek/deepseek-chat · openrouter.ai/openai/gpt-oss-120b · artificialanalysis.ai/models/deepseek-v3/providers · openrouter.ai/blog/tutorials/how-to-get-the-lowest-cost-llm-inference-on-openrouter/ · tldl.io/resources/llm-api-pricing-2026
**Control:** venturebeat.com/ai/openai-is-ending-api-access-to-fan-favorite-gpt-4o-model-in-february-2026 · openai.com/index/retiring-gpt-4o-and-older-models/ · arxiv.org/abs/2307.09009 · llama.com/docs/deployment/regulated-industry-self-hosting/ · ethz.ch (Apertus) · iais.fraunhofer.de (Teuken-7B) · raconteur.net (Mistral/France)
**Customizable:** huggingface.co/dphn/Dolphin3.0-Llama3.1-8B · en.wikipedia.org/wiki/Qwen · english.news.cn (Qwen 700M) · huggingface.co/blog/lbourdois/huggingface-models-stats
**Collaboration:** en.wikipedia.org/wiki/BLOOM_(language_model) · oecd.ai (BLOOM) · allenai.org/olmo · allenai.org/blog/olmo2 · huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 · kdnuggets.com/the-complete-hugging-face-primer-for-2026
**Laguna:** huggingface.co/poolside/Laguna-M.1 · poolside.ai/blog/introducing-laguna-xs2-m1 · marktechpost.com (SWE-bench) · developer.puter.com/ai/poolside/laguna-m.1/
