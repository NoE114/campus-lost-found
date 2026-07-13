import numpy as np
from models import db, LostItem, FoundItem, ItemEmbedding
from ai.metadata_matcher import (
    calculate_text_similarity,
    calculate_category_similarity,
    calculate_date_similarity
)

def calculate_cosine_similarity(vec1, vec2):
    """
    Computes normalized cosine similarity [0.0, 1.0] between two vectors.
    """
    if not vec1 or not vec2:
        return 0.0
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        dot_product = np.dot(v1, v2)
        sim = dot_product / (norm1 * norm2)
        # Scale to [0.0, 1.0]
        return float((sim + 1.0) / 2.0)
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return 0.0

def get_matches(item, item_type):
    """
    Finds and ranks matches for a given lost or found item.
    item_type must be either 'lost' or 'found'.
    Returns a list of dictionaries with matching item details and confidence percentage.
    """
    if item_type == 'lost':
        candidates = FoundItem.query.all()
        candidate_type = 'found'
        target_type = 'lost'
    elif item_type == 'found':
        candidates = LostItem.query.all()
        candidate_type = 'lost'
        target_type = 'found'
    else:
        raise ValueError("item_type must be either 'lost' or 'found'")

    # Retrieve target embedding
    target_emb = ItemEmbedding.query.filter_by(item_id=item.id, item_type=target_type).first()
    target_vector = target_emb.vector if target_emb else None
    target_date = target_emb.created_at if target_emb else None

    matches = []
    for candidate in candidates:
        # Retrieve candidate embedding
        candidate_emb = ItemEmbedding.query.filter_by(item_id=candidate.id, item_type=candidate_type).first()
        candidate_vector = candidate_emb.vector if candidate_emb else None
        candidate_date = candidate_emb.created_at if candidate_emb else None

        # 1. Image similarity
        has_image = target_vector is not None and candidate_vector is not None
        image_sim = 0.0
        if has_image:
            image_sim = calculate_cosine_similarity(target_vector, candidate_vector)

        # 2. Metadata similarities
        text_sim = calculate_text_similarity(item.item_name, candidate.item_name)
        category_sim = calculate_category_similarity(item.category, candidate.category)
        date_sim = calculate_date_similarity(target_date, candidate_date)

        # 3. Weighted scoring and dynamic weight adjustment (graceful degradation)
        if has_image:
            # Combined image + metadata matching weights
            w_image = 0.50
            w_text = 0.25
            w_category = 0.15
            w_date = 0.10
            
            confidence = (
                (image_sim * w_image) +
                (text_sim * w_text) +
                (category_sim * w_category) +
                (date_sim * w_date)
            )
        else:
            # Metadata-only matching weights (no images or AI model pipeline offline)
            w_text = 0.50
            w_category = 0.30
            w_date = 0.20
            
            confidence = (
                (text_sim * w_text) +
                (category_sim * w_category) +
                (date_sim * w_date)
            )

        confidence_pct = round(confidence * 100.0, 2)
        
        matches.append({
            "item": candidate.to_dict(),
            "confidence": confidence_pct,
            "match_details": {
                "has_image_match": has_image,
                "image_similarity": round(image_sim * 100.0, 2) if has_image else None,
                "text_similarity": round(text_sim * 100.0, 2),
                "category_similarity": round(category_sim * 100.0, 2),
                "date_similarity": round(date_sim * 100.0, 2)
            }
        })

    # Sort matches by confidence percentage descending
    matches.sort(key=lambda x: x["confidence"], reverse=True)
    return matches
