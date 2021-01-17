import pytest
import json
from cb_wrapper import APIModern

wrapper = APIModern()


@pytest.mark.parametrize("data, expected_result", (
        (
                {'content': json.loads('{ "test": "simple text", "header": { "sub": "sub text"} }')},
                {'content': [
                    '{',
                    'test', ':', 'simple text', ',',
                    'header', ':{', 'sub', ':', 'sub text', ',', '},',
                    '}'
                ]}
        ),
        (
                {'content': json.loads('{ "test": "simple text", "header": { "sub": "sub text"}, "last": "text" }')},
                {'content': [
                    '{',
                    'test', ':', 'simple text', ',',
                    'header', ':{', 'sub', ':', 'sub text', ',', '},',
                    'last', ':', 'text', ',',
                    '}'
                ]}
        ),
        (
                {'content': json.loads('{ "test": "simple text", "another_one": "another simple test" }')},
                {'content': ['{', 'test', ':', 'simple text', ',', 'another_one', ':', 'another simple test', ',', '}']}
        ),
        (
                {'content': json.loads('{ "test": {} }')},
                {'content': ['{', 'test', ':{', '},', '}']}
        ),
        (
                {'content': json.loads('[{ "test": {} }]')},
                {'content': ['[', '{', 'test', ':{', '},', '},', ']']}
        ),
        (
                {'content': json.loads('[{ "test": {} }]')},
                {'content': ['[', '{', 'test', ':{', '},', '},', ']']}
        ),
        (
                {'content': json.loads('[{ "test": [] }]')},
                {'content': ['[', '{', 'test', ':[', '],', '},', ']']}
        ),
        (
                {'content': json.loads('[{ "test": [{}, {}] }]')},
                {'content': ['[', '{', 'test', ':[', '{', '},', '{', '},', '],', '},', ']']}
        ),
        (
                {'content': json.loads('[{ "test": [{}, []] }]')},
                {'content': ['[', '{', 'test', ':[', '{', '},', '[', '],', '],', '},', ']']}
        )
))
def test_json_to_str(data, expected_result):
    assert wrapper.json_to_str(data) == expected_result


@pytest.mark.parametrize("data, expected_result", (
        (
                {'content': [
                    '{',
                    'test', ':', 'simple text', ',',
                    'header', ':{', 'sub', ':', 'sub text', ',', '},',
                    '}'
                ]},
                {'content': json.loads('{ "test": "simple text", "header": { "sub": "sub text"} }')}
        ),
        (
                {'content': [
                    '{',
                    'test', ':', 'simple text', ',',
                    'header', ':{', 'sub', ':', 'sub text', ',', '},',
                    'last', ':', 'text', ',',
                    '}'
                ]},
                {'content': json.loads('{ "test": "simple text", "header": { "sub": "sub text"}, "last": "text" }')}
        ),
        (
                {'content': ['{', 'test', ':', 'simple text', ',', 'another_one', ':', 'another simple test', ',',
                             '}']},
                {'content': json.loads('{ "test": "simple text", "another_one": "another simple test" }')}
        ),
        (

                {'content': ['{', 'test', ':{', '},', '}']},
                {'content': json.loads('{ "test": {} }')}
        ),
        (

                {'content': ['[', '{', 'test', ':{', '},', '},', ']']},
                {'content': json.loads('[{ "test": {} }]')}
        ),
        (

                {'content': ['[', '{', 'test', ':{', '},', '},', ']']},
                {'content': json.loads('[{ "test": {} }]')}
        ),
        (

                {'content': ['[', '{', 'test', ':[', '],', '},', ']']},
                {'content': json.loads('[{ "test": [] }]')}
        ),
        (

                {'content': ['[', '{', 'test', ':[', '{', '},', '{', '},', '],', '},', ']']},
                {'content': json.loads('[{ "test": [{}, {}] }]')}
        ),
        (

                {'content': ['[', '{', 'test', ':[', '{', '},', '[', '],', '],', '},', ']']},
                {'content': json.loads('[{ "test": [{}, []] }]')}
        )
))
def test_str_to_json(data, expected_result):
    assert wrapper.str_to_json(data) == expected_result
