#!/usr/bin/env python3
"""
Publica ghidul Claude Code in Notion cu structura ierarhica.

Moduri de utilizare:
  python publish_to_notion.py --all              # Publica tot ghidul (index + module)
  python publish_to_notion.py fisier.md          # Publica un singur fisier sub pagina ghidului
  python publish_to_notion.py --parent-id ID fisier.md  # Publica sub o pagina specifica
"""

import sys
import os
import json
import requests
import glob as globmod

# Config
ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")
DOC_PAGE_ID = "32df5e68-2ba7-80b3-a17c-de6960d1844e"
GHID_TITLE = "Ghid Claude Code"
NOTION_VERSION = "2022-06-28"


def load_api_key():
    if not os.path.exists(ENV_FILE):
        print("Eroare: fisierul .env nu exista.")
        sys.exit(1)
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("NOTION_API_KEY="):
                return line.strip().split("=", 1)[1]
    print("Eroare: NOTION_API_KEY nu gasita in .env")
    sys.exit(1)


def notion_request(api_key, method, endpoint, data=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    resp = requests.request(method, url, headers=headers, json=data)
    if not resp.ok:
        print(f"Eroare API Notion: {resp.status_code} — {resp.text}")
        return None
    return resp.json()


LANG_MAP = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "sh": "bash", "yml": "yaml", "md": "markdown", "rb": "ruby",
    "rs": "rust", "cs": "c#", "cpp": "c++", "mermaid": "plain text",
    "apidoc": "plain text",
}


def md_line_to_block(line):
    if line.startswith("# "):
        return {"object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]}}
    if line.startswith("## "):
        return {"object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]}}
    if line.startswith("### "):
        return {"object": "block", "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]}}
    if line.startswith("- ") or line.startswith("* "):
        return {"object": "block", "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]}}
    if line.startswith("> "):
        return {"object": "block", "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]}}
    if line.strip() in ("---", "***", "___"):
        return {"object": "block", "type": "divider", "divider": {}}
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": line.strip()}}]}}


def parse_markdown(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    title = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").replace("-", " ").title()
    first_line = content.split("\n")[0]
    if first_line.startswith("# "):
        title = first_line[2:].strip()

    blocks = []
    in_code = False
    code_lines = []
    code_lang = ""

    for line in content.split("\n"):
        if line.startswith("```"):
            if not in_code:
                in_code = True
                raw_lang = line[3:].strip().lower()
                code_lang = LANG_MAP.get(raw_lang, raw_lang) or "plain text"
                code_lines = []
            else:
                in_code = False
                blocks.append({
                    "object": "block", "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}],
                        "language": code_lang
                    }
                })
        elif in_code:
            code_lines.append(line)
        else:
            blocks.append(md_line_to_block(line))

    return title, blocks


def normalize_id(page_id):
    return page_id.replace("-", "")


def find_page_by_title(api_key, title, parent_id):
    result = notion_request(api_key, "POST", "search", {
        "query": title,
        "filter": {"property": "object", "value": "page"}
    })
    if not result:
        return None
    for page in result.get("results", []):
        if page.get("archived", False):
            continue
        parent = page.get("parent", {})
        pid = parent.get("page_id", "")
        page_title = ""
        title_prop = page.get("properties", {}).get("title", {}).get("title", [])
        if title_prop:
            page_title = title_prop[0].get("text", {}).get("content", "")
        if normalize_id(pid) == normalize_id(parent_id) and page_title == title:
            return page["id"]
    return None


def archive_page(api_key, title, parent_id):
    result = notion_request(api_key, "POST", "search", {
        "query": title,
        "filter": {"property": "object", "value": "page"}
    })
    if not result:
        return 0
    archived = 0
    for page in result.get("results", []):
        if page.get("archived", False):
            continue
        parent = page.get("parent", {})
        pid = parent.get("page_id", "")
        page_title = ""
        title_prop = page.get("properties", {}).get("title", {}).get("title", [])
        if title_prop:
            page_title = title_prop[0].get("text", {}).get("content", "")
        if normalize_id(pid) == normalize_id(parent_id) and page_title == title:
            notion_request(api_key, "PATCH", f"pages/{page['id']}", {"archived": True})
            archived += 1
    return archived


def create_page(api_key, title, blocks, parent_id):
    old = archive_page(api_key, title, parent_id)
    if old:
        print(f"  {old} versiune/versiuni vechi arhivate")

    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": blocks[:100]
    }
    page = notion_request(api_key, "POST", "pages", data)
    if not page:
        return None, None
    page_id = page["id"]

    remaining = blocks[100:]
    while remaining:
        chunk = remaining[:100]
        remaining = remaining[100:]
        notion_request(api_key, "PATCH", f"blocks/{page_id}/children", {"children": chunk})

    return page_id, page.get("url", "")


def find_or_create_ghid_parent(api_key):
    existing = find_page_by_title(api_key, GHID_TITLE, DOC_PAGE_ID)
    if existing:
        print(f"Pagina parinte '{GHID_TITLE}' gasita: {existing}")
        return existing

    print(f"Creez pagina parinte '{GHID_TITLE}'...")
    data = {
        "parent": {"page_id": DOC_PAGE_ID},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": GHID_TITLE}}]}
        },
        "children": [{
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {
                "content": "Ghid complet Claude Code in limba romana — 10 module, de la incepator la avansat."
            }}]}
        }]
    }
    page = notion_request(api_key, "POST", "pages", data)
    if not page:
        print("Eroare la crearea paginii parinte!")
        sys.exit(1)
    print(f"Pagina parinte creata: {page.get('url', '')}")
    return page["id"]


