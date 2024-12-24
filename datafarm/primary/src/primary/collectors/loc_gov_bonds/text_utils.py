def standardize_bond_name(bond_name: str) -> str:
    """
    Standardize bond names by converting various types of dashes to standard hyphen.
    
    Args:
        bond_name (str): Original bond name
        
    Returns:
        str: Standardized bond name
    """
    # List of different dash characters to replace
    dash_chars = [
        '－',  # Em dash (Unicode: U+FF0D)
        '—',   # Em dash (Unicode: U+2014)
        '–',   # En dash (Unicode: U+2013)
        '⁃',   # Hyphen bullet (Unicode: U+2043)
        '‐',   # Hyphen (Unicode: U+2010)
        '‑',   # Non-breaking hyphen (Unicode: U+2011)
    ]
    
    # Replace all dash variations with standard hyphen
    result = bond_name
    for dash in dash_chars:
        result = result.replace(dash, '-')
    
    return result


def standardize_text(text: str, language: str = 'zh') -> str:
    """
    Standardize text by converting various characters to their standard form.
    Supports multiple languages.
    
    Args:
        text (str): Original text
        language (str): Language code ('zh' for Chinese, 'en' for English)
        
    Returns:
        str: Standardized text
    """
    if not text:
        return text

    # Common replacements for all languages
    text = text.strip()
    
    # Replace various types of spaces
    space_chars = [
        '\u3000',  # Ideographic space
        '\u00A0',  # Non-breaking space
        '\u2002',  # En space
        '\u2003',  # Em space
        '\u2004',  # Three-per-em space
        '\u2005',  # Four-per-em space
        '\u2006',  # Six-per-em space
        '\u2007',  # Figure space
        '\u2008',  # Punctuation space
        '\u2009',  # Thin space
        '\u200A',  # Hair space
        '\u202F',  # Narrow no-break space
        '\u205F',  # Medium mathematical space
    ]
    
    for space in space_chars:
        text = text.replace(space, ' ')
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    # Language-specific standardization
    if language == 'zh':
        # Chinese specific replacements
        zh_chars = {
            '（': '(',  # Full-width parentheses to half-width
            '）': ')',
            '［': '[',  # Full-width brackets to half-width
            '］': ']',
            '【': '[',  # Chinese brackets to standard brackets
            '】': ']',
            '《': '<',  # Chinese angle brackets to standard
            '》': '>',
            '"': '"',   # Chinese quotes to standard
            '"': '"',
            ''': "'",   # Chinese single quotes to standard
            ''': "'",
            '，': ',',  # Chinese punctuation to standard
            '。': '.',
            '：': ':',
            '；': ';',
            '！': '!',
            '？': '?',
            '～': '~',
            '…': '...',
            # Number conversions
            '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
            '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
        }
        for old, new in zh_chars.items():
            text = text.replace(old, new)
            
    elif language == 'en':
        # English specific replacements
        text = text.replace('"', '"')  # Straight quotes
        text = text.replace('"', '"')
        text = text.replace(''', "'")  # Straight single quotes
        text = text.replace(''', "'")
        
    # Apply dash standardization
    text = standardize_bond_name(text)
    
    return text


# PostgreSQL function:
    """
-- Function for standardizing text (handles both Chinese and English characters)
CREATE OR REPLACE FUNCTION standardize_text(input_text text) RETURNS text AS $$
DECLARE
    result text;
BEGIN
    result := input_text;
    
    -- Replace spaces
    result := regexp_replace(result, '[\u3000\u00A0\u2002-\u200A\u202F\u205F]', ' ', 'g');
    
    -- Replace Chinese characters
    result := replace(result, '（', '(');
    result := replace(result, '）', ')');
    result := replace(result, '［', '[');
    result := replace(result, '］', ']');
    result := replace(result, '【', '[');
    result := replace(result, '】', ']');
    result := replace(result, '《', '<');
    result := replace(result, '》', '>');
    result := replace(result, '"', '"');
    result := replace(result, '"', '"');
    result := replace(result, ''', '''');
    result := replace(result, ''', '''');
    result := replace(result, '，', ',');
    result := replace(result, '。', '.');
    result := replace(result, '：', ':');
    result := replace(result, '；', ';');
    result := replace(result, '！', '!');
    result := replace(result, '？', '?');
    result := replace(result, '～', '~');
    result := replace(result, '…', '...');
    
    -- Replace full-width numbers
    result := replace(result, '０', '0');
    result := replace(result, '１', '1');
    result := replace(result, '２', '2');
    result := replace(result, '３', '3');
    result := replace(result, '４', '4');
    result := replace(result, '５', '5');
    result := replace(result, '６', '6');
    result := replace(result, '７', '7');
    result := replace(result, '８', '8');
    result := replace(result, '９', '9');
    
    -- Replace various dashes
    result := regexp_replace(result, '[－—–⁃‐‑]', '-', 'g');
    
    -- Normalize multiple spaces
    result := regexp_replace(result, '\s+', ' ', 'g');
    
    -- Trim spaces
    result := trim(result);
    
    RETURN result;
END;
$$ LANGUAGE plpgsql IMMUTABLE STRICT;

-- Example usage:
-- SELECT standardize_text('２０２４年黑龙江省棚改专项债券（二期）－2024年黑龙江省政府专项债券（七期）');
"""
