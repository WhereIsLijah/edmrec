# Import necessary libraries
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

def generate_cls_embedding(tokens, make_positive=False, method='relu'):
    """
    Takes a list of tokens, adds [CLS] and [SEP], converts to token IDs,
    creates attention masks, passes through BERT, and returns the [CLS] embedding.
    Optionally transforms the embedding to be positive.
    
    Args:
        tokens (list): List of string tokens.
        make_positive (bool): Whether to make the embedding vector positive.
        method (str): Method to make the vector positive ('relu', 'abs', 'min_max', 'add_constant').
        
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
    input_ids = torch.tensor([token_ids])                # Shape: [1, sequence_length]
    attention_masks = torch.tensor([attention_masks])    # Shape: [1, sequence_length]

    # Disable gradient computation for inference
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
    
    # Extract the last hidden states
    last_hidden_states = outputs.last_hidden_state       # Shape: [1, sequence_length, hidden_size]

    # Extract the [CLS] embedding
    cls_embedding = last_hidden_states[:, 0, :]         # Shape: [1, hidden_size]
    
    # Convert to NumPy array
    cls_embedding = cls_embedding.numpy()[0]             # Shape: [hidden_size]
    # print("CLS Embedding Vector (First 10 Dimensions):", cls_embedding[:10])

    # Transform the embedding to be positive if required
    if make_positive:
        if method == 'relu':
            cls_embedding = np.maximum(cls_embedding, 0)
            print("Applied ReLU: Set all negative values to 0.")
        elif method == 'abs':
            cls_embedding = np.abs(cls_embedding)
            print("Applied Absolute Value: Converted all values to positive.")
        elif method == 'min_max':
            min_val = cls_embedding.min()
            cls_embedding = cls_embedding - min_val
            max_val = cls_embedding.max()
            if max_val != 0:
                cls_embedding = cls_embedding / max_val
            print("Applied Min-Max Scaling: Scaled values to [0, 1].")
        elif method == 'add_constant':
            min_val = cls_embedding.min()
            if min_val < 0:
                cls_embedding = cls_embedding + abs(min_val)
                print(f"Added constant {abs(min_val):.3f}: Shifted all values to be positive.")
            else:
                print("No constant addition needed: All values are already positive.")
        else:
            print(f"Unknown method '{method}'. No transformation applied.")
    
    print("CLS Embedding Vector (First 10 Dimensions after Transformation):", cls_embedding[:15])

    return cls_embedding

if __name__ == "__main__":
    # Example tokens
    # tokens = ["dataset", "containing", "customer", "reviews", "analyzing", 
    #           "delivery", "speed", "product", "quality", "ecommerce", "orders"]
    tokens = ["dataset"]
    
    # Generate [CLS] embedding without transformation
    # print("----- Without Making Embedding Positive -----")
    # cls_vec = generate_cls_embedding(tokens, make_positive=False)
    
    print("\n----- With Making Embedding Positive using ReLU -----")
    # Generate [CLS] embedding and make it positive using ReLU
    cls_vec_positive = generate_cls_embedding(tokens, make_positive=True, method='relu')
