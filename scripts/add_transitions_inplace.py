#!/usr/bin/env python3
"""
animations.md に基づきスライドにFadeトランジションを追加
ZIPを直接編集し、OOXML構造を維持（アンパック/リパックしない）
"""
import zipfile
import io
import xml.etree.ElementTree as ET

NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def add_fade_transition_to_xml(xml_bytes: bytes) -> bytes:
    """スライドXMLにFadeトランジションを追加"""
    root = ET.fromstring(xml_bytes)

    # sld要素を取得（ルートがp:sldの場合、tagは {ns}sld）
    sld = root
    if "sld" not in root.tag:
        sld = root.find(f".//{{{NS}}}sld")
        if sld is None:
            return xml_bytes

    # 既存のtransitionを削除
    for trans in list(root.iter(f"{{{NS}}}transition")):
        parent = trans.getparent()
        if parent is not None:
            parent.remove(trans)

    # p:sld直下にFadeトランジションを追加（cSldの後、clrMapOvrの前に挿入）
    transition = ET.Element(f"{{{NS}}}transition")
    transition.set("spd", "med")
    transition.set("advClick", "1")
    ET.SubElement(transition, f"{{{NS}}}fade")

    # clrMapOvrの直前に挿入（なければ末尾に追加）
    clr_map = sld.find(f"{{{NS}}}clrMapOvr")
    if clr_map is not None:
        idx = list(sld).index(clr_map)
        sld.insert(idx, transition)
    else:
        sld.append(transition)

    # XMLをバイト列に変換（BOMなしUTF-8）
    tree = ET.ElementTree(root)
    buf = io.BytesIO()
    tree.write(buf, xml_declaration=True, encoding="UTF-8", default_namespace=None)
    return buf.getvalue()


def add_transitions_to_pptx(input_path: str, output_path: str) -> None:
    """PPTX内のスライドにトランジションを追加（ZIPを直接編集）"""
    with zipfile.ZipFile(input_path, "r") as z_in:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z_out:
            for item in z_in.infolist():
                data = z_in.read(item.filename)
                if (
                    item.filename.startswith("ppt/slides/slide")
                    and item.filename.endswith(".xml")
                    and "slideLayout" not in item.filename
                ):
                    data = add_fade_transition_to_xml(data)
                z_out.writestr(item.filename, data)
    print(f"Transitions added: {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: add_transitions_inplace.py input.pptx output.pptx")
        sys.exit(1)
    add_transitions_to_pptx(sys.argv[1], sys.argv[2])
