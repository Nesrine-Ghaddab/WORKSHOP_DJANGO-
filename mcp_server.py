import os
import sys
import django
import logging
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Setup logging for debugging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Configure Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Workshop.settings")
django.setup()

# Import models after Django setup
from ConferenceApp.models import conference, submission
from SessionApp.models import Session

logger.info("Django models imported successfully")

mcp = FastMCP("Conference Assistant")
logger.info("FastMCP server initialized")

@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    @sync_to_async
    def _get_conferences():
        return list(conference.objects.all())
    
    conferences = await _get_conferences()
    if not conferences:
        return "No conferences found."
    return "\n".join([f"- {c.title} ({c.start_date} to {c.end_date})"
                      for c in conferences])
# Construit une chaîne formatée avec le nom et les dates de chaque conférence, séparées par des sauts de ligne.



@mcp.tool()
async def get_conference_details(title: str) -> str:
    """Get details of a specific conference by title."""
    @sync_to_async
    def _get_conference():
        try:
            return conference.objects.get(title__icontains=title)
        except conference.DoesNotExist:
            return None
        except conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conf = await _get_conference()
    if conf == "MULTIPLE":
        return f"Multiple conferences found matching '{title}'. Please be more specific."
    if not conf:
        return f"Conference '{title}' not found."
    return (
         f"Title: {conf.title}\n"
         f"Theme: {conf.get_theme_display()}\n"
         f"Location: {conf.location}\n"
         f"Dates: {conf.start_date} to {conf.end_date}\n"
         f"Description: {conf.description}"
    )



@mcp.tool()
async def list_sessions(conference_title: str) -> str:
    """List sessions for a specific conference."""
    @sync_to_async
    def _get_sessions():
        try:
            conf = conference.objects.get(title__icontains=conference_title)
            return list(conf.sessions.all()), conf
        except conference.DoesNotExist:
            return None, None
        except conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conf = await _get_sessions()
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_title}'. Please be more specific."
    if conf is None:
        return f"Conference '{conference_title}' not found."
    
    sessions = result
    if not sessions:
        return f"No sessions found for conference '{conf.title}'."
    
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time})\n"
            f"  Topic: {s.topic}"
        )
    return "\n".join(session_list)

# Create filter tool for conferences by theme or date
@mcp.tool()
async def filter_conferences(theme: str = None, start_date: str = None, end_date: str = None) -> str:
    """Filter conferences by theme or date range."""
    @sync_to_async
    def _filter():
        qs = conference.objects.all()
        if theme:
            qs = qs.filter(theme=theme)
        if start_date:
            qs = qs.filter(start_date__gte=start_date)
        if end_date:
            qs = qs.filter(end_date__lte=end_date)
        return list(qs)
    
    conferences = await _filter()
    if not conferences:
        return "No conferences found matching the criteria."
    
    result = []
    for c in conferences:
        result.append(f"- {c.title} ({c.theme}) | {c.start_date} to {c.end_date}")
    return "\n".join(result)


if __name__ == "__main__":
    try:
        logger.info("Starting MCP server on stdio transport...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error starting MCP server: {e}", exc_info=True)
        sys.exit(1)