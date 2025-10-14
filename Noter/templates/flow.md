## Speech to text model:
1. Soniox -> $200 free credits and works at a rate of $0.10/hr for uploaded file recordings and $0.12/hr for live streaming audio, which
is the cheapest and according to the benchmarks has highest speech recognition accuracy.
2. AssemblyAI -> $50 free credits and works at a rate of $0.27/hr for the universal 2 model.
3. Deepgram -> can check out the nova 3 model which is $0.26/hr which claims very low median WER of 5.26%. High speed and low latency.


## Audio preprocessing pipeline so that STT model can give better accuracy cost effectively:
1. Voice Activity Detection (VAD): use pyannote.audio to analyze the audio and remove long periods of silence. Naturally breaks the audio
into segments of continuous speech, reducing total amount of audio.

2. Chunking with overlap (optional): After VAD, some speech segments may still be too large for the STT provider's limit. So, can divide
long segments into smaller chunks with overlap of 2-5 seconds between chunks, so that the ASR model has essential context at the boundaries
of each segement.

This all should be given to the STT provider's Batch API, maximizing accuracy and minimizing cost.

## Transcript-to-Markdown structuring
Once we have the high-quality transcript, next step is to structure it into a standardized Markdown note while preserving my "human essence".
system should format and organize my thoughts and not rewrite them.
To do so we need a highly constrained prompt, with hierarchical processing strategy.

### Extractive-First Prompting
Prompt Template:
```markdown
SYSTEM Prompt:
You are a technical copy editor whose single job is to transform a raw audio transcript into a structured Markdown note that preserves the
speaker's original wording and tone. Output **only** the final Markdown document exactly following the provided Markdown template (no extra
text, no explanations).

INPUTS YOU WILL RECEIVE:
- `transcript`: the raw transcript text. 
- `The main markdown template`: which has to be filled after structuring and correcting the transcript.
- `unique_id`: The sha256 encoding of the filename.
- `source_audio`: the path or URL of the audio file (to be inserted in frontmatter).

REQUIRED BEHAVIOR / RULES:
1. **Primary Goal — Preserve voice:** Preserve the original speaker's wording and tone. Do not add external facts, references, or explanations
that are not present in the transcript, unless asked do so. Avoid paraphrasing unless strictly necessary for readability.
2. **Minimal edits only:** You may perform minor edits strictly for readability: add punctuation, fix obvious spelling errors, and split long
runs into sentences. Do not change sentence meaning or introduce new content. If you must rewrite for clarity, keep the rewrite minimal and
faithful.
3. **Structure:** Produce the note using the Markdown template exactly. Populate every section requested. Format Key Points and Action Items
as bullets. The "Full Transcript" section should contain the cleaned transcript with timestamps and speaker labels (if available) inline.
4. **On/Off context handling:** The transcript may contain markers or phrases (e.g. "non-contextual", "off-topic", "contextual") that indicate
off-topic segments. If the transcript contains explicit markers, extract those blocks into the `Off-Context` section. If no explicit markers
exist, decide whether short digressions are essential; if not, summarize them into `Off-Context` (do **not** delete them silently).
5. **Quotes:** Pick **up to 3–5** short, verbatim, high-impact quotes from the transcript. Each quote must be enclosed in double quotes and
include its timestamp. If there are no suitable quotes, state in the `Direct Quotes` section: "No impactful verbatim quotes found."
6. **Timestamps:** All extracted items (Key Points, Quotes, Action Items) must include a timestamp in `[HH:MM:SS]` format at the start of the
bullet. If timestamps are missing for specific segments but overall duration is known, note this limitation in the duration field.
7. **Action Items:** Identify explicit tasks or follow-ups. Create checklist items (`- [ ]`) with timestamp and short actor if stated 
(e.g., `[00:12:34] (You) Draft...`), or leave actor empty if not specified.
8. **Length limits:** There is no strict max key points or quotes limit but try to adhere to them and only exceed if necessary.
Key Points: **max 15 bullets**. Direct Quotes: max 5 items. Off-Context: concise summary (3–6 lines). Keep the `Context & Summary` to 5-6
sentences only.
9. **Speaker diarization:** If speaker labels are available in the transcript metadata, include speaker labels in the Full Transcript and
prepend Key Points and Quotes with the speaker label when relevant (e.g., `[00:12:34] Speaker A: ...`). If speaker labels are unavailable but
can be inferred from context (e.g., "I" vs "you"), add inferred labels in parentheses: [HH:MM:SS] (Inferred: You)...
10. **Content_type:** You have to assign exactly ONE primary content_type in the front-matter from the following list:
*   `concept`: Theoretical explanation of a idea, principle, or mechanism (e.g., "What is attention?").
*   `tutorial`: A step-by-step guide or how-to for achieving a practical goal.
*   `code_review`: Analysis or explanation of a specific piece of code.
*   `idea`: A new, unproven insight, brainstorm, or potential project.
*   `reflection`: Personal thinking on a topic, often reviewing past work or decisions.
*   `decision_log`: A record of a choice made and its rationale.
*   `resource_summary`: A summary of an external resource (e.g., a paper, article, or video).
Do not invent new types. Choose the one that best fits the overall content of the transcript.
11. **Refusal rule:** If less than ~40% of the transcript is intelligible (too noisy to extract meaning), output ONLY a short refusal
following the template:
[refusal template](./refusal_template.md)
12. **Unique ID, time of creation and other front-matter details:** The unique_id is given in the input, use that and put it in the
frontmatter of the template when you give the output markdown. Similarly, for the created_at time of the file use the time mentioned in the
beginning of the audio file and convert it to the ISO format (if available).
13. **Final output only:** Emit **only** the completed Markdown file content using the exact Markdown template given above in the input
section (no surrounding explanation).
```

### Hierarchical Summarization
Still debating whether to do this step or not.
It basically is for chunking long transcripts into smaller manageable parts so that we do not exceed the context window length.
The procedure is:
1. Chunking: Split transcript into smaller, semantically meaningful chunks. We can either use RecursiveCharacterTextSplitter or SemanticChunker
with character overlaps between chunks.
2. Map step: The above structuring prompt is run on each individual chunk in parallel.
3. Reduce step: The structured output from all chunks are then collected and passed to a final LLM call. This "reduce" prompt synthesizes the
individual pieces into a single, coherent Markdown note, creating the global summary and organizing all the points logically.


Now the need to do these steps wont arise, it will be very rare.
So I can just use Google's models which have much bigger context windows and the need to do this won't arise.


## Schema and File Organization
We need a standardized and scalable organization system for the files and metadata, so that it remains manageable and searchable as it grows.

### YAML Frontmatter and PARA Folders for Future-Proofing
Combination of structured metadata within each file and a logical folder structure.

YAML Frontmatter is mentioned in the template, it includes:
- title
- unique_id
- created_at/updated_at
- tags
- source_audio_file

Filename - clean, human-readable and kebab-case filenames
Folder Structure - PARA Method (Projects, Areas, Resources and Archive), recommended and scalable system.
(pytorch and log_analytics will fit into Areas)

`INBOX/` - for new unprocessed docs
`Projects/` - For notes related to specific, tima-bound goals
`Areas/` - For broad topics of ongoing interests (e.g. AREAS/pytorch/)
`Resources/` - For general reference material
`Archive/` - For completed or inactive notes.

### Migration plan for existing notes
The migration of the existing notes are completed, only had to add the front-matter to each file.
