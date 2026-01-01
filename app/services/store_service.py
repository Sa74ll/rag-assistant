from google import genai


class FileSearchStoreManager:
    """
    Manager for creating and managing File Search stores (setup operations).

    >>> manager = FileSearchStoreManager(client=genai.Client())
    """

    def __init__(self, client: genai.Client):
        """
        Initialize the store manager.

        Args:
            client: The Gemini API client
        """
        self.client = client

    def create_store(self, display_name: str) -> str:
        """
        Create a new File Search store.

        Args:
            display_name: Human-readable name for the store

        Returns:
            The store name (e.g., 'fileSearchStores/abc123')

        Example:
            >>> manager = FileSearchStoreManager(client)
            >>> store_name = manager.create_store("FAQ Store")
            >>> print(f"Created store: {store_name}")
        """
        store = self.client.file_search_stores.create(
            config={"display_name": display_name}
        )
        return store.name

    def list_stores(self):
        """List all File Search stores."""
        return list(self.client.file_search_stores.list())

    def get_store(self, name: str):
        """
        Get a specific store by name.

        Args:
            name: The store name (e.g., 'fileSearchStores/abc123')
        """
        return self.client.file_search_stores.get(name=name)

    def delete_store(self, name: str, force: bool = True):
        """
        Delete a File Search store.

        Args:
            name: The store name to delete
            force: Force deletion even if store contains documents
        """
        self.client.file_search_stores.delete(name=name, config={"force": force})
