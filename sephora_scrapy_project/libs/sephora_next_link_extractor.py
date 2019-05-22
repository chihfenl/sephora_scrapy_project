from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

NEXT_PAGE_XPATH = \
        "//nav[@aria-label='Pagination']" + \
        "//button[@aria-label='Next' and @class='css-a8wls9 ']"


class SephoraNextLinkExtractor(LinkExtractor):

    def construct_next_page_url(self, response_url):

        splitted_url = response_url.split('=')
        url_without_page_num = splitted_url[0]
        current_page_num = int(splitted_url[-1])
        next_page_url = ''.join(
            [url_without_page_num, '=', str(current_page_num + 1)]
        )

        return next_page_url

    # Override parent's _extract_links function
    def _extract_links(
        self, selector, response_url, response_encoding, base_url=None
    ):
        result = []
        is_multi_page = selector.xpath(NEXT_PAGE_XPATH)
        if is_multi_page:
            if 'currentPage' not in response_url:
                response_url += "?currentPage=1"
            next_page_url = self.construct_next_page_url(response_url)
            result.append(Link(next_page_url, u'', nofollow=False))
        return result
