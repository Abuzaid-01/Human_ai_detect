import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_model():
    """
    Load the RoBERTa model for sequence classification from Hugging Face
    """
    try:
        # Your Hugging Face model ID
        hf_model_id = "Abuzaid01/Ai_Human_text_detect" 
        
        print(f"Loading model from Hugging Face: {hf_model_id}")
        
        # Load tokenizer and model directly from Hugging Face
        tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
        model = AutoModelForSequenceClassification.from_pretrained(hf_model_id)
        
        # Set model to evaluation mode
        model.eval()
        
        print("Model and tokenizer loaded successfully from Hugging Face")
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model from Hugging Face: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback to a public model
        print("Attempting to load fallback model...")
        try:
            tokenizer = AutoTokenizer.from_pretrained("roberta-base")
            model = AutoModelForSequenceClassification.from_pretrained(
                "roberta-base",
                num_labels=2
            )
            print("Fallback model loaded successfully")
            return model, tokenizer
        except Exception as e2:
            print(f"Error loading fallback model: {e2}")
            return None, None

def classify_text(text, model, tokenizer, human_bias=0.15):
    """
    Classify text as human-written or AI-generated with a calibration bias
    to fix the model's tendency to over-predict AI-generated text
    
    Args:
        text (str): The text to classify
        model: The loaded model
        tokenizer: The loaded tokenizer
        human_bias: Bias factor to add to human prediction score
        
    Returns:
        tuple: (result_dict, human_probability, ai_probability)
    """
    # Check inputs
    if not text or model is None or tokenizer is None:
        return {"prediction": "Error", "confidence": 0}, 0.0, 0.0
        
    # Ensure text is properly formatted
    text = text.strip()
    if not text:
        return {"prediction": "Error", "confidence": 0}, 0.0, 0.0
    
    # Tokenize and prepare for model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, 
                      max_length=512, padding=True)
    
    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    # Calculate probabilities with calibration
    raw_probs = torch.nn.functional.softmax(logits, dim=1)[0]
    
    # Apply bias correction toward human prediction
    human_prob = min(1.0, raw_probs[0].item() + human_bias)
    ai_prob = raw_probs[1].item()
    
    # Renormalize
    total = human_prob + ai_prob
    human_prob = human_prob / total
    ai_prob = ai_prob / total
    
    # Determine prediction with confidence
    if human_prob > ai_prob:
        result = {"prediction": "Human-written", "confidence": human_prob * 100}
    else:
        result = {"prediction": "AI-generated", "confidence": ai_prob * 100}
    
    return result, human_prob, ai_prob