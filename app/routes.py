from flask import Blueprint, render_template, request, jsonify
from app.model import load_model, classify_text

main = Blueprint('main', __name__)

# Load model when the Blueprint is created
try:
    model, tokenizer = load_model()
    print("Model loaded successfully in routes.py")
except Exception as e:
    print(f"Error loading model in routes.py: {e}")
    model, tokenizer = None, None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        text = request.form.get('text', '')
        
        if not text:
            return render_template('result.html', error="Please enter some text to classify.")
        
        if model is None or tokenizer is None:
            return render_template('result.html', error="Model could not be loaded. Please try again later.")
            
        # Classify the text
        result, human_prob, ai_prob = classify_text(text, model, tokenizer)
        
        # Extract the prediction and confidence
        prediction = result.get("prediction", "Error")
        confidence = result.get("confidence", 0)
        
        return render_template('result.html', 
                              text=text,
                              result=prediction,
                              confidence=confidence)

@main.route('/api/classify', methods=['POST'])
def api_classify():
    """API endpoint for text classification"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    if model is None or tokenizer is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    text = data['text']
    result, human_prob, ai_prob = classify_text(text, model, tokenizer)
    
    return jsonify({
        'text': text,
        'classification': result.get("prediction"),
        'confidence': result.get("confidence"),
        'probabilities': {
            'human': human_prob * 100,
            'ai': ai_prob * 100
        }
    })

# Add your debug endpoint here
@main.route('/debug', methods=['POST'])
def debug():
    """Debug endpoint to see raw model outputs"""
    text = request.form.get('text', '')
    if not text:
        return jsonify({"error": "Missing text"})
    
    if model is None or tokenizer is None:
        return jsonify({"error": "Model not loaded"}), 500
        
    # Get tokenized representation
    inputs = tokenizer(text, return_tensors="pt", truncation=True, 
                      max_length=512, padding=True)
    
    # Get raw logits
    import torch
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.tolist()[0]
    
    # Calculate probabilities
    import torch.nn.functional as F
    probs = F.softmax(torch.tensor(logits), dim=0).tolist()
    
    return jsonify({
        "text": text,
        "logits": logits,
        "probabilities": probs,
        "tokens": tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    })