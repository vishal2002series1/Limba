from pydantic import BaseModel
from typing import List, Optional
from openai import AzureOpenAI
import instructor
import os
from app.irah.connections.azure_openai import (AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT, advisor_copilot_client)

# Importing required classes from request_schema.py
from app.modules.chat.schema.request_schema import (
    CallSummary,
    Transcript,
    Email,
    CombinedQuestionRequest,
    ProcessNotesRequest
)

# Importing required classes from response_schema.py
from app.modules.chat.schema.response_schema import (
    ProcessNotesResponse,
    CombinedQuestionAnswer,
    CombinedSelector
)

MODEL = AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT
client = instructor.patch(advisor_copilot_client)

def get_relevant_ids(client: AzureOpenAI, question: str, summaries: List[CallSummary], emails: List[Email]) -> CombinedSelector:
    summaries_text = "\n".join([f"Transcript ID: {s.id}, Summary: {s.summary}" for s in summaries])
    email_info = "\n".join([f"Email ID: {e.id}, Subject: {e.subject}" for e in emails])
    
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant helping to identify relevant call transcripts and emails based on a given question."},
            {"role": "user", "content": f"""
            Given the following question, list of call summaries, and list of emails, identify which transcript IDs and email IDs are most likely to contain information relevant to answering the question.

            Question: {question}

            Call Summaries:
            {summaries_text}

            Emails:
            {email_info}

            Provide your reasoning and separate lists of relevant transcript IDs and email IDs.
            """}
        ],
        response_model=CombinedSelector
    )

def analyze_content_and_answer(client: AzureOpenAI, question: str, relevant_summaries: List[CallSummary], relevant_transcripts: List[Transcript], relevant_emails: List[Email]) -> CombinedQuestionAnswer:
    transcripts_info = "\n".join([
        f"Transcript ID: {t.id}\nSummary: {s.summary}\nTranscript: {t.transcript}"
        for s, t in zip(relevant_summaries, relevant_transcripts)
    ])
    emails_info = "\n".join([
        f"Email ID: {e.id}\nSubject: {e.subject}\nBody: {e.body}"
        for e in relevant_emails
    ])
    
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant tasked with analyzing call transcripts and emails to briefly answer a question based on the information provided."},
            {"role": "user", "content": f"""
            Analyze the following call transcripts and emails to answer the question based on the information provided:

            Question: {question}

            Transcripts:
            {transcripts_info}

            Emails:
            {emails_info}

            1. For each transcript and email, identify the relevant sentences that help answer the question. Each sentence must be an exact quote from the source.
            2. Provide a concise answer to the question based on the relevant information from all sources.
            3. List the relevant transcripts and emails with their IDs, summaries/subjects, and the relevant sentences you identified.

            Format your response as a JSON object with the following structure:
            {{
                "answer": "Your concise answer to the question",
                "relevant_transcripts": [
                    {{
                        "transcript_id": transcript_id,
                        "summary": "Summary of the transcript",
                        "relevant_sentences": ["Relevant sentence 1", "Relevant sentence 2", ...]
                    }},
                    ...
                ],
                "relevant_emails": [
                    {{
                        "email_id": email_id,
                        "subject": "Subject of the email",
                        "relevant_sentences": ["Relevant sentence 1", "Relevant sentence 2", ...]
                    }},
                    ...
                ]
            }}
            """}
        ],
        response_model=CombinedQuestionAnswer,
    )

def process_question(req: CombinedQuestionRequest) -> CombinedQuestionAnswer:
    selector = get_relevant_ids(client, req.question, req.summaries, req.emails)
    relevant_summaries = [s for s in req.summaries if s.id in selector.relevant_transcript_ids]
    relevant_transcripts = [t for t in req.transcripts if t.id in selector.relevant_transcript_ids]
    relevant_emails = [e for e in req.emails if e.id in selector.relevant_email_ids]
    final_answer = analyze_content_and_answer(client, req.question, relevant_summaries, relevant_transcripts, relevant_emails)
    return final_answer

def process_notes(req: ProcessNotesRequest) -> ProcessNotesResponse:
    pinned_items_text = "\n".join([
        f"ID: {item.id}\nType: {item.type}\nSource: {item.source}\nTitle: {item.title}\nGroup: {item.group}\nContent: {item.content}"
        for item in req.pinnedItems
    ])
    
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant tasked with analyzing pinned items, notes, and prompt instructions to generate a summary."},
            {"role": "user", "content": f"""
            Analyze the following information and generate a summary based on the provided data and instructions:

            Pinned Items:
            {pinned_items_text}

            Notes:
            {req.notes}

            Prompt Instructions:
            {req.promptInstructions}

            Generate a concise summary based on the above information, following the prompt instructions.
            """}
        ],
        response_model=ProcessNotesResponse
    )

