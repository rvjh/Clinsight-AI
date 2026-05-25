import requests
import xml.etree.ElementTree as ET


def fetch_pubmed_articles_with_metadata(
    query: str,
    max_results: int = 3,
    use_mock_if_empty: bool = True
):
    """
    Fetch PubMed articles and extract metadata.

    Args:
        query (str): PubMed search query
        max_results (int): Number of articles to fetch
        use_mock_if_empty (bool): Return mock data if no results found

    Returns:
        list: List of article metadata dictionaries
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        # -----------------------------------
        # STEP 1: SEARCH PUBMED
        # -----------------------------------
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }

        search_response = requests.get(
            search_url,
            params=search_params,
            headers=headers,
            timeout=10
        )

        search_response.raise_for_status()

        search_json = search_response.json()

        id_list = search_json["esearchresult"]["idlist"]

        print(f"Found PubMed IDs: {id_list}")

        if not id_list:
            raise ValueError("No articles found")

        ids = ",".join(id_list)

        # -----------------------------------
        # STEP 2: FETCH ARTICLE DETAILS
        # -----------------------------------
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

        fetch_params = {
            "db": "pubmed",
            "id": ids,
            "retmode": "xml"
        }

        fetch_response = requests.get(
            fetch_url,
            params=fetch_params,
            headers=headers,
            timeout=10
        )

        fetch_response.raise_for_status()

        xml_data = fetch_response.text

        # -----------------------------------
        # STEP 3: PARSE XML RESPONSE
        # -----------------------------------
        root = ET.fromstring(xml_data)

        articles = []

        for article in root.findall(".//PubmedArticle"):

            # PMID
            pmid = article.findtext(".//PMID", default="N/A")

            # Title
            title = article.findtext(".//ArticleTitle", default="N/A")

            # Abstract
            abstract_parts = article.findall(".//AbstractText")

            abstract = " ".join(
                [part.text.strip() for part in abstract_parts if part.text]
            )

            if not abstract:
                abstract = "No abstract available"

            # Journal
            journal = article.findtext(".//Journal/Title", default="N/A")

            # Publication Year
            publication_year = article.findtext(
                ".//PubDate/Year",
                default="N/A"
            )

            # Authors
            authors = []

            for author in article.findall(".//Author"):

                firstname = author.findtext("ForeName", default="")
                lastname = author.findtext("LastName", default="")

                full_name = f"{firstname} {lastname}".strip()

                if full_name:
                    authors.append(full_name)

            # DOI
            doi = "N/A"

            for article_id in article.findall(".//ArticleId"):

                if article_id.attrib.get("IdType") == "doi":
                    doi = article_id.text
                    break

            # PubMed URL
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            # Store article metadata
            articles.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "publication_year": publication_year,
                "authors": authors,
                "doi": doi,
                "pubmed_url": pubmed_url
            })

        return articles

    except Exception as e:

        print(f"Error occurred: {e}")

        if use_mock_if_empty:

            return [
                {
                    "pmid": "000000",
                    "title": "Mock Article",
                    "abstract": "This is mock abstract data.",
                    "journal": "Mock Journal",
                    "publication_year": "2025",
                    "authors": ["John Doe"],
                    "doi": "10.000/mock",
                    "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/"
                }
            ]

        return []