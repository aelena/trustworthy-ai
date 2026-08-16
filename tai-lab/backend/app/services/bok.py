from dataclasses import dataclass, field
from pathlib import Path

from app.config import settings


@dataclass
class BokFile:
    path: str
    title: str
    content: str


@dataclass
class BokIndex:
    """In-memory index of the Body of Knowledge.

    The full corpus is loaded once at startup and concatenated into a single
    string used as a cached system prompt prefix on Anthropic. Total size is
    ~50-80K tokens — well within the context window of any current Claude.
    """

    files: list[BokFile] = field(default_factory=list)
    full_text: str = ""
    is_loaded: bool = False

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def token_estimate(self) -> int:
        # Rough heuristic: 1 token ~= 3.5 chars for English markdown.
        return int(len(self.full_text) / 3.5)

    def load(self) -> None:
        root = settings.bok_root.resolve()
        readme = root / "README.md"
        pages_dir = root / "pages"

        files: list[BokFile] = []
        if readme.exists():
            files.append(_read_file(readme, root))
        if pages_dir.exists():
            for md in sorted(pages_dir.glob("*.md")):
                files.append(_read_file(md, root))

        self.files = files
        self.full_text = "\n\n---\n\n".join(
            f"# Source: {f.path}\n\n{f.content}" for f in files
        )
        self.is_loaded = True

    def grep(self, query: str, max_hits: int = 8) -> list[BokFile]:
        q = query.lower()
        hits = [f for f in self.files if q in f.content.lower() or q in f.title.lower()]
        return hits[:max_hits]


def _read_file(path: Path, root: Path) -> BokFile:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")), rel)
    return BokFile(path=rel, title=title, content=text)


bok_index = BokIndex()
