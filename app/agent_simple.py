"""The world's most minimal AI RAG agent ever"""

import os
from google import genai
from google.genai import types

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

class SimpleAgent:
    """Minimal agent using Gemini's File Search tool."""

    def __init__(self, store_name: str | None = None):
        self.client = genai.Client()
        self.store_name = store_name or os.getenv("STORE_NAME")

        if not self.store_name:
            raise ValueError("Store name required (or set STORE_NAME env var)")

    def chat(self, message: str) -> str:
        """Send a message and get a response."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[self.store_name]
                        )
                    )
                ],
            ),
        )
        return response.text
