import logging
import re
from pathlib import Path

logger = logging.getLogger("phoenix_charts.wheel")

# Matches: var(--kerykeion-foo-bar)
VAR_PATTERN = re.compile(r"var\(\s*(--kerykeion-[^)]+?)\s*\)")

# Matches CSS var definitions: --kerykeion-foo-bar: value;
VAR_DEF_PATTERN = re.compile(
    r"(?P<name>--kerykeion-[a-z0-9\-]+)\s*:\s*(?P<value>[^;]+);",
    re.IGNORECASE,
)

# Map theme name -> css filename under app/themes
THEME_FILES = {
    "classic": "classic.css",
    "dark": "dark.css",
    "dark-high-contrast": "dark-high-contrast.css",
    "light": "light.css",
    "strawberry": "strawberry.css",
    "black-and-white": "black-and-white.css",
}


def _normalize_theme_name(theme: str | None) -> str:
    if not theme:
        return "classic"
    t = theme.strip().lower().replace("_", "-")
    return t if t in THEME_FILES else "classic"


def _load_theme_vars(theme: str) -> dict[str, str]:
    """
    Load all --kerykeion-* variables from the corresponding CSS file and
    resolve single-level var(...) indirections (e.g. chart-color-* pointing
    at color-*).
    """
    base_dir = Path(__file__).resolve().parents[1] / "themes"
    css_path = base_dir / THEME_FILES[theme]

    if not css_path.exists():
        logger.warning("[phoenix_theme] CSS file not found for theme=%s at %s", theme, css_path)
        return {}

    text = css_path.read_text(encoding="utf-8")

    raw_vars: dict[str, str] = {}

    # First pass: collect all --kerykeion-* definitions verbatim
    for m in VAR_DEF_PATTERN.finditer(text):
        name = m.group("name").strip()
        value = m.group("value").strip()
        raw_vars[name] = value

    # Second pass: resolve values like "var(--kerykeion-color-warning)"
    resolved: dict[str, str] = {}

    def resolve_value(val: str, depth: int = 0) -> str:
        # Avoid infinite loops
        if depth > 5:
            return val
        m = VAR_PATTERN.search(val)
        if not m:
            return val
        ref_name = m.group(1)
        ref_val = raw_vars.get(ref_name)
        if ref_val is None:
            return val
        # If the referenced value is another var(), resolve recursively
        if "var(" in ref_val:
            ref_val = resolve_value(ref_val, depth + 1)
        return ref_val.strip()

    for name, value in raw_vars.items():
        if "var(" in value:
            resolved[name] = resolve_value(value)
        else:
            resolved[name] = value.strip()

    logger.info(
        "[phoenix_theme] loaded %d variables for theme=%s from %s",
        len(resolved),
        theme,
        css_path.name,
    )
    return resolved


# Load all themes once at import
THEME_VARS: dict[str, dict[str, str]] = {
    theme: _load_theme_vars(theme) for theme in THEME_FILES.keys()
}


# … everything above stays exactly as you pasted …

def apply_phoenix_perfection(svg: str, theme: str = "classic") -> str:
    """
    Apply the EXACT Kerykeion theme colors to the SVG.

    - Reads all --kerykeion-* vars from the theme CSS.
    - Updates var definitions in the <style> section.
    - Inlines var(--kerykeion-...) usages in attributes.
    - Strips sign-name / planet-name text labels (for a cleaner wheel).
    - Ensures a chart "paper" background rect exists using paper-1.
    """
    raw_theme = theme
    theme = _normalize_theme_name(theme)
    logger.info(
        "[phoenix_theme] apply_phoenix_perfection raw_theme=%s normalized_theme=%s",
        raw_theme,
        theme,
    )

    theme_colors = THEME_VARS.get(theme, {})
    if not theme_colors:
        logger.warning(
            "[phoenix_theme] No theme vars loaded for %s; using SVG as-is", theme
        )

    # 1) Override CSS variable definitions in the SVG's <style> block
    for var_name, color in theme_colors.items():
        svg = re.sub(
            rf"{re.escape(var_name)}\s*:[^;]+;",
            f"{var_name}: {color};",
            svg,
        )

    # 2) Strip text labels (optional – keeps your wheel cleaner like examples)
    svg = re.sub(
        r'<text[^>]*class="sign-name"[^>]*>.*?</text>',
        "",
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(
        r'<text[^>]*class="planet-name"[^>]*>.*?</text>',
        "",
        svg,
        flags=re.DOTALL,
    )

    # 3) Inline any remaining var(--kerykeion-...) usages in attributes / styles
    #    with some explicit fallbacks for common base vars that might not be
    #    defined in the theme CSS (e.g. --kerykeion-color-neutral-content).
    FALLBACK_ALIASES: dict[str, str] = {
        # If neutral-content isn't defined, fall back to paper-0, then paper-1.
        "--kerykeion-color-neutral-content": "--kerykeion-chart-color-paper-0",
        # You can add more aliases here if upstream adds new base vars.
    }

    def _inline_var(m: re.Match) -> str:
        name = m.group(1)

        # If the theme defines this var, use it.
        if name in theme_colors:
            return theme_colors[name]

        # If we have an alias (e.g. neutral-content -> paper-0), try that.
        alias = FALLBACK_ALIASES.get(name)
        if alias and alias in theme_colors:
            return theme_colors[alias]

        # As a last resort, hard-code a reasonable neutral gray just so that
        # svglib doesn't see a raw "var(...)" and scream.
        if name == "--kerykeion-color-neutral-content":
            return "#9ca3af"  # tweak if you want a different neutral

        # Unknown var: leave it as-is so it's obvious something's missing.
        return m.group(0)

    svg = VAR_PATTERN.sub(_inline_var, svg)

    # 4) Ensure the SVG has a "paper" background rect inside <svg>, but
    #    do NOT touch the PDF page background.
    try:
        paper_hex = (
            theme_colors.get("--kerykeion-chart-color-paper-1")
            or theme_colors.get("--kerykeion-chart-color-paper-0")
        )

        if paper_hex:
            paper_hex = paper_hex.strip()
            if 'data-phoenix-paper-bg="1"' not in svg:
                m = re.search(r"<svg[^>]*>", svg, flags=re.IGNORECASE)
                if m:
                    insert_pos = m.end()
                    bg_rect = (
                        f'<rect width="100%" height="100%" '
                        f'fill="{paper_hex}" data-phoenix-paper-bg="1"/>'
                    )
                    svg = svg[:insert_pos] + bg_rect + svg[insert_pos:]
    except Exception as e:
        logger.warning("[phoenix_theme] failed to inject paper background: %s", e)

    return svg