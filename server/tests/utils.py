"""
Utilities for use by the unit tests
"""
from datetime import datetime
import server.services.demos as demo_service


def create_demo():
    """Creates a demo object for a unit test class"""
    return demo_service.create_demo(datetime.now().isoformat("T"))


def delete_demo(demo_guid):
    """Deletes the demo object used by a unit test class"""
    demo_service.delete_demo_by_guid(demo_guid)


def get_bad_token():
    """Returns an invalid loopback token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJu" \
           "YW1lIjoiU3VwcGx5IENoYWluIE1hbmFnZXIgKG1kcTNRMEZDYlEpIiwiZ" \
           "GVtb0lkIjoiN2U3ZjQ1ZTA1ZTQyNTFiNWFjZDBiMTlmYTRlZDI5OTIiLC" \
           "JlbWFpbCI6ImNocmlzLm1kcTNRMEZDYlFAYWNtZS5jb20iLCJyb2xlcyI" \
           "6W3siY3JlYXRlZCI6IjIwMTYtMDYtMDFUMTE6MTU6MzQuNTE1WiIsImlk" \
           "IjoiM2RlZjE0MzZlYjUxZTQzOWU3ZmI1MDA5ZmVjM2EwZWIiLCJtb2RpZ" \
           "mllZCI6IjIwMTYtMDYtMDFUMTE6MTU6MzQuNTE1WiIsIm5hbWUiOiJzdX" \
           "BwbHljaGFpbm1hbmFnZXIifV0sImlkIjoiN2U3ZjQ1ZTA1ZTQyNTFiNWF" \
           "jZDBiMTlmYTRlZDQ3OTAifSwiZXhwIjoxNDY2MDQ1MzczLCJsb29wYmFj" \
           "a190b2tlbiI6ImhFRnJzeGhSa3lBUEhQWWN0TWtEaE9mSTZOaDY5TlBzc" \
           "FhkRWhxWXVSTzBqZDBLem1HVkZFbnpRZVRwVTV2N28ifQ.I8_iqpK7pwY" \
           "5mmND220MhnsMDS5FtqRhtliEiXoMAGM"
