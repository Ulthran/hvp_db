import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from hvp_db.cli import _load_csv


def test_load_csv_reports_all_enum_errors(tmp_path):
    csv_content = (
        "sample_id,participant_id,anatomical_site,storage_buffer,sample_use\n"
        "s1,p1,invalid_site,neat,experiment\n"
        "s2,p2,np_swab,invalid_buffer,invalid_use\n"
    )
    csv_file = tmp_path / "samples.csv"
    csv_file.write_text(csv_content)

    with pytest.raises(ValueError) as exc:
        _load_csv("sqlite:///:memory:", str(csv_file))

    message = str(exc.value)
    assert "line 2" in message and "anatomical_site" in message
    assert "line 3" in message and "storage_buffer" in message
    assert "sample_use" in message
