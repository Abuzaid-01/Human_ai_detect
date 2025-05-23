# AI Text Classifier

An application that classifies text as human-written or AI-generated using a fine-tuned RoBERTa model.

## Features

- Analyze text to determine if it was written by a human or AI
- Displays confidence scores and probabilities
- User-friendly web interface
- API endpoint for integration with other services

## Tech Stack

- Python/Flask: Backend web framework
- HuggingFace Transformers: ML model management
- PyTorch: Deep learning framework
- HTML/CSS/JavaScript: Frontend interface

## Model

The model is hosted on [Hugging Face](https://huggingface.co/Abuzaid01/Ai_Human_text_detect) and is loaded directly from there during application startup.

## Deployment

This application is designed to be deployed on Render.com.

### Local Development

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`

### Production Deployment

Follow the instructions in DEPLOYMENT.md to deploy on Render.