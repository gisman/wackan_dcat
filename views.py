from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
import requests
from wackan.ckan_search import CkanSearch


# Create your views here.
def dcat(request, name, format):
    """
    Fetches and returns the RDF representation of a dataset from a CKAN instance.

    Note: Requires the ckanext-dcat extension to be installed on the CKAN server (https://github.com/ckan/ckanext-dcat)

    Args:
        request (HttpRequest): The HTTP request object.
        name (str): The name of the dataset.
        format (str): The format of the dataset (e.g., 'rdf', 'ttl').

    Returns:
        HttpResponse: The HTTP response containing the dataset content with the appropriate content type.

    Raises:
        Http404: If the dataset does not exist or there is a request exception.
    """
    EXPOSED_CKAN_URL = CkanSearch(request).ckan_url()  # "https://catalog.gimi9.com"
    url = f"{EXPOSED_CKAN_URL}/dataset/{name}.{format}"

    try:
        response = requests.get(url, timeout=1)
        if response.status_code == 200:
            return HttpResponse(
                response.content, content_type=response.headers["Content-Type"]
            )
        else:
            raise Http404(f"Dataset {name} does not exist. {response.reason}")
    except requests.exceptions.RequestException as e:
        raise Http404(f"Dataset {name} does not exist")
