from enum import Enum

from pydantic import BaseModel


class GithubSearchModel(BaseModel):
    keyword_search_url: str = "https://api.github.com/search/repositories?q="
    topic_search_url: str = (
        "https://api.github.com/search/repositories?q=topic:{topic}+is:featured"
    )
    github_base_url: str = "https://github.com"

    def keyword_url(self, keyword: str) -> str:
        return self.keyword_search_url + keyword

    def topic_url(self, topic: str) -> str:
        return self.topic_search_url.format(topic=topic)


class GoogleSearchMode(Enum):
    ARTICLES = "articles"
    COURSES = "courses"
    BOOKS = "books"
    RESEARCH = "research"
    PODCASTS = "podcasts"
    VIDEOS = "videos"
    TOOLS_SOFTWARE = "tools_software"
    CONFERENCES_EVENTS = "conferences_events"
    SLIDES_PRESENTATIONS = "slides_presentations"


websites_to_search_articles = [
    "medium.com",  # Medium
    "dev.to",  # The DEV Community
    "hackernoon.com",  # Hacker Noon
    "smashingmagazine.com",  # Smashing Magazine
    "alistapart.com",  # A List Apart
    "dzone.com",  # DZone
    "infoq.com",  # InfoQ
    "tutsplus.com",  # Tuts+ (from Envato Tuts+)
    "css-tricks.com",  # CSS-Tricks
    "sitepoint.com",  # SitePoint
    "tympanus.net/codrops",  # Codrops
    "realpython.com",  # Real Python
    "freecodecamp.org/news",  # Freecodecamp News
    "towardsdatascience.com",  # Towards Data Science (Medium's Data Science community)
    "arxiv.org",  # arXiv (Research Papers in AI, ML, CS, etc.)
    "ai.googleblog.com",  # Google AI Blog
    "blogs.nvidia.com",  # NVIDIA Blog (AI, Deep Learning)
    "distill.pub",  # Distill (ML Visualization)
    "deepmind.com/blog",  # DeepMind Blog
    "openai.com/blog",  # OpenAI Blog
    "neuralink.com/blog",  # Neuralink Blog
    "research.fb.com",  # Facebook AI Research Blog
    "research.google",  # Google Research Publications
    "blogs.microsoft.com/ai",  # Microsoft AI Blog
    "blog.tensorflow.org",  # TensorFlow Blog
    "pytorch.org/blog",  # PyTorch Blog
    "blog.ycombinator.com",  # Y Combinator Blog (Startups, Tech News)
    "thenewstack.io",  # The New Stack (Cloud, Containers, etc.)
    "overleaf.com/learn",  # Overleaf (LaTeX, Research Writing)
    "geeksforgeeks.org",  # GeeksforGeeks (CS, Algorithms, Tutorials)
    "stackoverflow.blog",  # Stack Overflow Blog
    "martinfowler.com",  # Martin Fowler's Blog (Software Design, Patterns)
    "acm.org/technews",  # ACM TechNews
    "spectrum.ieee.org/computing",  # IEEE Spectrum's computing section
]

websites_to_search_courses = [
    "udemy.com",
    "coursera.org",
    "edx.org",
    "pluralsight.com",
    "khanacademy.org",
    "lynda.com",
    "udacity.com",
    "codecademy.com",
    "futurelearn.com",
    "skillshare.com" "linkedin.com/learning",
]

websites_to_search_books = [
    "amazon.com",
    "goodreads.com",
    "barnesandnoble.com",
    "books.google.com",
    "bookdepository.com",
    "powells.com",
    "abebooks.com",
    "springer.com",
    "oreilly.com",
    "packtpub.com",
]

websites_to_search_research = [
    "scholar.google.com",
    "semanticscholar.org",
    "jstor.org",
    "springer.com",
    "ieee.org",
    "sciencedirect.com",
    "researchgate.net",
    "pubmed.ncbi.nlm.nih.gov",
    "arxiv.org",
    "ncbi.nlm.nih.gov",
]

websites_to_search_podcasts = [
    "anchor.fm",
    "stitcher.com",
    "podbean.com",
    "spotify.com",
    "itunes.apple.com",
    "podbay.fm",
    "podtail.com",
    "podcasts.apple.com",
    "player.fm",
    "overcast.fm",
]

websites_to_search_videos = [
    "youtube.com",
    "vimeo.com",
    "twitch.tv",
    "ted.com",
    "dailymotion.com",
]

websites_to_search_tools_software = [
    "alternativeto.net",
    "producthunt.com",
    "capterra.com",
    "sourceforge.net",
    "softpedia.com",
    "g2.com",
]

websites_to_search_conferences_or_events = [
    "eventbrite.com",
    "meetup.com",
    "10times.com",
    "conferenceseries.com",
    "techmeme.com/events",  # for tech-related events
    "lanyrd.com",
]

websites_to_search_slides_or_presentations = [
    "slideshare.net",
    "speakerdeck.com",
    "academia.edu",  # Some researchers share their presentations here
    "prezi.com",
    "slideboom.com",
    "authorstream.com",
]

websites_to_search = {
    GoogleSearchMode.ARTICLES: websites_to_search_articles,
    GoogleSearchMode.COURSES: websites_to_search_courses,
    GoogleSearchMode.BOOKS: websites_to_search_books,
    GoogleSearchMode.RESEARCH: websites_to_search_research,
    GoogleSearchMode.PODCASTS: websites_to_search_podcasts,
    GoogleSearchMode.VIDEOS: websites_to_search_videos,
    GoogleSearchMode.TOOLS_SOFTWARE: websites_to_search_tools_software,
    GoogleSearchMode.CONFERENCES_EVENTS: websites_to_search_conferences_or_events,
    GoogleSearchMode.SLIDES_PRESENTATIONS: websites_to_search_slides_or_presentations,
}

terms_to_search = {
    GoogleSearchMode.ARTICLES: "(article OR blog OR tutorial OR guide OR post)",
    GoogleSearchMode.COURSES: "(course OR tutorial OR class OR certification OR training)",
    GoogleSearchMode.BOOKS: "(book OR ebook OR textbook OR manual)",
    GoogleSearchMode.RESEARCH: "(paper OR article OR publication OR study OR research)",
    GoogleSearchMode.PODCASTS: "(podcast OR episode OR show OR series OR audio)",
    GoogleSearchMode.VIDEOS: "(video OR lecture OR webinar)",
    GoogleSearchMode.TOOLS_SOFTWARE: "(software OR tool OR utility OR app OR platform OR service)",
    GoogleSearchMode.CONFERENCES_EVENTS: "(conference OR event OR workshop OR seminar OR symposium OR tech talk)",
    GoogleSearchMode.SLIDES_PRESENTATIONS: "(slides OR presentation OR deck OR ppt OR powerpoint OR keynote)",
}
