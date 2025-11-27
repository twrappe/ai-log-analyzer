## tests/test_log_analyzer.py
import pytest
from pathlib import Path
from log_analyzer.loader import load_json, load_log_file
from log_analyzer.analyzer import summarize_events
from log_analyzer.llm_client import analyze_with_llm
from log_analyzer.report import validate_summary, save_summary

def test_load_json(tmp_path):
    sample_file = tmp_path / 'sample.json'
    sample_file.write_text('{"key": "value"}')
    data = load_json(sample_file)
    assert data['key'] == 'value'

def test_load_log_file(tmp_path):
    log_file = tmp_path / 'sample.log'
    # Ensure each line ends with a newline
    log_file.write_text('ERROR Disk full\nINFO Service started\n')
    events = load_log_file(log_file)
    assert len(events) == 2
    assert events[0]['raw'].startswith('ERROR')

def test_summarize_events():
    events = [{'raw': 'ERROR Disk full'}, {'raw': 'INFO Started service'}]
    blueprint = {
        'severity_keywords': {'ERROR': ['error'], 'INFO': ['info']},
        'category_rules': {'system': ['disk', 'service']},
        'default_category': 'general'
    }
    summary = summarize_events(events, blueprint)
    assert summary['log_summary'][0]['severity'] == 'ERROR'
    assert summary['log_summary'][1]['severity'] == 'INFO'

def test_analyze_with_llm_mock():
    # Mock LLM behavior
    summary = {'log_summary': [{'message': 'ERROR Disk full', 'severity': 'ERROR', 'category': 'system'}]}
    enriched = analyze_with_llm(summary)
    for entry in enriched['log_summary']:
        assert entry.get('recommended_action') == 'No API key: placeholder action'

def test_validate_summary():
    schema = {
        'type': 'object',
        'properties': {
            'log_summary': {'type': 'array'}
        },
        'required': ['log_summary']
    }
    summary = {'log_summary': []}
    is_valid, err = validate_summary(summary, schema)
    assert is_valid
    assert err is None

def test_save_summary(tmp_path):
    summary = {'log_summary': [{'message': 'Test', 'severity': 'INFO', 'category': 'general'}]}
    output_file = tmp_path / 'summary.json'
    save_summary(summary, output_file)
    loaded = load_json(output_file)
    assert loaded == summary
