from typing import List
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from llmrag.models.base_model import BaseModel
from langchain_core.documents import Document
import torch

class TransformersModel(BaseModel):
    """
    Text generation model using Hugging Face Transformers.
    
    STUDENT EXPLANATION:
    This class wraps HuggingFace models for text generation. It's designed to work
    with RAG systems by taking context documents and generating answers based on them.
    
    The key improvement here is the climate science-specific prompt that helps the
    model understand it's dealing with scientific IPCC reports and should provide
    accurate, well-sourced answers.

    Args:
        model_name (str): The name of the pretrained model to load.
        device (str): Device to run the model on ('cpu' or 'cuda').

    Methods:
        generate(prompt: str, temperature: float) -> str:
            Generates text from a given prompt.
        generate(query: str, documents: List[Document]) -> str:
            Generates text from a query and context documents.
    """

    def __init__(self, model_name="gpt2-large", device="cpu"):
        """
        Initialize the Transformers model.
        
        STUDENT NOTE:
        We're now using gpt2-large by default (774M parameters) which should give
        much better answers than the smaller gpt2 model. This model is still
        manageable on CPU with 32GB RAM.
        """
        self.model_name = model_name
        self.device = device
        
        # Handle device mapping for different platforms
        if device == "mps":
            # Apple Silicon GPU
            device_id = "mps"
            self.torch_device = torch.device("mps")
        elif device == "cuda":
            # NVIDIA GPU
            device_id = 0
            self.torch_device = torch.device("cuda")
        else:
            # CPU
            device_id = -1
            self.torch_device = torch.device("cpu")
        
        # Use pipeline for simpler models, direct loading for larger ones
        if "gpt2" in model_name and "large" in model_name:
            # For larger models, load directly for better control
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Move model to appropriate device
            if device in ["mps", "cuda"]:
                self.model = self.model.to(self.torch_device)
            
            self.use_pipeline = False
        else:
            # Use pipeline for smaller models
            self.generator = pipeline("text-generation", model=model_name, device=device_id)
            self.use_pipeline = True

    def generate(self, prompt_or_query: str, temperature: float = 0.7, documents: List[Document] = None) -> str:
        """
        Generate text from a prompt or query with optional context documents.
        
        STUDENT EXPLANATION:
        This method creates a climate science-specific prompt that helps the model
        understand it's dealing with IPCC reports and should provide accurate,
        well-sourced answers. The prompt includes:
        
        1. Role definition (climate science expert)
        2. Context about IPCC reports
        3. Instructions for source-based answers
        4. Clear formatting for the response
        
        Args:
            prompt_or_query (str): The prompt or query to generate from
            temperature (float): Sampling temperature for generation
            documents (List[Document], optional): Context documents for RAG-style generation
            
        Returns:
            str: The generated text
        """
        if documents is not None:
            # RAG-style generation with climate science context
            context = "\n\n".join(doc.page_content for doc in documents)
            
            # Improved climate science prompt
            prompt = f"""You are a climate science expert analyzing IPCC (Intergovernmental Panel on Climate Change) reports. 
Your task is to provide accurate, evidence-based answers using ONLY the provided context from IPCC chapters.

IMPORTANT GUIDELINES:
- Base your answer ONLY on the provided context
- Be precise and scientific in your language
- If the context doesn't contain enough information, say "Based on the provided context, I cannot provide a complete answer"
- Cite specific findings and data when available
- Use technical terminology appropriate for climate science

CONTEXT FROM IPCC REPORT:
{context}

QUESTION: {prompt_or_query}

ANSWER:"""
        else:
            # Direct prompt generation
            prompt = prompt_or_query

        if self.use_pipeline:
            # Use pipeline for smaller models with safer parameters
            try:
                response = self.generator(
                    prompt, 
                    max_new_tokens=150,  # Reduced for stability
                    temperature=min(temperature, 0.8),  # Cap temperature
                    pad_token_id=50256,
                    do_sample=True,
                    top_p=0.85,  # Slightly more conservative
                    repetition_penalty=1.05,  # Reduced penalty
                    num_return_sequences=1
                )
                return response[0]["generated_text"]
            except RuntimeError as e:
                if "probability tensor" in str(e):
                    # Fallback to more conservative parameters
                    response = self.generator(
                        prompt,
                        max_new_tokens=50,
                        temperature=0.5,
                        do_sample=False,  # Use greedy decoding
                        pad_token_id=50256
                    )
                    return response[0]["generated_text"]
                else:
                    raise e
        else:
            # Direct generation for larger models
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            
            # Move inputs to the same device as the model
            if hasattr(self, 'torch_device'):
                inputs = inputs.to(self.torch_device)
                # Ensure inputs are the right dtype for MPS
                if self.device == "mps":
                    inputs = inputs.to(torch.int64)
            
            # Create attention mask
            attention_mask = torch.ones_like(inputs)
            
            with torch.no_grad():
                try:
                    outputs = self.model.generate(
                        inputs,
                        attention_mask=attention_mask,
                        max_new_tokens=150,  # Reduced for stability
                        temperature=min(temperature, 0.8),  # Cap temperature
                        do_sample=True,
                        top_p=0.85,  # More conservative
                        repetition_penalty=1.05,  # Reduced penalty
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                except RuntimeError as e:
                    if "probability tensor" in str(e):
                        # Fallback to greedy decoding
                        outputs = self.model.generate(
                            inputs,
                            attention_mask=attention_mask,
                            max_new_tokens=50,
                            do_sample=False,  # Greedy decoding
                            pad_token_id=self.tokenizer.eos_token_id,
                            eos_token_id=self.tokenizer.eos_token_id
                        )
                    else:
                        raise e
            
            # Decode and return only the new tokens
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the original prompt
            return generated_text[len(prompt):].strip()
