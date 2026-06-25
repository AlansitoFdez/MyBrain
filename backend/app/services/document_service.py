import httpx
from pypdf import PdfReader
from bs4 import BeautifulSoup
from io import BytesIO

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_text_from_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        with httpx.Client() as client:
            response = client.get(url, follow_redirects=True, timeout=10, headers=headers)
            response.raise_for_status()
    except Exception as e:
        print(f"ERROR fetching URL: {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text[:10000]