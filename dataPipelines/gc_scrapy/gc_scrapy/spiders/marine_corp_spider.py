from time import sleep
import scrapy
import re

from dataPipelines.gc_scrapy.gc_scrapy.items import DocItem
from dataPipelines.gc_scrapy.gc_scrapy.GCSpider import GCSpider
from scrapy import signals
from pydispatch import dispatcher

# patterns to extract
type_pattern = re.compile("^[A-Z]+")
type_spc_pattern = re.compile("^[A-Z ]+")
num_pattern = re.compile("[0-9].*")
alpha_num_pattern = re.compile("[((A-Z-)?(0-9))].+")
part_pattern = re.compile(r"(PT(\s)?\d)|((_|\s)\d)")
url_pattern = re.compile("^https?://\\S+$")

# title patterns to remove
rm_date = r"(\d+[A-Z]{3}(\d{4}|\d{2}))"
rm_with = "(W/)|(WITH)|(W-)|(&#39;)|(AMP;)"
rm_idx = r"(/INDEX)|(.PDF)|( -)"
rm_canx = r"(\(|CANCEL|DTD|CANX|FORMER).+"
rm_spc = r"\s*[\n\t\r\s+]\s*"
rm_char = r"[^a-zA-Z0-9 ()\\-]"
rm_matches = "|".join([rm_date, rm_with, rm_idx, rm_canx])

