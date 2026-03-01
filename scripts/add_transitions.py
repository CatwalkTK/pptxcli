#!/usr/bin/env python3
"""
animations.md に基づきスライドにFadeトランジションを追加する
"""
import xml.etree.ElementTree as ET
import os
import glob

NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def add_fade_transition(slide_path, speed="med"):
    """スライドにFadeトランジションを追加（animations.md 準拠）"""
    tree = ET.parse(slide_path)
    root = tree.getroot()

    # sld要素（transitionの親）
    sld = root if "sld" in root.tag else root.find(f".//{{{NS}}}sld")
    if sld is None:
        sld = root

    # 既存のtransitionを削除（リストに集めてから削除）
    to_remove = list(root.iter(f"{{{NS}}}transition"))
    for trans in to_remove:
        parent = trans.getparent()
        if parent is not None:
            parent.remove(trans)

    # p:sld直下にFadeトランジションを追加
    transition = ET.SubElement(sld, f"{{{NS}}}transition")
    transition.set("spd", speed)
    transition.set("advClick", "1")
    ET.SubElement(transition, f"{{{NS}}}fade")

    tree.write(slide_path, xml_declaration=True, encoding="UTF-8", default_namespace=None)
    return True


def add_transitions_to_all(unpacked_dir, speed="med"):
    """全スライドにトランジションを追加"""
    slides_dir = os.path.join(unpacked_dir, "ppt", "slides")
    if not os.path.exists(slides_dir):
        print(f"Error: {slides_dir} not found")
        return False
    count = 0
    for slide_file in sorted(glob.glob(os.path.join(slides_dir, "slide*.xml"))):
        add_fade_transition(slide_file, speed)
        count += 1
        print(f"Added fade transition to {os.path.basename(slide_file)}")
    return count


if __name__ == "__main__":
    import sys
    unpacked_dir = sys.argv[1] if len(sys.argv) > 1 else "unpacked"
    add_transitions_to_all(unpacked_dir)
