## KnowledgeRAG

A minimal, educational Retrieval-Augmented Generation (RAG) project showcasing a multimodal ingestion pipeline (focused on PDF sources), ElasticSearch-based retrieval (keyword + vector with RRF fusion), query rewriting (coreference, fusion, decomposition), neural re-ranking, lightweight context aggregation, and a simple chat loop for answering queries.


### Features
- **Multimodal ingestion (PDF-first)**: extract text, tables, and images from PDFs into normalized chunks
- **Vector + keyword retrieval**: ElasticSearch index and search via both modes, fused with Reciprocal Rank Fusion (RRF)
- **Query rewrite**: coreference resolution, fusion, and decomposition for better retrieval coverage
- **Neural re-rank**: reorder candidates using a neural model interface
- **Context aggregation**: build concise context from top hits
- **Chat**: a minimal conversational loop with short-term memory


### Repo layout (high level)
- `information/`
  - `source/pdf.py`: PDF ingestion to produce typed chunks (text/table/image)
  - `module/{text,table,image}.py`: modality-specific processors
  - `processor.py`: orchestrates loading files, running processors, batching chunks
  - `embedder.py`: text embedding interface
- `elastic_search/`
  - `es_client.py`: thin ElasticSearch client wrapper
  - `basic.py`, `query.py`: index management, read/write, query helpers
- `retrieval_augment/`
  - `rewrite/{coref_resolve.py,decomp.py,fusion.py}`: query rewriting
  - `query/{es_query.py,web_query.py}`: retrieval from ES and web
  - `rerank/neural.py`: neural re-ranking interface
  - `context/aggregate.py`: build final context string
  - `answer/chat.py`: chat component with short-term memory
  - `rag_client.py`: end-to-end RAG pipeline
- `utils/`: helpers (text formatting, embedding, etc.)
- `main.py`: runnable examples and tests for each stage
- `data/`: sample PDFs and extracted images


## Architecture

```
[Data Sources]
   │
   ▼
InformationProcessor
  - Detect type (pdf)
  - PDFProcessor → modality modules (text/table/image)
  - Chunk + metadata emitters
   │
   ▼
Embeddings → ElasticSearch Index (write_data)
   │                                 ▲
   │                                 │
   └────────────── Retrieval ────────┘
                     │
                     ▼
              ESQuery (keyword + vector)
                + WebQuery (optional)
                     │
                     ▼
                 RRF Fusion
                     │
                     ▼
             Neural Re-ranker
                     │
                     ▼
             Context Aggregation
                     │
                     ▼
                   Answer
                     │
                     ▼
                    Chat
```


## General logic (end-to-end)

1. Ingestion & Indexing
   - Use `InformationProcessor` to load input files and dispatch to modality processors.
   - Extract text/table/image chunks with metadata.
   - Generate embeddings for text chunks via `information/embedder.py`.
   - Write `{text, vector, metadata}` documents into ElasticSearch via `ElasticSearchClient`.

2. Query Rewrite
   - `CoreferenceResolution`: resolves references using recent chat history.
   - `QueryFusion`: produces diverse rewrites of the query.
   - `QueryDecomposition`: decomposes complex questions into sub-queries.

3. Retrieval
   - `ESQuery`: runs keyword and vector searches over the same index.
   - Results are fused by RRF to balance lexical and semantic matches.
   - Optionally `WebQuery` augments with external results.

4. Re-ranking
   - `NeuralReranker` reorders candidates to surface the most relevant passages.

5. Context Aggregation
   - `Aggregate` builds a concise context from the top-N reranked hits.

6. Answering & Chat
   - `Chat` produces an answer (and maintains lightweight history).
   - `RAGClient.rag_chat()` provides an interactive CLI loop.


## Setup

### Prerequisites
- Python 3.11+
- ElasticSearch instance (local Docker or managed)
- Create `.env.development` with ES credentials

Example `.env.development` variables:
```bash
ELASTIC_URL=http://localhost:9200
ELASTIC_USERNAME=elastic
ELASTIC_PASSWORD=changeme
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Ensure ElasticSearch is running and reachable using the credentials above.


## Quickstart

1) Index sample data (PDFs):
- Place PDFs under `data/pdf/` (already includes samples)
- In `main.py`, un-comment `test_processor()` to ingest and index

```bash
python main.py
```

2) Try basic retrieval:
- In `main.py`, un-comment `test_search()` to run a vector search

3) Run the full RAG chat loop:
- Leave `test_rag_chat()` enabled in `main.py`

```bash
python main.py
# type your queries, type "exit" to quit
```


## Key components (by role)
- `InformationProcessor`: detects source type, runs processors, yields chunks/batches
- `PDFProcessor`: extracts text/table/image from PDFs
- `TextEmbedder`: converts chunks to vectors for ES documents
- `ElasticSearchClient`: create/delete index, write docs, submit queries
- `ESQuery`: keyword + vector search, RRF fusion
- `NeuralReranker`: semantic reranking of candidates
- `Aggregate`: merges top candidates into final context
- `Chat`: answers using the augmented context and maintains history
- `RAGClient`: orchestrates rewrite → retrieve → rerank → aggregate → answer → chat


## Notable flows in code
- Ingestion & indexing example: see `main.py:test_processor()` and `information/processor.py`
- RAG pipeline: see `retrieval_augment/rag_client.py`
- ES retrieval & fusion: see `retrieval_augment/query/es_query.py`


## Notes
- The repo includes sample PDFs in `data/pdf/` and images in `data/image/`.
- The `WebQuery` and `NeuralReranker` provide extension points; plug in your preferred providers/models.
- For production, consider persistent chat memory, robust prompt/LLM integration, and telemetry.
