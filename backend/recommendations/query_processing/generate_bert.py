# Import necessary libraries
from transformers import BertTokenizer, BertModel
import torch

def generate_cls_embedding(tokens):
    """
    Takes a list of tokens, adds [CLS] and [SEP], converts to token IDs,
    creates attention masks, passes through BERT, and returns the [CLS] embedding.
    
    Args:
        tokens (list): List of string tokens.
        
    Returns:
        numpy.ndarray: [CLS] embedding vector.
    """
    # Initialize the BERT tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    model.eval()  # Set model to evaluation mode

    # Add [CLS] and [SEP] tokens
    tokens = ["[CLS]"] + tokens + ["[SEP]"]
    print("Tokens with special tokens:", tokens)

    # Convert tokens to token IDs
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    print("Token IDs:", token_ids)

    # Create attention masks (1 for real tokens, 0 for padding)
    attention_masks = [1] * len(token_ids)
    print("Attention Masks:", attention_masks)

    # Convert inputs to PyTorch tensors
    input_ids = torch.tensor([token_ids])           # Shape: [1, sequence_length]
    attention_masks = torch.tensor([attention_masks])  # Shape: [1, sequence_length]

    # Disable gradient computation for inference
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
    
    # Extract the last hidden states
    last_hidden_states = outputs.last_hidden_state  # Shape: [1, sequence_length, hidden_size]

    # Extract the [CLS] embedding
    cls_embedding = last_hidden_states[:, 0, :]    # Shape: [1, hidden_size]
    
    # Convert to numpy array
    cls_embedding = cls_embedding.numpy()
    print("CLS Embedding Vector (First 10 Dimensions):", cls_embedding[0][:10])

    return cls_embedding

if __name__ == "__main__":
    # Example tokens
    # tokens = ["dataset", "containing", "customer", "reviews", "analyzing", 
    #           "delivery", "speed", "product", "quality", "ecommerce", "orders"]
    tokens = ["dataset"]
    
    # Generate [CLS] embedding
    cls_vec = generate_cls_embedding(tokens)
