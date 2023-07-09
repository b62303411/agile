from django.contrib import admin
from django.urls import path, include
import os
import sys
import logging

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AgileApp.urls')),
]
# Set up logging
logging.basicConfig(level=logging.INFO)

# Log available URL paths
for url in urlpatterns:
    if hasattr(url, 'url_patterns'):
        for included_url in url.url_patterns:
            logging.info(f"URL pattern: {included_url.pattern}")
    else:
        logging.info(f"URL pattern: {url.pattern}")