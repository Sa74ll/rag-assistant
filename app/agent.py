import os
import logging
from pydantic import BaseModel
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatResponse(BaseModel):
    """Response from the agent with text and citations."""

    text: str
    citations: list[str]


class FAQAgent:
    """
    Customer support agent with conversation memory.

    Uses Gemini's File Search API to answer questions from a knowledge base,
    maintaining conversation history for context-aware responses.
    """

    SYSTEM_PROMPT = """
أنت مساعد ذكي متخصص في أنظمة ولوائح البنك المركزي السعودي (ساما).

## التعليمات:
- أجب على الأسئلة باللغة العربية بشكل افتراضي
- إذا سأل المستخدم باللغة الإنجليزية أو طلب الإجابة بالإنجليزية، أجب بالإنجليزية
- استخدم أسلوباً رسمياً ومهنياً يليق بالقطاع المالي والتنظيمي
- عند الإجابة، اذكر اسم النظام أو اللائحة والمادة أو البند المرجعي إن وُجد
- كن دقيقاً ومختصراً وواضحاً في إجاباتك

## قواعد مهمة:
- أجب فقط من المعلومات الموجودة في قاعدة المعرفة
- إذا لم تجد الإجابة في الوثائق المتاحة، قل:
  "عذراً، لم أتمكن من العثور على معلومات حول هذا الاستفسار في الأنظمة واللوائح المتاحة. يُرجى التواصل مع الإدارة المختصة للحصول على مزيد من التوضيح."
- لا تختلق أو تفترض معلومات غير موجودة في المستندات
"""

    def __init__(self, store_name: str | None = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the agent.

        Args:
            store_name: File search store name (or set STORE_NAME env var)
            model: Gemini model to use
        """
        self.client = genai.Client()
        self.store_name = store_name or os.getenv("STORE_NAME")
        self.model = model
        self.history: list[types.Content] = []

        if not self.store_name:
            raise ValueError(
                "Store name must be provided or set in STORE_NAME environment variable"
            )

    def chat(self, message: str) -> ChatResponse:
        """
        Send a message and get a response, maintaining conversation history.

        Args:
            message: The user's message

        Returns:
            ChatResponse with text and citations
        """
        # Add user message to history
        self.history.append(
            types.Content(role="user", parts=[types.Part(text=message)])
        )

        # Call Gemini with file search tool
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.history,
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT,
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[self.store_name]
                        )
                    )
                ],
            ),
        )

        # Extract response text
        assistant_message = response.text

        # Extract citations from grounding metadata
        citations = self._extract_citations(response)

        # Add assistant response to history
        self.history.append(
            types.Content(role="model", parts=[types.Part(text=assistant_message)])
        )

        return ChatResponse(text=assistant_message, citations=citations)

    def _extract_citations(self, response) -> list[str]:
        """Extract unique source document names from grounding metadata."""
        sources = set()

        try:
            metadata = response.candidates[0].grounding_metadata
            chunks = metadata.grounding_chunks

            logger.info("=" * 50)
            logger.info("RETRIEVED CHUNKS FROM FILE SEARCH")
            logger.info("=" * 50)

            if not chunks:
                logger.warning("No chunks retrieved from file search")
            else:
                logger.info(f"Total chunks retrieved: {len(chunks)}")

            for i, chunk in enumerate(chunks or []):
                logger.info(f"\n--- Chunk {i + 1} ---")

                # Log retrieved context
                ctx = getattr(chunk, "retrieved_context", None)
                if ctx:
                    title = getattr(ctx, "title", None)
                    uri = getattr(ctx, "uri", None)
                    text = getattr(ctx, "text", None)

                    logger.info(f"  Title: {title}")
                    logger.info(f"  URI: {uri}")
                    if text:
                        # Truncate long text for readability
                        preview = text[:500] + "..." if len(text) > 500 else text
                        logger.info(f"  Text preview: {preview}")

                    name = title or uri
                    if name:
                        sources.add(name)
                else:
                    logger.info("  No retrieved context")

            # Log grounding supports if available
            supports = getattr(metadata, "grounding_supports", None)
            if supports:
                logger.info(f"\nGrounding supports: {len(supports)}")
                for j, support in enumerate(supports):
                    logger.info(f"  Support {j + 1}: {support}")

            logger.info("=" * 50)

        except (AttributeError, IndexError) as e:
            logger.error(f"Error extracting citations: {e}")

        return [f"Source: {s}" for s in sources if s]

    def clear_history(self):
        """Clear conversation history to start fresh."""
        self.history = []
