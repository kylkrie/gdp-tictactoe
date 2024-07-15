from .routes import router

# only expose the router
# keep api code contained in the api module
__all__ = ['router']
