# Image Module for PDF
import os
import io
import base64
import mimetypes
import logging
import time
import traceback
import re
from typing import List, Dict, Optional
from utils.pdf_utils import _build_chapter_map
import fitz  # PyMuPDF
from PIL import Image
from openai import OpenAI
from utils.client import OpenAIClient

# Base URL for local/remote vision model API
IMAGE_MODEL_URL = os.getenv("IMAGE_MODEL_URL", "http://localhost:8000/v1")
IMAGE_DIR = os.getenv("IMAGE_DIR", "/Users/wjs/Library/CloudStorage/OneDrive-Personal/Coding, ML & DL/GenAI Beta/week_3/MultiModal_RAG/data/image")    

def extract_and_save_images(pdf_path: str, min_width: int = 100, min_height: int = 100) -> List[dict]:
    """
    Extract images from a PDF and save them to disk.

    - Filters out small images to avoid icons/thumbnails (defaults: 200x200).
    - Saves with deterministic names: {pdf_basename}_page{page_number:03d}_img{img_index:03d}.{ext}

    Returns a list of metadata dicts for each saved image.
    """
    results: List[Dict] = []

    if not os.path.isfile(pdf_path):
        logging.error(f"PDF not found: {pdf_path}")
        return results

    # Ensure output directory exists
    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)
    except Exception:
        logging.error(traceback.format_exc())
        return results

    pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
    page_to_chapter = _build_chapter_map(pdf_path)
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        logging.error(traceback.format_exc())
        return results

    try:
        for page_index in range(len(doc)):
            page_number = page_index + 1  # 1-indexed page number
            page = doc.load_page(page_index)
            images = page.get_images(full=True)
            metadata = dict(getattr(doc, "metadata", {}) or {})
            metadata.setdefault("source", pdf_path)
            metadata["page"] = page_number
            # get chapter number
            chapter_num = page_to_chapter.get(int(page_number)) if isinstance(page_number, int) or (isinstance(page_number, str) and page_number.isdigit()) else None
            metadata["chapter"] = chapter_num

            for img_idx_on_page, img in enumerate(images):
                try:
                    xref = img[0]
                    img_info = doc.extract_image(xref)
                    img_bytes: bytes = img_info.get("image", b"")
                    img_ext: str = img_info.get("ext", "png")  # fallback to png
                    if not img_bytes:
                        continue

                    # Inspect size with PIL
                    try:
                        with Image.open(io.BytesIO(img_bytes)) as pil_img:
                            width, height = pil_img.size
                            # Small image filter: skip icons/thumbnails
                            if width < min_width or height < min_height:
                                continue
                            # Build deterministic filename
                            filename = f"{pdf_basename}_page{page_number:03d}_img{img_idx_on_page:03d}.{img_ext}"
                            full_path = os.path.join(IMAGE_DIR, filename)
                            # Avoid collisions by overwriting deterministically or ensure unique
                            pil_img.save(full_path)
                            result = {
                                "image_path": full_path,
                                "file_name": filename,
                                "page_number": page_number,
                                "img_index": img_idx_on_page,
                                "width": int(width),
                                "height": int(height),
                                "source_pdf": pdf_path,
                                "page_text": page.get_text(),
                            }
                            result = result | metadata
                            results.append(result)
                    except Exception:
                        # Unreadable image; skip
                        logging.error(traceback.format_exc())
                        continue
                except Exception:
                    logging.error(traceback.format_exc())
                    continue
    finally:
        try:
            doc.close()
        except Exception:
            pass

    return results

