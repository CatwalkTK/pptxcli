"""PowerPoint generation tool using python-pptx."""

import os
from typing import Any

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from .base import ToolDefinition, ToolResult


def _build_title_slide(prs: Presentation, title: str, subtitle: str = "") -> None:
    """Add a title slide (matches generate_ai_2026.py layout)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    if subtitle:
        sub_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(4), Inches(9), Inches(0.8)
        )
        tf2 = sub_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitle
        p2.font.size = Pt(24)
        p2.alignment = PP_ALIGN.CENTER


def _build_content_slide(
    prs: Presentation,
    heading: str,
    bullets: list[str],
) -> None:
    """Add a content slide with heading and bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(9), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = heading
    p.font.size = Pt(32)
    p.font.bold = True

    content_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.2), Inches(9), Inches(5.5)
    )
    tf = content_box.text_frame
    tf.word_wrap = True
    for i, text in enumerate(bullets):
        if i > 0:
            tf.add_paragraph()
        p = tf.paragraphs[-1]
        if not text.startswith(("\u2022", "-", "*")):
            p.text = f"\u2022 {text}"
        else:
            p.text = text
        p.font.size = Pt(18)
        p.space_after = Pt(14)


def _build_two_column_slide(
    prs: Presentation,
    heading: str,
    left_title: str,
    left_bullets: list[str],
    right_title: str,
    right_bullets: list[str],
) -> None:
    """Add a two-column content slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(9), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = heading
    p.font.size = Pt(32)
    p.font.bold = True

    # Left column
    left_box = slide.shapes.add_textbox(
        Inches(0.3), Inches(1.2), Inches(4.4), Inches(5.5)
    )
    tf_l = left_box.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = left_title
    p.font.size = Pt(20)
    p.font.bold = True
    p.space_after = Pt(8)
    for text in left_bullets:
        p = tf_l.add_paragraph()
        p.text = f"\u2022 {text}"
        p.font.size = Pt(16)
        p.space_after = Pt(10)

    # Right column
    right_box = slide.shapes.add_textbox(
        Inches(5.3), Inches(1.2), Inches(4.4), Inches(5.5)
    )
    tf_r = right_box.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = right_title
    p.font.size = Pt(20)
    p.font.bold = True
    p.space_after = Pt(8)
    for text in right_bullets:
        p = tf_r.add_paragraph()
        p.text = f"\u2022 {text}"
        p.font.size = Pt(16)
        p.space_after = Pt(10)


async def _generate_pptx(
    filename: str,
    title: str,
    subtitle: str = "",
    slides: list[dict[str, Any]] | None = None,
) -> ToolResult:
    """Generate a PowerPoint file from structured data."""
    if slides is None:
        slides = []

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    _build_title_slide(prs, title, subtitle)

    for slide_data in slides:
        slide_type = slide_data.get("type", "content")
        if slide_type == "two_column":
            _build_two_column_slide(
                prs,
                heading=slide_data.get("heading", ""),
                left_title=slide_data.get("left_title", ""),
                left_bullets=slide_data.get("left_bullets", []),
                right_title=slide_data.get("right_title", ""),
                right_bullets=slide_data.get("right_bullets", []),
            )
        else:
            _build_content_slide(
                prs,
                heading=slide_data.get("heading", ""),
                bullets=slide_data.get("bullets", []),
            )

    if not filename.endswith(".pptx"):
        filename = f"{filename}.pptx"
    # Ensure output goes to the output/ directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    abs_path = os.path.join(output_dir, os.path.basename(filename))
    prs.save(abs_path)
    slide_count = len(prs.slides)
    return f"PowerPoint generated: {abs_path} ({slide_count} slides)"


generate_pptx_tool = ToolDefinition(
    name="generate_pptx",
    description=(
        "Generate a PowerPoint (.pptx) file. Provide a title, optional subtitle, "
        "and a list of slides. Each slide has a 'type' ('content' or 'two_column'), "
        "a 'heading', and 'bullets' (list of strings). For two_column type, provide "
        "'left_title', 'left_bullets', 'right_title', 'right_bullets'."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Output filename (e.g., 'presentation.pptx')",
            },
            "title": {
                "type": "string",
                "description": "Presentation title (shown on title slide)",
            },
            "subtitle": {
                "type": "string",
                "description": "Subtitle on title slide",
                "default": "",
            },
            "slides": {
                "type": "array",
                "description": "List of slide definitions",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["content", "two_column"],
                            "description": "Slide layout type",
                            "default": "content",
                        },
                        "heading": {"type": "string", "description": "Slide heading"},
                        "bullets": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Bullet points for content slides",
                        },
                        "left_title": {"type": "string"},
                        "left_bullets": {"type": "array", "items": {"type": "string"}},
                        "right_title": {"type": "string"},
                        "right_bullets": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["heading"],
                },
            },
        },
        "required": ["filename", "title"],
    },
    handler=_generate_pptx,
)
