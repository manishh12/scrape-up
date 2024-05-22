class Glassdoor:
    """
    Create an object for the 'Glassdoor' class :\n
    ```python
    scraper = Glassdoor()
    ```
    | Methods              | Details                                                                     |
    | ---------------------| --------------------------------------------------------------------------- |
    | `.jobs(query, location, num_pages)`    | Scrapes and returns a list of dictionaries representing job listings.        |
    | `.internships(query, location, num_pages)`    | Scrapes and returns a list of dictionaries representing internship listings.        |
    """

    def __init__(self, search_type: str, *, config: RequestConfig = RequestConfig()):
        self.base_url = "https://www.glassdoor.com/"
        self.search_type = search_type
        self.config = config

    def __scrape_page(self, url: str):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while fetching the page: {str(e)}")

    def __parse_page(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            return soup
        except Exception as e:
            raise Exception(f"An error occurred while parsing the page: {str(e)}")

    def jobs(self, query, location, num_pages=5):
        """
        Fetches the job listings.\n
        Args:
        - query (str): The job title or keyword to search for.
        - location (str): The location to search for jobs.
        - num_pages (int): Number of pages to scrape. Defaults to 5.

        Returns:
        - dict: A dictionary with job listings.
        """
        base_url = f"{self.base_url}Job/jobs.htm"
        job_listings = {}

        for page in range(1, num_pages + 1):
            url = f"{base_url}?q={query}&l={location}&p={page}"
            page_content = self.__scrape_page(url)
            if page_content:
                soup = self.__parse_page(page_content)
                job_listings[page] = self.__extract_job_details(soup.find_all("div", class_="jobContainer"))
            else:
                print(f"Failed to fetch content from {url}")

        return job_listings

    def __extract_job_details(self, job_listings):
        job_details = []
        for job in job_listings:
            title = job.find("a", class_="jobLink").text
            company = job.find("div", class_="jobInfoItem jobEmpolyerName").text.strip()
            location = job.find("span", class_="jobInfoItem jobLocation").text.strip()
            salary_estimate = job.find("span", class_="jobInfoItem jobSalaryEstimate")
            if salary_estimate:
                salary_estimate = salary_estimate.text.strip()
            else:
                salary_estimate = "Not provided"
            job_details.append({"title": title, "company": company, "location": location, "salary_estimate": salary_estimate})
        return job_details

    def internships(self, query, location, num_pages=5):
        """
        Fetches the internship listings.\n
        Args:
        - query (str): The internship title or keyword to search for.
        - location (str): The location to search for internships.
        - num_pages (int): Number of pages to scrape. Defaults to 5.

        Returns:
        - dict: A dictionary with internship listings.
        """
        base_url = f"{self.base_url}Job/india-internship-jobs-SRCH_IL.0,5_IN115_KO6,16.htm"
        internships = {}

        for page in range(1, num_pages + 1):
            url = f"{base_url}?p={page}"
            page_content = self.__scrape_page(url)
            if page_content:
                soup = self.__parse_page(page_content)
                internship_listings = soup.find_all("li", class_="jl")
                internships[page] = []
                for internship in internship_listings:
                    title = internship.find("div", class_="jobTitle").text.strip()
                    company = internship.find("div", class_="jobEmployerName").text.strip()
                    location = internship.find("span", class_="loc").text.strip()
                    stipend = internship.find("div", class_="jobStipend").text.strip()
                    internships[page].append({"title": title, "company": company, "location": location, "stipend": stipend})
            else:
                print(f"Failed to fetch content from {url}")

        return internships
