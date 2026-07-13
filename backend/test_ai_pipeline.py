import os
import shutil
import unittest
from PIL import Image
import numpy as np

# Set import path for testing
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.embeddings import pipeline

class TestAIPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create temp folder for test images
        cls.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_temp_images')
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Generate two distinct solid color dummy images
        cls.img_path1 = os.path.join(cls.test_dir, 'red_image.jpg')
        cls.img_path2 = os.path.join(cls.test_dir, 'blue_image.jpg')
        
        red_img = Image.new('RGB', (300, 300), color='red')
        red_img.save(cls.img_path1)
        
        blue_img = Image.new('RGB', (300, 300), color='blue')
        blue_img.save(cls.img_path2)

    @classmethod
    def tearDownClass(cls):
        # Clean up temp folder
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_embedding_dimensions(self):
        """Test that the embedding pipeline extracts a 1280-dimensional vector."""
        vec = pipeline.get_embedding(self.img_path1)
        self.assertIsNotNone(vec, "Embedding should not be None for a valid image.")
        self.assertEqual(len(vec), 1280, f"Expected 1280 dimensions, got {len(vec)}")
        self.assertTrue(all(isinstance(x, float) for x in vec), "Embedding values must be floats.")

    def test_embedding_determinism(self):
        """Test that running embedding extraction on the same image twice yields the identical vector."""
        vec1 = pipeline.get_embedding(self.img_path1)
        vec2 = pipeline.get_embedding(self.img_path1)
        
        self.assertIsNotNone(vec1)
        self.assertIsNotNone(vec2)
        self.assertEqual(vec1, vec2, "Embeddings of the exact same image must be identical.")

    def test_embedding_sensitivity(self):
        """Test that two different images yield distinct vectors (sanity check)."""
        vec_red = pipeline.get_embedding(self.img_path1)
        vec_blue = pipeline.get_embedding(self.img_path2)
        
        self.assertIsNotNone(vec_red)
        self.assertIsNotNone(vec_blue)
        
        # Check that they are not equal
        self.assertNotEqual(vec_red, vec_blue, "Embeddings of different images should be distinct.")
        
        # Calculate cosine similarity manually to check sensitivity
        v_r = np.array(vec_red)
        v_b = np.array(vec_blue)
        cos_sim = np.dot(v_r, v_b) / (np.linalg.norm(v_r) * np.linalg.norm(v_b))
        
        # They shouldn't be identical (sim < 0.999)
        print(f"Cosine Similarity between red and blue test images: {cos_sim:.4f}")
        self.assertTrue(cos_sim < 0.999, "Cosine similarity of distinct colors shouldn't be perfect.")

    def test_graceful_missing_file_handling(self):
        """Test that passing a non-existent file path returns None instead of raising an exception."""
        non_existent_path = os.path.join(self.test_dir, 'does_not_exist.jpg')
        vec = pipeline.get_embedding(non_existent_path)
        self.assertIsNone(vec, "Embedding must be None for non-existent image paths.")

if __name__ == '__main__':
    unittest.main()
