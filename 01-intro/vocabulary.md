# GenAI SME Vocabulary File

--- 

### **Generative AI**
* A category of artificial intelligence models that do not just classify or predict, but *create novel, new* content. This includes text (LLMs), images (Diffusion Models), code, and even complex data like 3D protein structures.

### **Black Box (Model)**
* A term for an AI model (especially deep learning ones) where we can't easily understand *why* it made a specific decision or produced a certain output. We can see the input and the output, but the internal logic is too complex to be human-readable. This is a major challenge for debugging and in high-stakes fields like medicine.

### **Fine-Tuning**
* The process of taking a large, pre-trained "base" model (like GPT-4) and retraining it (usually just a few layers) on a smaller, specific, proprietary dataset. This is done to make the model an expert in a specific *style*, *tone*, or *domain* (e.g., making it sound like your company's brand voice or understand specific legal jargon).

### **Hallucination**
* The primary failure state of generative AI. It's when the model confidently generates a response that is factually incorrect, nonsensical, or completely fabricated. It is *not* a bug, but a natural side effect of the model's probabilistic design (it's trying to predict the "next most likely word").

### **RAG (Retrieval-Augmented Generation)**
* The most common architectural pattern for building enterprise-ready GenAI apps. Instead of *just* relying on the model's static training, the system first *retrieves* relevant documents (from a vector database, for example) and then *augments* the user's prompt with this new information. This "grounds" the model in real-time, company-specific data.

