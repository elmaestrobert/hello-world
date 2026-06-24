# Open-Source AI Benefits — The Argument (data → claim)

**Format:** For each of the four pillars: *with **data X**, we can show **Y***, then a short elaboration.
**Backing evidence & sources:** see [`open-source-ai-benefits.md`](./open-source-ai-benefits.md).
**Note:** figures are first-pass (gathered via web search; this session's network policy blocked direct
HF/OpenRouter API access). Re-verify exact numbers against the live source pages before publishing.

---

## 1. Cost-efficient

> **With data:** OpenRouter per-token pricing showing the *same* open model sold by many providers at
> a large price spread (DeepSeek V3 ~2.4× cheapest-to-priciest; Llama 3.3 70B ~10×), open free
> `$0/$0` endpoints, and head-to-head ratios like gpt-oss-120b vs GPT-5.4 Pro (~750–1000× cheaper) or
> DeepSeek R1 vs OpenAI o1 (~25× cheaper at comparable quality)…
>
> **…we can show that** open weights drive inference cost toward marginal compute cost, because buyers
> get a competitive market instead of a single price-setter.

**Elaboration.** The point isn't only that open models are cheap today — it's *why* they stay cheap.
A closed model has exactly one seller, so its price is whatever the lab decides. An open model is
served simultaneously by DeepInfra, Together, Fireworks, Groq, Novita, the lab itself, and others, and
aggregators let them bid against each other on one page (OpenRouter's `:floor` even auto-routes to the
cheapest). The price *spread* on an identical model is the visible fingerprint of that competition —
something a closed model can never display. For the public this means lower bills, free tiers for
students/hobbyists/non-profits, and no exposure to unilateral price hikes.

---

## 2. Control

> **With data:** dated closed-model deprecations (OpenAI ending GPT-4o API access Feb 2026; the GPT-5
> rollout pulling older models → the #Keep4o reversal), the Stanford/Berkeley "behavior changing over
> time" study (GPT-4 accuracy 84% → 51% behind the *same* API name), regulated-industry self-hosting
> guides, and sovereign-AI programs (Apertus, Teuken-7B, France's Mistral military deal)…
>
> **…we can show that** open weights give the *user* the decision rights over privacy, longevity,
> provider, behavior, and verifiability — rights that a closed API delegates entirely to the vendor.

**Elaboration.** This is the pillar that's easy to hand-wave, so anchor it in the ownership-vs-rental
distinction: an open weight file is an *artifact you possess* (run it forever, anywhere, privately,
unchanged); a closed model is a *service you rent*. From that one difference, every concrete advantage
follows — the vendor can't sunset your model, can't silently change it underneath you, can't see your
data if you self-host, and can't impose moderation you can't inspect. Be honest that this transfers a
burden too (you now own the GPUs and uptime) and that the same control is a safety double-edge — that
candor makes the argument more credible, not less. The claim that survives scrutiny: not "open is
better," but "open holds the decision rights with the user."

---

## 3. Customizable

> **With data:** Hugging Face "Model tree" counts — *tens* of derivatives per checkpoint (Laguna-M.1's
> 3 finetunes + 12 quantizations; Dolphin3.0's 13 finetunes / 26 quants / 9 merges) scaling to
> *~100K+* per popular base family (Qwen: ~700M downloads, 100K+ derivative models)…
>
> **…we can show that** open weights let anyone specialize a base model for languages, domains, and
> hardware the original lab would never serve — producing thousands of purpose-built variants.

**Elaboration.** The Laguna screenshot is the perfect single visual: one company-released, Apache-2.0
model that the community is already extending into fine-tuned and quantized variants. Multiply that
pattern across a whole family and you get the Qwen-scale numbers. What this buys the public is the
*long tail* — low-resource-language models, niche medical/legal fine-tunes, and tiny quantizations
that run on cheap or old hardware. A closed model offers only the handful of variants the vendor
chooses to sell; an open one offers whatever anyone in the world needs enough to build.

---

## 4. Collaboration

> **With data:** the model tree as a literal build-on-each-other graph (Meta Llama-3.1-8B → community
> Dolphin3.0 finetune → 13 *further* finetunes + 9 merges on top of that), plus openly-collaborative
> projects at scale — BLOOM/BigScience (1,000+ researchers, 70+ countries, 250+ institutions) and OLMo
> (fully open weights + data + code + recipes + checkpoints), against a ~2.4M-model ecosystem…
>
> **…we can show that** open AI isn't just *released* — it compounds, with the community building
> cumulatively on each other's models, datasets, and recipes in the open.

**Elaboration.** This is the same model-tree structure as the customizability pillar, but read as a
*social* graph rather than a technical one: each node is someone's contribution that someone else then
built upon. BLOOM is the headline collaboration stat (a thousand volunteers across 250 institutions);
OLMo is the radical-transparency exemplar (everything open, down to intermediate checkpoints); and the
Llama → Dolphin → further-finetunes chain is the most literal "standing on each other's shoulders"
example — and it's the *same shape* as the Laguna screenshot, just deeper. The public benefit is
speed and reach: improvements flow back into the commons instead of staying locked inside one vendor.

---

### Suggested visual per claim
| Pillar | Visual that makes the "show Y" land |
|---|---|
| Cost-efficient | Same-model price-spread chart (DeepSeek V3 / Llama 3.3 70B across providers) + open-vs-closed output-price bars (log scale) |
| Control | Deprecation timeline (GPT-4o sunset, GPT-5 rollout) vs "your weight file, unchanged"; 84%→51% drift callout |
| Customizable | The Laguna model-tree screenshot beside a Qwen big-number callout |
| Collaboration | The model tree rendered as a graph; BLOOM's 1,000 / 70 / 250 as a callout |