class ImageProcessor:
    def __init__(self):
        pass

    def summarize_image(self, image_path: str) -> str:
        """Summarize the image by LLM.

        Returns a dict with keys:
        - summary_text: str | None

        Note: Although signature hints at str, this returns a dict for richer metadata.
        """
        # Read local image and convert to Base64 data URL
        with open(image_path, 'rb') as f:
            content_bytes = f.read()
        mime_type = mimetypes.guess_type(image_path)[0] or 'image/png'
        encoded = base64.b64encode(content_bytes).decode('utf-8')
        data_url = f"data:{mime_type};base64,{encoded}"

        prompt_text = "详细地描述这张图片的内容，不要漏掉细节，并提取图片中的文字。注意只需客观说明图片内容，无需进行任何评价。"
        # Call OpenAI-like client with retries
        client = OpenAIClient(model="internvl-internlm2", api_key='API_KEY', base_url=IMAGE_MODEL_URL)
        summary_text: Optional[str] = None

        summary_text = client.chat(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        temperature=0.2,
        top_p=0.95,
        max_tokens=2048,
        stream=False,
        )

        return summary_text

    def context_augment(self, image_description: str, context: str) -> str:
        prompt = f'''
        目标：通过图片的上下文以及来源文件信息补充图片描述的细节，准确描述出图片在文档中的实际内容和用途含义。

        注意事项：
        - 上下文中可能会有噪音，请注意甄别。
        - 重点关注上下文中的图片caption标注，因为它们通常描述图片的用途和意义。
        - 保留图片的意图与重要信息，过滤掉与上下文无关的信息。
        - 有时图片描述中会出现重复性的内容，这类内容请视为噪音过滤掉。
        - 请直接输出答案，无需解释。
        - 如果图片不包含任何内容，或者为背景图片，输出 0

        期望输出：
        - 一段精准并且详细的描述，说明图片在上下文中的作用和意义，以及图片中的重要细节。
        - 保留图片描述中的文字以及数据，不要遗漏。

        输出案例(供参考)：
        1. 图片描述了在狭义相对论的框架下，一个闪光事件在不同参考系（S 和 S'）中的观察结果。在参考系 S 中，闪光发生在 M 点，光信号以光速 c 向各个方向传播。在参考系 S' 中，S' 相对于 S 以速度 u 沿着 MB 方向运动。在 S' 参考系中，A' 和 B' 是两个接收器，它们随着 S' 一起运动。闪光发生后，光信号以光速 c 向各个方向传播，由于 A' 比 B' 早接收到光信号，因此在 S' 参考系中，事件1（A' 接收到光信号）先于事件2（B' 接收到光信号）发生。图片中标注了各个事件发生的位置和时间关系，其中 AM' < BM'，说明在 S' 参考系中，A' 比 B' 更靠近闪光发生的位置 M。
        2. 图片2.1展示了网络爬虫的工作原理。爬虫程序从互联网上获取数据，经过筛选和清洗，提取出有价值的信息，去除无关数据，最终形成结构化的数据。这一过程体现了爬虫技术在数据采集和处理中的关键作用，尤其是在大数据时代，爬虫技术能够自动化地获取大量信息，为后续的数据分析和应用提供了基础支持。
        3. 图片展示了杭州市公安局西湖风景区名胜区分局西湖核心景区监控设施提升完善及安全提升项目的文档统计情况。统计内容包括：考核数38，已提交29；按时提交的文档数15，及时提交的12，未及时提交的2。具体文档包括开工申请、监理工作总结、方案计划报审表、开工令和周报等，以及各自的提交截止日期和实际提交日期。

        图片描述：
        ```
        {image_description}
        ```

        上下文：
        ```
        {context}
        ```
        '''
        client = OpenAIClient()
        result = client.chat(
            messages=[
                {"role": "system", "content": "你是一个智能AI助手，根据图片的上下文对图片描述进行补充，补充后的描述要更加准确，更加详细，更加完整。"},
                {"role": "user", "content": prompt},
            ]
        )
        return result

    def get_metadata(self, dict_data: dict) -> dict:
        return {
            "source": dict_data.get("source", ""),
            "title": dict_data.get("title", ""),
            "author": dict_data.get("author", ""),
            "subject": dict_data.get("subject", ""),
            "keywords": dict_data.get("keywords", ""),
            "page": dict_data.get("page", None),
            "chapter": dict_data.get("chapter", None),
            "image_path": dict_data.get("image_path", ""),
            "image_description": dict_data.get("image_description", ""),
            "img_index": dict_data.get("img_index", None),
        }

    def process(self, info_path: str) -> list[dict]:
        # Read image from PDF and output image chunks (context augmented), with metadata
        # If a PDF is provided, extract images and return their metadata
        image_results = extract_and_save_images(info_path, min_width=200, min_height=200)
        '''
        image_result = {
        "image_path": full_path,
        "file_name": filename,
        "page_number": page_number,
        "img_index": img_idx_on_page,
        "width": int(width),
        "height": int(height),
        "source_pdf": pdf_path,
        "page_text": page.get_text()
        }
        '''
        chunks: List[Dict[str]] = []
        for image_result in image_results:
            image_path = image_result["image_path"]
            image_description = self.summarize_image(image_path)
            print(f'Image Description: {image_description}')
            image_result["image_description"] = image_description
            context_aug_content = self.context_augment(image_description, image_result["page_text"])
            print(f'Context Augmented Content: {context_aug_content}')
            metadata = self.get_metadata(image_result)
            chunk = {
                "content": context_aug_content,
                "metadata": metadata,
            }
            chunks.append(chunk)
        return chunks