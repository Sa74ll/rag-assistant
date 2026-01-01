"""
Gemini File Search API Demo

Demonstrates the core workflow:
1. Create a file search store
2. Upload and index documents
3. Query documents using Gemini
4. Clean up resources
"""

from pathlib import Path
from google import genai


def create_store(
    client: genai.Client, display_name: str
) -> genai.types.FileSearchStore:
    """Create a file search store for organizing searchable documents."""
    store = client.file_search_stores.create(config={"display_name": display_name})
    print(f"Created store: {store.name}")
    return store


def upload_documents(client: genai.Client, store_name: str, docs_path: Path) -> None:
    """Upload all PDF documents from the specified directory to the store."""
    print("\nUploading documents...")
    for file_path in docs_path.glob("*.pdf"):
        file = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=store_name,
            config={"display_name": file_path.name},
        )
        print(f"Uploaded file: {file.name}")


def search(client: genai.Client, store_name: str, query: str) -> str:
    """Query the store using Gemini with file search."""
    print(f"\nSearching the store for: '{query}'...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={"tools": [{"file_search": {"file_search_store_names": [store_name]}}]},
    )
    print(f"\nAnswer:\n{response.text}")
    return response.text


def cleanup(client: genai.Client) -> None:
    """Delete all file search stores (force deletes documents and chunks too)."""
    print("\nCleaning up resources...")
    for store in client.file_search_stores.list():
        client.file_search_stores.delete(name=store.name, config={"force": True})
        print(f"Deleted store: {store.name}")
    print("Cleanup complete.")


if __name__ == "__main__":
    # Initialize client (requires GEMINI_API_KEY environment variable)
    client = genai.Client()

    # Step 1: Create a file search store
    store = create_store(client, "FAQ Store")

    # Step 2: Upload documents
    upload_documents(client, store.name, Path("docs"))

    # Step 3: Query the documents
    search(client, store.name, "How long does it take to ship to Canada?")

    # Step 4: Clean up all stores
    # cleanup(client)
