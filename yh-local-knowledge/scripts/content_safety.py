"""Sanitize invisible controls and flag advisory prompt-injection shapes."""
from __future__ import annotations

import re
from dataclasses import dataclass


_INVISIBLE = frozenset(
    {
        0x00AD,
        0x034F,
        0x061C,
        0x180E,
        0x200B,
        0x200C,
        0x200D,
        0x200E,
        0x200F,
        0x202A,
        0x202B,
        0x202C,
        0x202D,
        0x202E,
        0x2060,
        0x2061,
        0x2062,
        0x2063,
        0x2064,
        0x2066,
        0x2067,
        0x2068,
        0x2069,
        0x3164,
        0xFEFF,
        0xFFA0,
    }
)
_TAG_START = 0xE0000
_TAG_END = 0xE007F


def is_invisible(codepoint: int) -> bool:
    return codepoint in _INVISIBLE or _TAG_START <= codepoint <= _TAG_END


def sanitize_extracted_text(text: str) -> tuple[str, int]:
    kept: list[str] = []
    removed = 0
    for char in text:
        if is_invisible(ord(char)):
            removed += 1
        else:
            kept.append(char)
    return "".join(kept), removed


@dataclass(frozen=True)
class Finding:
    line: int
    rule_id: str
    message: str


_RULES = (
    (
        "prompt.ignore_prior",
        re.compile(
            r"\bignore\s+(?:(?:all|any|the)\s+)?(?:previous|prior)\s+"
            r"(?:instructions?|prompts?|rules?|messages?)\b",
            re.IGNORECASE,
        ),
        "instruction-override phrase",
    ),
    (
        "prompt.role_reassignment",
        re.compile(r"\byou\s+are\s+now\b", re.IGNORECASE),
        "role-reassignment phrase",
    ),
    (
        "prompt.zh_override",
        re.compile(r"忽略.{0,12}(?:之前|先前|以上|系统|开发者).{0,8}(?:指令|提示|规则)"),
        "Chinese instruction-override phrase",
    ),
    (
        "prompt.system_tag",
        re.compile(r"<\s*/?\s*(?:system|developer)\b[^>]*>", re.IGNORECASE),
        "system-like message tag",
    ),
    (
        "prompt.chat_template",
        re.compile(r"<\|\s*im_start\s*\|>|\[\s*INST\s*\]", re.IGNORECASE),
        "chat-template delimiter",
    ),
)

_OUTBOUND = re.compile(r"\b(?:curl|wget|upload|transmit|send)\b|https?://|上传|发送|外传", re.IGNORECASE)
_SENSITIVE = re.compile(r"\.env\b|\b(?:secrets?|credentials?|api[_ -]?keys?)\b|密钥|凭据|令牌", re.IGNORECASE)


def scan_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(is_invisible(ord(char)) for char in line):
            findings.append(Finding(line_number, "unicode.invisible", "invisible Unicode control"))
        for rule_id, pattern, message in _RULES:
            if pattern.search(line):
                findings.append(Finding(line_number, rule_id, message))
        if _OUTBOUND.search(line) and _SENSITIVE.search(line):
            findings.append(Finding(line_number, "tool.exfiltration_shape", "outbound action combined with sensitive-data language"))
    return findings
