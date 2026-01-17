"""
Bible MCP Server

A comprehensive Bible server providing verse lookup, search, chapter reading, and study tools using the Bible API

This MCP server is configured for remote hosting with SSE transport.
"""

import os
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Bible MCP Server")

@mcp.tool()
def get_verse(reference: str, translation: str) -> str:
    """Look up specific Bible verses by reference (e.g., 'John 3:16', 'Romans 8:28')

    Args:
        reference: Bible verse reference (e.g., 'John 3:16', 'Psalm 23:1-6')
        translation: Bible translation (default: KJV)

    Returns:
        The requested Bible verse(s) with reference and text
    """
    import requests
    translation = translation or 'kjv'
    url = f'https://bible-api.com/{reference}?translation={translation}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            return f"Error: {data['error']}"
        return f"{data['reference']} ({data['translation_name']}):\n{data['text'].strip()}"
    else:
        return f"Error fetching verse: HTTP {response.status_code}"

@mcp.tool()
def search_verses(query: str, limit: int) -> str:
    """Search for Bible verses containing specific words or phrases

    Args:
        query: Search term or phrase to find in Bible verses
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of Bible verses containing the search term
    """
    import requests
    limit = limit or 10
    url = f'https://bible-api.com/search/{query}?limit={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data or len(data) == 0:
            return f"No verses found containing '{query}'"
        results = []
        for verse in data[:limit]:
            results.append(f"{verse['reference']}: {verse['text'].strip()}")
        return f"Found {len(results)} verse(s) for '{query}':\n\n" + "\n\n".join(results)
    else:
        return f"Error searching verses: HTTP {response.status_code}"

@mcp.tool()
def get_chapter(book_chapter: str, translation: str) -> str:
    """Get an entire Bible chapter

    Args:
        book_chapter: Book and chapter reference (e.g., 'Genesis 1', 'Psalm 23')
        translation: Bible translation (default: KJV)

    Returns:
        The complete chapter text with all verses
    """
    import requests
    translation = translation or 'kjv'
    url = f'https://bible-api.com/{book_chapter}?translation={translation}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            return f"Error: {data['error']}"
        chapter_text = f"{data['reference']} ({data['translation_name']}):\n\n"
        for verse in data['verses']:
            chapter_text += f"{verse['verse']}. {verse['text']}\n"
        return chapter_text.strip()
    else:
        return f"Error fetching chapter: HTTP {response.status_code}"

@mcp.tool()
def get_random_verse(translation: str) -> str:
    """Get a random inspiring Bible verse

    Args:
        translation: Bible translation (default: KJV)

    Returns:
        A random Bible verse for inspiration
    """
    import requests
    import random
    inspiring_verses = [
        'Jeremiah 29:11', 'Romans 8:28', 'Philippians 4:13', 'John 3:16',
        'Psalm 23:1', 'Isaiah 40:31', 'Proverbs 3:5-6', 'Matthew 28:20',
        'Romans 8:31', 'Ephesians 2:8-9', 'Psalm 46:1', 'Isaiah 41:10'
    ]
    verse_ref = random.choice(inspiring_verses)
    translation = translation or 'kjv'
    url = f'https://bible-api.com/{verse_ref}?translation={translation}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Random Verse - {data['reference']} ({data['translation_name']}):\n{data['text'].strip()}"
    else:
        return f"Error fetching random verse: HTTP {response.status_code}"

