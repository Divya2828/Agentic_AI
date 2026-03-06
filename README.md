# Agentic AI RAG Q&A Agent

A Streamlit-based application that leverages Retrieval-Augmented Generation (RAG) and AI agents to enable intelligent question-answering and business planning from PDF documents.

## Features

- **PDF Document Processing**: Upload and process PDF files for content extraction
- **Q&A Chat**: Ask questions about your uploaded documents and get accurate, context-aware answers with page citations
- **Business Model Generation**: Use AI agents to generate detailed business plans and use cases based on document content
- **Vector Search**: FAISS-powered semantic search for fast document retrieval
- **Multi-Model Support**: Compatible with OpenRouter API for flexible LLM selection

## Project Structure

```
├── app_new.py          # Main Streamlit application
├── rag.py              # RAG pipeline (PDF processing, vectorstore, QA)
├── agent.py            # AI agent for business model generation
├── prompt.py           # Custom prompts for QA and agent
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Requirements

- Python 3.7+
- PDF files for processing
- OpenAI API key (configured for OpenRouter)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=<your-openrouter-api-key>
   OPENAI_API_BASE=https://openrouter.ai/api/v1
   EMBEDDING_MODEL=<embedding-model-name>
   CHAT_MODEL=<chat-model-name>
   ```

## Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run app_new.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Q&A Chat Mode

1. Upload a PDF file using the file uploader
2. Type your question about the document
3. The AI will search through the document and provide answers with page citations

### Business Model Generator Mode

1. Upload a PDF file
2. The AI agent will analyze the document and generate:
   - Detailed business plan
   - Implementation strategies
   - Relevant use cases

## Key Dependencies

- **LangChain**: LLM orchestration and RAG pipeline
- **Streamlit**: Web UI framework
- **FAISS**: Vector similarity search
- **OpenAI**: Embeddings and language models via OpenRouter
- **PyPDF**: PDF text extraction

## Configuration

Key environment variables:
- `OPENAI_API_KEY`: Your OpenRouter API key
- `OPENAI_API_BASE`: OpenRouter API endpoint (default: `https://openrouter.ai/api/v1`)
- `EMBEDDING_MODEL`: Model for text embeddings (e.g., OpenAI's embedding model)
- `CHAT_MODEL`: Model for chat responses (e.g., `mistralai/mistral-7b-instruct`)

## API Integration

This project uses **OpenRouter** as the LLM provider, allowing flexibility in model selection. To use different models:

1. Get an API key from [OpenRouter](https://openrouter.ai)
2. Set the `OPENAI_API_KEY` environment variable
3. Adjust `CHAT_MODEL` and `EMBEDDING_MODEL` as needed

## Technical Details

### RAG Pipeline

The RAG system works as follows:

1. **PDF Ingestion**: Extracts text from uploaded PDFs
2. **Text Chunking**: Splits text into manageable chunks (800 chars with 100 char overlap)
3. **Embedding**: Converts chunks to vector embeddings using OpenAI Embeddings
4. **Vectorstore**: Stores embeddings in FAISS for fast retrieval
5. **QA**: Retrieves relevant chunks and generates answers using context

### Prompting Strategy

- **QA Prompt**: Enforces context-only answers with page citations
- **Agent Prompt**: Directs AI to generate comprehensive business plans and use cases

## Troubleshooting

### API Key Error
Ensure `OPENAI_API_KEY` is set in your `.env` file and the key is valid.

### PDF Processing Issues
- Check that the PDF file is not corrupted
- Ensure sufficient disk space for temporary files
- Verify PDF contains extractable text

### Vector Search Issues
- Verify the `EMBEDDING_MODEL` is correctly configured
- Check API connection to OpenRouter

