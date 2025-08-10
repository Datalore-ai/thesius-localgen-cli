<div align="center">
  <img src="./assets/logo.png" alt="Datalore.ai" />
</div>
<br/>
<br/>
<div align="center">
  <img src="./assets/local_file_dataset.gif" alt="Deep Research Demo" />
</div>


## Overview

Datalore is a terminal tool for generating structured datasets from local files like PDFs, Word docs, images, and text. You upload a file and describe the kind of dataset you want. It extracts the content, uses semantic search to understand and gather relevant context, applies your instructions through a generated schema, and outputs clean, structured data. Perfect for converting raw or unstructured local documents into ready-to-use datasets for training, analysis, or experimentation, all without manual formatting.


## How It Works

- give the path to a local file resource (PDF, DOCX, JPG, TXT, etc.)  
- extracts text from the uploaded document  
- splits the content page-wise into smaller chunks  
- randomly selects a chunk to use as a reference  
- runs a semantic similarity search using Qdrant to find related chunks  
- gathers similar chunks to build a context window  
- formats the gathered context cleanly  
- generates structured data using an instruction query and generated schema  
- evolves and improves the dataset iteratively  
- combines generated samples into a complete dataset  
- exports the final dataset in CSV or JSON format via the terminal  



## Workflow

This diagram shows how Datalore takes a local file and an instruction, extracts and understands the content, and turns it into a structured dataset.

![Deep Research Workflow](./assets/Local_File.png)



## Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create a Virtual Environment

Use `uv` to create a virtual environment:

```bash
uv venv
```

### 3. Activate the Virtual Environment

Activate the environment depending on your OS:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

Install required packages using:

```bash
uv pip install -r requirements.txt
```

### 5. Set Up Docker

Make sure you have Docker and Docker Compose installed. Then start the required services (e.g., Qdrant) using:

```bash
docker-compose up --build
```

This will spin up the necessary services in the background.

### 6. Run the Application

Once the environment and services are ready, start the application:

```bash
python main.py
```

You're all set to go! The app will now guide you through the workflow step by step.

## Authors

- [Swaraj Biswal](https://github.com/swarajbiswal)
- [Swadhin Biswal](https://github.com/swadhinbiswal)  


## Contributing

If something here could be improved, please open an issue or submit a pull request.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

