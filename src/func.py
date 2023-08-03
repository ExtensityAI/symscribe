import re
from typing import List
from pathlib import Path

import pandas as pd
from symai import Expression, Function, Interface

FUNCTION_DESCRIPTION = '''
Transcription Guidelines:
    Create new chapters at logical topic transitions.
    Highlight significant events or discussions.
    Keep chapter headings concise, use less than 2 words.
    Respect the timestamps.
    Use commas to separate multiple topics, but don't use commas at the end of the line.
    Use a blank line as seperator between chapters.
    Don't add quotes or other special characters other than the ones required by the template.
    Template:
        HH:MM:SS - {comma separated headings}\n
'''

class MyExpression(Expression):
    def __init__(self):
        super().__init__()
        self.fn = Function(FUNCTION_DESCRIPTION)

    def forward(self, data, template: str = '', *args, **kwargs):
        lang = kwargs.get("language", "en")
        bin_size_s = int(kwargs.get("bin_size_s", 5 * 60)) #@NOTE: default to 5 minutes bins
        export_dir = kwargs.get("export_dir", Path.cwd())
        whisper = Interface("whisper")
        transcript = whisper(data, language=lang, word_timestamps=True, disable_pbar=True)
        bins = self._get_bins(transcript.value, bin_size_s)
        chapters = "\n".join([self.fn(bin).value for bin in bins])
        pd.DataFrame(self._naive_format_validator(chapters),columns=["Chapters"]).to_csv(Path(export_dir) / "chapters.csv")
        pd.DataFrame(transcript.value.split("\n"), columns=["Transcript"]).to_csv(Path(export_dir) / "transcript.csv")
        return f"Files were successfully exported to {export_dir} as chapters.csv and transcript.csv"

    def _get_bins(self, data: str, bin_size_s: int) -> str:
        tmps = map(self._seconds, re.findall(r"\b\d{2}:\d{2}:\d{2}\b", data))
        data = zip(tmps, data.split("\n"))
        bin = []
        for tmp, seg in data:
            bin.append(seg)
            if tmp == 0 or (tmp - bin_size_s) % bin_size_s != 0:
                continue
            yield "\n".join(bin)
            bin = []
        yield "\n".join(bin)
        bin = []

    def _seconds(self, tmp: str) -> int:
        h, m ,s = tmp.split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)

    def _naive_format_validator(self, s: str) -> List[str]:
        sval = []
        for _ in (_ for _ in s.replace('"', "").split("\n") if _):
            if _.count(":") < 2:
                continue
            if _.startswith("'"):
                _ = _[1:]
            if _.endswith("'"):
                _ = _[:-1]
            sval.append(_)
        return sval

