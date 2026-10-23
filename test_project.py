import sys
import pandas as pd
import pytest

# Fix command-line argument BEFORE importing project
_original_argv = sys.argv
sys.argv = ["project.py", "test_data.csv"]
import project

sys.argv = _original_argv


def sample_data():
    return pd.DataFrame(
        {
            "Religion": ["Muslim", "Muslim", "Christian"],
            "Sect": ["Sunni", "Shia", "Maronite"],
            "No. of voters 2018": [100, 200, 150],
            "No. of voters 2022": [110, 220, 165],
            "Difference": [10, 20, 15],
            "Percentage %": [10.0, 10.0, 10.0],
        }
    )


def test_cleaning(tmp_path):
    data = sample_data()
    data.loc[len(data)] = ["Ignore", "Total", 450, 495, 45, 10]
    path = tmp_path / "test.csv"
    data.to_csv(path, index=False)

    result, filename = project.cleaning(str(path))

    assert "Ignore" not in result["Religion"].values
    assert result["No. of voters 2018"].dtype.kind in "iu"
    assert "Percentage %" in result.columns


def test_general_stats(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = sample_data()

    result, filename = project.general_stats(data, "test.csv")

    assert result.equals(data)
    assert (tmp_path / "General_Desc_Stats.csv").exists()


def test_plot_settings(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    project.plot_settings("test", "Voters")

    assert (tmp_path / "test Voters.png").exists()


def test_plots(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(project, "NAME", "test")

    data = sample_data()
    result, filename = project.plots(data, "test.csv")

    assert result.equals(data)
    assert (tmp_path / "test No. of voters 2018-2022.png").exists()
    assert (tmp_path / "test Percentage %.png").exists()
