import os
from google import genai
from typing import Optional, List
from google.genai import types


class FileService:
    """Service for managing Gemini File Search operations."""

    def __init__(self, client: genai.Client, store_name: str):
        """
        Initialize the service with an existing File Search store.

        Args:
            client: The Gemini API client
            store_name: Name of the File Search store (e.g., 'fileSearchStores/abc123')
        """
        self.client = client
        self.store_name = store_name
        self._store = self.client.file_search_stores.get(name=self.store_name)

    def upload_file(
        self,
        file_path: str,
        display_name: Optional[str] = None,
        max_tokens_per_chunk: Optional[int] = None,
        max_overlap_tokens: Optional[int] = None,
        custom_metadata: Optional[List[dict]] = None,
    ) -> str:
        """
        Upload a file to the File Search store.

        Args:
            file_path: Path to the file to upload
            display_name: Display name for the file (defaults to filename)
            max_tokens_per_chunk: Maximum tokens per chunk for chunking strategy
            max_overlap_tokens: Maximum overlap tokens between chunks
            custom_metadata: List of metadata dicts with 'key' and 'string_value' or 'numeric_value'

        Returns:
            The operation name

        Example:
            >>> service.upload_file(
            ...     "docs/faq.pdf",
            ...     display_name="FAQ Document",
            ...     max_tokens_per_chunk=200,
            ...     max_overlap_tokens=20,
            ...     custom_metadata=[
            ...         {"key": "category", "string_value": "support"},
            ...         {"key": "version", "numeric_value": 2}
            ...     ]
            ... )
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use filename if display_name not provided
        if display_name is None:
            display_name = os.path.basename(file_path)

        # Build config
        config = {"display_name": display_name}

        # Add chunking config if specified
        if max_tokens_per_chunk or max_overlap_tokens:
            config["chunking_config"] = {
                "white_space_config": {
                    "max_tokens_per_chunk": max_tokens_per_chunk or 200,
                    "max_overlap_tokens": max_overlap_tokens or 20,
                }
            }

        # Add custom metadata if specified
        if custom_metadata:
            config["custom_metadata"] = custom_metadata

        # Upload to file search store
        self.client.file_search_stores.upload_to_file_search_store(
            file=file_path, file_search_store_name=self.store_name, config=config
        )

    def search(
        self,
        query: str,
        model: str = "gemini-2.5-flash",
        metadata_filter: Optional[str] = None,
    ) -> types.GenerateContentResponse:
        """
        Search the File Search store and generate a response.

        Args:
            query: The search query
            model: Model to use for generation
            metadata_filter: Optional filter expression (e.g., 'category="support"')

        Returns:
            The model's response with citations

        Example:
            >>> response = service.search(
            ...     "What are the payment options?",
            ...     metadata_filter='category="support"'
            ... )
            >>> print(response.text)
            >>> print(response.candidates[0].grounding_metadata)
        """
        # Build file search tool config
        file_search_config = types.FileSearch(file_search_store_names=[self.store_name])

        # Add metadata filter if provided
        if metadata_filter:
            file_search_config = types.FileSearch(
                file_search_store_names=[self.store_name],
                metadata_filter=metadata_filter,
            )

        # Generate content with file search
        response = self.client.models.generate_content(
            model=model,
            contents=query,
            config=types.GenerateContentConfig(
                tools=[types.Tool(file_search=file_search_config)]
            ),
        )

        return response