url_re = re.compile("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                    "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")


def is_valid_url(url):
    if not url:
        return False
    try:
        return re.search(url_re, url)
    except:
        return False


general_num_re = re.compile(
    r"(?<!ch )(?<!vol )(?<!\W )(\d[\w\.\-]*)", flags=re.IGNORECASE)


def general_set_num(raw_data):
    doc_num = ""
    try:
        doc_type_num_raw = raw_data.get('doc_type_num_raw')
        doc_name_groups = re.search(general_num_re, doc_type_num_raw)

        if doc_name_groups:
            doc_num = doc_name_groups.group(1)
    except:
        pass
    finally:
        raw_data['doc_num'] = doc_num


def set_no_num(raw_data):
    raw_data['doc_num'] = ""


def set_type_using_num(raw_data):
    doc_type_num_raw = raw_data.get('doc_type_num_raw')
    doc_num = raw_data.get('doc_num')
    if doc_num:
        doc_type, *_ = doc_type_num_raw.partition(doc_num)
        raw_data['doc_type'] = doc_type.strip()
    else:
        use_raw_type(raw_data)

    # print(raw_data['doc_type'], ':', raw_data['doc_type_num_raw'])


def use_raw_type(raw_data):
    raw_data['doc_type'] = raw_data.get('doc_type_raw')


def name_from_type_and_num(raw_data):
    raw_data['doc_name'] = raw_data['doc_type'] + ' ' + raw_data['doc_num']


def name_from_type_and_num_no_space(raw_data):
    raw_data['doc_name'] = raw_data['doc_type'] + raw_data['doc_num']


def name_from_type_and_num_with_dash(raw_data):
    raw_data['doc_name'] = raw_data['doc_type'] + '-' + raw_data['doc_num']


def name_from_doc_type_num_raw(raw_data):
    raw_data['doc_name'] = raw_data['doc_type_num_raw']


def name_from_title(raw_data):
    raw_data['doc_name'] = raw_data['doc_title_raw']


def name_from_type_title(raw_data):
    raw_data['doc_name'] = raw_data['doc_type_raw'] + \
        ": " + raw_data['doc_title_raw']


def set_all_transformations(raw_data, transform_dict):
    set_num_func = transform_dict.get(
        "set_num_func")
    set_type_func = transform_dict.get(
        "set_type_func")
    set_doc_name_func = transform_dict.get(
        "set_doc_name_func")

    set_num_func(raw_data)
    set_type_func(raw_data)
    set_doc_name_func(raw_data)


dcg_re = re.compile(r'DCG (VOL \d* PGS \d*\-\d*)')


def legal_pubs_set_num(raw_data):
    raw_data['doc_num'] = ""
    if 'DCG VOL' in raw_data['doc_type_num_raw']:
        groups = re.search(dcg_re, raw_data['doc_type_num_raw'])
        if groups:
            raw_data['doc_num'] = groups.group(1)
    elif 'MANUAL FOR COURTS-MARTIAL' in raw_data['doc_type_num_raw']:
        raw_data['doc_num'] = ""
    else:
        general_set_num(raw_data)


def legal_pubs_set_name(raw_data):
    if raw_data['doc_num']:
        name_from_type_and_num(raw_data)
    else:
        name_from_title(raw_data)


irm_re = re.compile(r'IRM\-?(\w*\-\w*)')


def misc_pubs_set_num(raw_data):
    doc_type_num_raw = raw_data['doc_type_num_raw']
    raw_data['doc_num'] = ""
    if 'IRM ' in doc_type_num_raw or 'IRM-' in doc_type_num_raw:
        groups = re.search(irm_re, doc_type_num_raw)
        if groups:
            raw_data['doc_num'] = groups.group(1)
    elif 'MCCP' in doc_type_num_raw or 'CMC White Letter' in doc_type_num_raw:
        general_set_num(raw_data)
    else:
        set_no_num(raw_data)


def misc_pubs_set_type(raw_data):
    if 'IRM' in raw_data['doc_type_num_raw']:
        raw_data['doc_type'] = 'IRM'
    else:
        set_type_using_num(raw_data)


def misc_pubs_set_name(raw_data):
    if raw_data['doc_num']:
        if 'IRM' in raw_data['doc_type_num_raw']:
            name_from_type_and_num_with_dash(raw_data)
        else:
            name_from_type_and_num(raw_data)
    else:
        name_from_title(raw_data)


secnavm_re = re.compile(r'SECNAV M\-?(\w*\.?\w*)')


def navy_pubs_set_num(raw_data):
    raw_data['doc_num'] = ""
    if 'SECNAV M-' in raw_data['doc_type_num_raw']:
        groups = re.search(secnavm_re, raw_data['doc_type_num_raw'])
        if groups:
            raw_data['doc_num'] = groups.group(1).replace('-', '')
    else:
        general_set_num(raw_data)


def navy_pubs_set_type(raw_data):
    if 'SECNAV M-' in raw_data['doc_type_num_raw']:
        print('++++++ setting SECNAV M')
        raw_data['doc_type'] = 'SECNAV M'
    else:
        set_type_using_num(raw_data)


def navy_pubs_set_name(raw_data):
    if raw_data['doc_num']:
        if 'SECNAV M-' in raw_data['doc_type_num_raw']:
            name_from_type_and_num_with_dash(raw_data)
        elif 'NAVSUP P' in raw_data['doc_type_num_raw']:
            name_from_type_and_num_no_space(raw_data)
        else:
            name_from_type_and_num(raw_data)
    else:
        name_from_title(raw_data)


standard_funcs = {
    "set_num_func": general_set_num,
    "set_type_func": set_type_using_num,
    "set_doc_name_func": name_from_type_and_num,
}


# each doc type has so many exceptions, most need specific rules
doc_type_transformations_map = {
    "Army Pubs": standard_funcs,
    "Doctrine Pubs": standard_funcs,
    "Historical": {
        "set_num_func": set_no_num,
        "set_type_func": use_raw_type,
        "set_doc_name_func": name_from_type_title,
    },
    "Legal Pubs": {
        "set_num_func": legal_pubs_set_num,
        "set_type_func": set_type_using_num,
        "set_doc_name_func": legal_pubs_set_name,
    },
    "MCBUL": {
        "set_num_func": general_set_num,
        "set_type_func": set_type_using_num,
        "set_doc_name_func": name_from_type_and_num,
    },
    "MCO": standard_funcs,
    "MCO P": {
        "set_num_func": general_set_num,
        "set_type_func": set_type_using_num,
        "set_doc_name_func": name_from_type_and_num_no_space,
    },
    "Misc Pubs": {
        "set_num_func": misc_pubs_set_num,
        "set_type_func": misc_pubs_set_type,
        "set_doc_name_func": misc_pubs_set_name,
    },
    "NAVMC": standard_funcs,
    "NAVMC Directive": standard_funcs,
    "Navy Pubs": {
        "set_num_func": navy_pubs_set_num,
        "set_type_func": navy_pubs_set_type,
        "set_doc_name_func": navy_pubs_set_name,
    },
    "UM": {
        "set_num_func": set_no_num,
        "set_type_func": use_raw_type,
        "set_doc_name_func": name_from_type_title,
    },
    "USAF Pubs": standard_funcs,
}


class MarineCorpSpider(GCSpider):
    """
        Parser for Marine Corp EPEL
    """

    def __init__(self):
        dispatcher.connect(self.spider_did_close, signals.spider_closed)

    def spider_did_close(self, spider):
        # import json
        print('SPIDER CLOSED\n\n\n')
        # with open('doc_types.json', 'w') as f:
        #     f.writelines(json.dumps(self.doc_types))
        # print(self.doc_types)
        # print('NO reTITLE')
        # for l in spider.skipped["title"]:
        #     print(l)

        # print('\n\n No NUM')
        # for l in spider.skipped["num"]:
        #     print(l)
        print("\n\n NO PDF LINK")
        for l in spider.skipped["no_link"]:
            print(l)

        print("\n\n INVALID LINK")
        for l in spider.skipped["pdf_link"]:
            print(l)

    # def close(self, reason):
    #     print('reason', reason)

    name = "marine_pubs"
    allowed_domains = ['marines.mil']
    base_url = 'https://www.marines.mil/News/Publications/MCPEL/?Page='
    current_page = 1
    start_urls = [
        f"{base_url}{current_page}"
    ]
    cac_login_required = False
    file_type = "pdf"

    skipped = {
        "title": [],
        "pdf_link": [],
        "no_link": [],
        "num": []
    }

    doc_types = {}

    def parse(self, response):
        try:
            source_page_url = response.url
            # print('REQUESTING FROM', source_page_url)
            rows = response.css('div.alist-more-here div.litem')

            if not rows:
                print('response has no rows, done', rows)
                return

            for row in rows:
                try:
                    follow_href = row.css('a::attr(href)').get()

                    doc_type_raw = row.css(
                        'div.list-type span::text').get(default="")
                    doc_type_num_raw = row.css(
                        'div.list-title::text').get(default="")
                    doc_title_raw = row.css(
                        'div.cat span::text').get(default="")
                    doc_status_raw = row.css(
                        'div.status::text').get(default="")

                    if not doc_type_raw:
                        continue
                    if not doc_type_raw in doc_type_transformations_map:
                        print('!!!!!!!! skipped - UNKNOWN type', doc_type_num_raw)
                        continue
                    if doc_status_raw == 'Deleted':
                        # print('skipped - deleted', doc_type_num_raw)
                        continue
                    if not follow_href:
                        # print('skipped - no follow_href', doc_type_num_raw)
                        continue

                    raw_data = {
                        "doc_type_raw": doc_type_raw,
                        "doc_type_num_raw": doc_type_num_raw,
                        "doc_title_raw": doc_title_raw
                    }

                    # each doc type has ways to parse it defined in doc_type_transformations_map
                    transformations = doc_type_transformations_map[doc_type_raw]
                    # mutably sets keys on raw_data dict
                    set_all_transformations(raw_data, transformations)

                    version_hash_fields = {
                        "status": doc_status_raw
                    }

                    doc_title = self.ascii_clean(doc_title_raw)
                    print(raw_data['doc_type'], ':',
                          raw_data['doc_num'], '-- from', doc_type_num_raw)
                    incomplete_item = {
                        "item": DocItem(
                            doc_name=raw_data['doc_name'],
                            doc_num=raw_data['doc_num'],
                            doc_type=raw_data['doc_type'],
                            doc_title=doc_title,
                            source_page_url=source_page_url,
                            version_hash_raw_data=version_hash_fields,
                        )
                    }

                    # follow href to get downloadable item link, pass in parts of item from table
                    yield scrapy.Request(
                        follow_href, callback=self.parse_download_page, meta=incomplete_item)
                except Exception as e:
                    print('ERROR', type(e), e)
                    return

            try:
                # increment page and send next request
                self.current_page = self.current_page + 1
                next_url = f"{self.base_url}{self.current_page}"
                # print('next url', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)

    def parse_download_page(self, response):
        # print('page response', response)
        doc_item = response.meta["item"]
        # href_raw = response.css(
        #     'div.download-section a::attr(href)').get(default="")
        # if not href_raw:
        #     href_raw = response.css(
        #         'div.body-text p:nth-child(3)::text').get(default="")
        # if not href_raw:
        #     href_raw = response.css()
        href_raw = response.css(
            'div.download-section a::attr(href)').get(default="")
        if not href_raw:
            href_raw = response.css(
                'div.body-text a::attr(href)').get(default="")
        if not href_raw:
            texts = response.css('div.body-text *::text').getall()
            href_texts = [x for x in texts if url_re.match(x)]
            if len(href_texts):
                href_raw = href_texts[0]

        # try to repair some broken hrefs
        href_raw = href_raw.replace('http:/www./', 'http://www.')
        if not href_raw:
            print('NO HREF AT ALL')
            self.skipped["no_link"].append((doc_item['doc_name'], href_raw))
            # print(doc_item['doc_name'], 'no href, returning')
            return

        if not is_valid_url(href_raw):
            print('NOT VALID URL ', href_raw, doc_item['doc_name'])
            self.skipped["pdf_link"].append((doc_item['doc_name'], href_raw))
            # print(doc_item['doc_name'], 'no href, returning')
            return

        doc_item['version_hash_raw_data'].update({
            "item_currency": href_raw
        })

        doc_type = self.get_href_file_extension(href_raw)
        web_url = self.url_encode_spaces(href_raw)

        doc_item['downloadable_items'] = [
            {
                "doc_type": doc_type,
                "web_url": web_url,
                "compression_type": None
            }
        ]

        yield doc_item
