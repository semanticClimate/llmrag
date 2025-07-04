#!/usr/bin/env python3
"""
Analysis script for RAG results
"""

import re
from llmrag.chapter_rag import ask_chapter

def clean_answer(raw_output):
    """
    Clean the raw model output to extract just the answer.
    """
    # Look for the answer after "Answer:" or "ANSWER:"
    answer_match = re.search(r'(?:Answer|ANSWER):\s*(.*)', raw_output, re.DOTALL | re.IGNORECASE)
    if answer_match:
        return answer_match.group(1).strip()
    
    # If no clear answer marker, try to extract after the last "Question:"
    parts = raw_output.split("Question:")
    if len(parts) > 1:
        last_part = parts[-1]
        # Remove the question and get what comes after
        if "Answer:" in last_part:
            answer_part = last_part.split("Answer:")[-1]
            return answer_part.strip()
    
    # Fallback: return everything after the last prompt instruction
    return raw_output

def analyze_chapter_query(question, chapter="wg1/chapter04", user_id="analysis_user"):
    """
    Analyze a query and return clean results.
    """
    print(f"🔍 Analyzing: {question}")
    print(f"📖 Chapter: {chapter}")
    print("=" * 60)
    
    try:
        # Get the raw result
        result = ask_chapter(
            question=question,
            chapter_name=chapter,
            user_id=user_id,
            model_name="distilgpt2",
            device="cpu"
        )
        
        # Extract clean answer
        clean_response = clean_answer(result['answer'])
        
        print("📝 Clean Answer:")
        print(clean_response)
        print()
        
        print("📄 Sources:")
        if result.get('paragraph_ids'):
            for i, pid in enumerate(result['paragraph_ids'][:5], 1):
                print(f"  {i}. {pid}")
            if len(result['paragraph_ids']) > 5:
                print(f"  ... and {len(result['paragraph_ids']) - 5} more")
        print()
        
        print("🔍 Context Analysis:")
        if result.get('context'):
            print(f"Retrieved {len(result['context'])} document chunks")
            for i, doc in enumerate(result['context'][:2], 1):
                print(f"\nChunk {i} (first 200 chars):")
                print(doc.page_content[:200] + "...")
        print()
        
        return {
            'question': question,
            'clean_answer': clean_response,
            'sources': result.get('paragraph_ids', []),
            'context_count': len(result.get('context', []))
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Test questions
    questions = [
        "What are SSP scenarios?",
        "What are the main temperature projections for 2100?",
        "What are the key findings about future climate change?",
        "What is the Executive Summary about?"
    ]
    
    print("🚀 IPCC Chapter 4 Analysis")
    print("=" * 60)
    
    results = []
    for question in questions:
        result = analyze_chapter_query(question)
        if result:
            results.append(result)
        print("-" * 60)
    
    print("\n📊 Summary:")
    print(f"Successfully analyzed {len(results)} questions")
    for result in results:
        print(f"• {result['question'][:50]}... - {len(result['clean_answer'])} chars") 