@mcp.resource("bible://books")
def bible_books() -> str:
    """List of all 66 books of the Bible with their abbreviations"""
    books = [
        'Genesis (Gen)', 'Exodus (Exo)', 'Leviticus (Lev)', 'Numbers (Num)', 'Deuteronomy (Deu)',
        'Joshua (Jos)', 'Judges (Jdg)', 'Ruth (Rut)', '1 Samuel (1Sa)', '2 Samuel (2Sa)',
        '1 Kings (1Ki)', '2 Kings (2Ki)', '1 Chronicles (1Ch)', '2 Chronicles (2Ch)', 'Ezra (Ezr)',
        'Nehemiah (Neh)', 'Esther (Est)', 'Job (Job)', 'Psalms (Psa)', 'Proverbs (Pro)',
        'Ecclesiastes (Ecc)', 'Song of Solomon (Son)', 'Isaiah (Isa)', 'Jeremiah (Jer)', 'Lamentations (Lam)',
        'Ezekiel (Eze)', 'Daniel (Dan)', 'Hosea (Hos)', 'Joel (Joe)', 'Amos (Amo)',
        'Obadiah (Oba)', 'Jonah (Jon)', 'Micah (Mic)', 'Nahum (Nah)', 'Habakkuk (Hab)',
        'Zephaniah (Zep)', 'Haggai (Hag)', 'Zechariah (Zec)', 'Malachi (Mal)',
        'Matthew (Mat)', 'Mark (Mar)', 'Luke (Luk)', 'John (Joh)', 'Acts (Act)',
        'Romans (Rom)', '1 Corinthians (1Co)', '2 Corinthians (2Co)', 'Galatians (Gal)', 'Ephesians (Eph)',
        'Philippians (Phi)', 'Colossians (Col)', '1 Thessalonians (1Th)', '2 Thessalonians (2Th)', '1 Timothy (1Ti)',
        '2 Timothy (2Ti)', 'Titus (Tit)', 'Philemon (Phm)', 'Hebrews (Heb)', 'James (Jam)',
        '1 Peter (1Pe)', '2 Peter (2Pe)', '1 John (1Jo)', '2 John (2Jo)', '3 John (3Jo)',
        'Jude (Jud)', 'Revelation (Rev)'
    ]
    return f"Bible Books ({len(books)} total):\n\n" + "\n".join([f"{i+1:2d}. {book}" for i, book in enumerate(books)])

@mcp.resource("bible://translations")
def bible_translations() -> str:
    """Available Bible translations and their codes"""
    translations = {
        'KJV': 'King James Version (1769)',
        'ASV': 'American Standard Version (1901)',
        'BBE': 'Bible in Basic English (1965)',
        'WEB': 'World English Bible',
        'YLT': 'Youngs Literal Translation (1898)',
        'DARBY': 'Darby Translation (1890)'
    }
    return "Available Bible Translations:\n\n" + "\n".join([f"{code}: {name}" for code, name in translations.items()]) + "\n\nNote: Use the code (e.g., 'KJV') when specifying translation in tools."

@mcp.prompt()
def bible_study(topic_or_passage: str, study_level: str) -> str:
    """Generate a comprehensive Bible study guide for a given topic or passage

    Args:
        topic_or_passage: Bible topic (e.g., 'love', 'faith') or specific passage (e.g., 'Romans 8:28')
        study_level: Study depth level: 'basic', 'intermediate', or 'advanced'
    """
    return f"""Create a comprehensive Bible study guide for: {topic_or_passage}

Study Level: {study_level}

Please include:
1. **Key Verses**: 3-5 relevant Bible verses with references
2. **Context**: Historical and cultural background
3. **Main Themes**: Core theological concepts
4. **Application**: How this applies to modern life
5. **Discussion Questions**: 3-4 thought-provoking questions
6. **Prayer Points**: Suggested areas for prayer
7. **Further Study**: Related passages or topics to explore

Make this study guide practical and accessible for personal or group study."""

@mcp.prompt()
def daily_reflection(verse_or_theme: str, focus_area: str) -> str:
    """Create a daily devotional reflection based on a Bible verse or theme

    Args:
        verse_or_theme: Bible verse reference or spiritual theme for reflection
        focus_area: Life area to focus on: 'spiritual growth', 'relationships', 'challenges', 'gratitude', etc.
    """
    return f"""Daily Devotional Reflection

**Scripture Focus**: {verse_or_theme}
**Life Focus**: {focus_area}

Create a meaningful daily devotional that includes:

1. **Opening Prayer**: A brief prayer to center the heart
2. **Scripture Reading**: The full text of the verse(s)
3. **Reflection**: 2-3 paragraphs exploring the meaning and relevance
4. **Personal Application**: Specific ways to apply this truth today
5. **Closing Prayer**: A prayer incorporating the day's lesson
6. **Action Step**: One concrete step to take today

Write this in a warm, encouraging tone that speaks to both heart and mind. Make it practical for someone's daily walk with God."""

if __name__ == "__main__":
    # Run with SSE transport for remote hosting
    # Railway will set the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
