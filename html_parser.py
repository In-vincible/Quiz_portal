from urllib.request import urlopen
from lxml import html
import pandas as pd
import time
import argparse
import logging


class IndexNewsUpdates:
    URL = "https://www.stoxx.com/index-updates"
    NEWS_UPDATES_REGISTRY = set()

    @classmethod
    def fetch_index_update_html_node(cls):
        logging.critical(f'About to poll - {cls.URL}')
        # Fetch the HTML content from the URL
        response = urlopen(cls.URL)
        html_content = response.read().decode("utf-8")

        # Parse the HTML content using lxml
        tree = html.fromstring(html_content)

        # Use XPath to find elements
        custom_xpath = "//div[@class='latestannouncementca']//div[@class='latestannouncementca']"
        target_node = tree.xpath(custom_xpath)[0]
        return target_node

    @classmethod
    def extract_download_link(cls, col):
        col_children = col.getchildren()

        if len(col_children) == 0:
            return None
        a_tag = col.getchildren()[0]
        pdf_link = a_tag.get('href')
        pdf_link = None if pdf_link == '#' else pdf_link
        return pdf_link

    @classmethod
    def extract_row_info(cls, tr):
        cols = tr.getchildren()
        return {
            'date': cols[0].text_content(),
            'title': cols[1].text_content(),
            'download_en': cls.extract_download_link(cols[2]),
            'download_other': cls.extract_download_link(cols[3])
        }

    @classmethod
    def extract_all_rows_info(cls, target_node):
        all_content = []
        rows = target_node.findall('.//tr')
        for row in rows[1:]:
            all_content.append(cls.extract_row_info(row))
        
        df = pd.DataFrame(all_content)
        return df
    
    @classmethod
    def fetch_index_news_updates(cls):
        index_update_page_html = cls.fetch_index_update_html_node()
        all_news_updates = cls.extract_all_rows_info(index_update_page_html)
        return all_news_updates

    @classmethod
    def filter_out_new_updates(cls, all_updates):
        new_updates = []
        all_updates['key'] = all_updates['date'] + all_updates['title']
        for _, row in all_updates.iterrows():
            news_key = row['key']
            if news_key not in cls.NEWS_UPDATES_REGISTRY:
                # Register the update so that - it doesn't get caught next time
                cls.NEWS_UPDATES_REGISTRY.add(news_key)
                new_updates.append(row)
        return pd.DataFrame(new_updates)
    
    @classmethod
    def track_index_news_updates(cls, time_period_in_secs=15):
        while True:
            all_news_updates = cls.fetch_index_news_updates()
            new_news_updates = cls.filter_out_new_updates(all_news_updates)
            print(new_news_updates)
            time.sleep(time_period_in_secs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Read time period from args
    parser.add_argument('--time_period', type=int, default=300, help='Time span in secs at which we poll index updates website regularly.')
    args = parser.parse_args()

    IndexNewsUpdates.track_index_news_updates(args.time_period)
