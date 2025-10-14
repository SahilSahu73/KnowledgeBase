from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os
from datetime import datetime
from typing import Optional, Dict

from logger_config import logger
from llm_factory import LLMFactory


class AudioTranscriptProcessor:
    def __init__(self, llm_provider: str = "groq", llm_model: str = "llama-3.3-70b-versatile",
                 max_tokens: int = 8000, **llm_kwargs):
        """
        Initialize the audio transcript processor with flexible LLM provider.

        Args:
            llm_provider: LLM provider to use - (openai, groq, google, anthropic)
            llm_model: The specific model to use in the specific provider choosen
            max_tokens: Maximum tokens for LLM output.
            **llm_kwargs: additional arguments to pass to the LLM constructor.
        """
        self.provider = llm_provider
        self.model = llm_model
        logger.info(f"Initializing LLM provider: {llm_provider}, and model: {llm_model}")
        try:
            self.llm = LLMFactory.create_llm(
                provider=llm_provider,
                model=llm_model,
                max_tokens=max_tokens,
                **llm_kwargs
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_Size=8000,
            overlap=500,
            length_function=len
        )

    def load_system_prompt(self, prompt_path: str = "./templates/system_prompt.txt") -> str:
        """
        Load the system prompt from the text file in templates
        """
        logger.info(f"Loading system prompt from: {prompt_path}")
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                logger.info(f"Loaded system prompt with {len(content)} characters")
                return content
        except FileNotFoundError:
            logger.error(f"System prompt file not found at: {prompt_path}")
            raise
        except Exception as e:
            logger.error(f"Error in loading/reading the system prompt file: {str(e)}")
            raise

    def load_transcript(self, transcript_path: str) -> str:
        """
        Load the transcript from the text file generated after STT model API call.
        """
        logger.info(f"Loading Transcript from: {transcript_path}")
        try:
            # using standard file reading instead of a TextLoader for more control.
            encodings = ['utf-8', 'cp1252', 'latin-1']

            for encoding in encodings:
                try:
                    with open(transcript_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    logger.info(f"Successfully loaded transcript with {encoding} encoding.")
                    return content
                except UnicodeDecodeError:
                    continue

            # if all encoding fails
            raise UnicodeDecodeError(f"Failed to decode {transcript_path} with tried encodings: {encodings}")

        except Exception as e:
            logger.error(f"Error loading transcript: {str(e)}")
            raise

    def create_formatting_chain(self, system_prompt: str):
        """
        Create the formatting chain with the system prompt
        """
        logger.info("Creating formatting chain")

        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(
                "Please format the following audio transcript:\n"
                "TRANSCRIPT:\n"
                "{transcript}\n\n"
                "Remember to follow all formatting rules and requirements specified in the system prompt."
            )
        ])

        # Create the chain
        return prompt_template | self.llm | StrOutputParser()

    def process_transcript(self, transcript_path: str,
                           prompt_path: str,
                           output_path: Optional[str] = None,
                           metadata: Optional[Dict] = None) -> str:
        """
        Main method to process the transcript through the LLM formatting pipeline
        """
        logger.info(f"Starting transcript processing for: {transcript_path}")

        # Load system prompt
        system_prompt = self.load_system_prompt(prompt_path)

        # Enhance prompt with metadata if provided
        if metadata:
            metadata_str = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
            system_prompt = f"{system_prompt}\n\nADDITIONAL METADATA:\n{metadata_str}"
            logger.debug("Enhanced system prompt with metadata")

        # Load transcript
        transcript_content = self.load_transcript(transcript_path)
        logger.info(f"Transcript loaded with {len(transcript_content)} characters")

        # Create formatting chain
        formatting_chain = self.create_formatting_chain(system_prompt)

        # Process transcript
        logger.info("Processing transcript through LLM...")
        try:
            formatted_output = formatting_chain.invoke({
                "transcript": transcript_content
            })
            logger.info("Successfully processed transcript through LLM")

        except Exception as e:
            logger.error(f"Error during LLM processing: {str(e)}")

            # Handle context length issues by chunking
            if "context" in str(e).lower() and "length" in str(e).lower() or "too long" in str(e).lower():
                logger.info("Transcript too long, attempting chunked processing...")
                formatted_output = self._process_in_chunks(
                    transcript_content, system_prompt
                )
            else:
                raise

        # Save output if path provided
        if output_path:
            self._save_output(formatted_output, output_path)

        logger.info(f"Processing completed. Output length: {len(formatted_output)} characters")
        return formatted_output

    def _process_in_chunks(self, transcript: str, system_prompt: str) -> str:
        """
        Process very long transcripts in chunks
        """
        logger.info("Splitting transcript into chunks")

        # Split the transcript into manageable chunks
        chunks = self.text_splitter.split_text(transcript)
        all_formatted = []

        logger.info(f"Processing {len(chunks)} chunks...")

        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)} (size: {len(chunk)} chars)")

            formatting_chain = self.create_formatting_chain(system_prompt)
            formatted_chunk = formatting_chain.invoke({
                "transcript": chunk
            })
            all_formatted.append(formatted_chunk)

        # Combine results
        combined = "\n\n".join(all_formatted)
        logger.info(f"Combined {len(chunks)} chunks into {len(combined)} characters")
        return combined

    def _save_output(self, content: str, output_path: str):
        """
        Save the formatted output to a file
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Formatted output saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save output to {output_path}: {str(e)}")
            raise