def notify(title, count):
    try:
        requests.post(
            "https://ntfy.sh/claude_code_mac",
            data=f"Ghid Claude Code publicat: {count} pagini\n{title}".encode("utf-8"),
            headers={"Title": "Ghid publicat in Notion", "Priority": "default"},
            timeout=5,
            verify=False
        )
    except Exception:
        pass


def publish_single(api_key, filepath, parent_id):
    if not os.path.exists(filepath):
        print(f"Eroare: fisierul '{filepath}' nu exista.")
        return False

    title, blocks = parse_markdown(filepath)
    print(f"Publicare: {title} ({len(blocks)} blocuri)")
    page_id, url = create_page(api_key, title, blocks, parent_id)
    if url:
        print(f"  OK: {url}")
        return True
    return False


def publish_all(api_key):
    base = os.path.dirname(__file__)
    ghid_parent = find_or_create_ghid_parent(api_key)

    # Ordine de publicare: hub docs, apoi module
    hub_files = ["README.md", "HARTA-INVATARE.md", "REFERINTA-RAPIDA.md", "CATALOG.md"]
    module_dirs = sorted(globmod.glob(os.path.join(base, "[0-9][0-9]-*")))

    count = 0

    # Publica hub documents
    for fname in hub_files:
        fpath = os.path.join(base, fname)
        if os.path.exists(fpath) and os.path.getsize(fpath) > 50:
            if publish_single(api_key, fpath, ghid_parent):
                count += 1

    # Publica module
    for mdir in module_dirs:
        readme = os.path.join(mdir, "README.md")
        if os.path.exists(readme) and os.path.getsize(readme) > 100:
            if publish_single(api_key, readme, ghid_parent):
                count += 1

    print(f"\nTotal: {count} pagini publicate sub '{GHID_TITLE}'")
    notify(GHID_TITLE, count)
    return count


def main():
    if len(sys.argv) < 2:
        print("Folosire:")
        print("  python publish_to_notion.py --all              # Publica tot ghidul")
        print("  python publish_to_notion.py fisier.md          # Publica un fisier")
        print("  python publish_to_notion.py --parent-id ID fisier.md")
        sys.exit(1)

    api_key = load_api_key()
    args = sys.argv[1:]

    if args[0] == "--all":
        publish_all(api_key)
        return

    parent_id = None
    filepath = None

    if "--parent-id" in args:
        idx = args.index("--parent-id")
        parent_id = args[idx + 1]
        filepath = args[idx + 2] if len(args) > idx + 2 else None
    else:
        filepath = args[0]

    if not filepath:
        print("Eroare: specifica un fisier .md")
        sys.exit(1)

    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)

    if not parent_id:
        parent_id = find_or_create_ghid_parent(api_key)

    publish_single(api_key, filepath, parent_id)


if __name__ == "__main__":
    main()
