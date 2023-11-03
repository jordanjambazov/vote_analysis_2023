import glob
import re
from collections import defaultdict
from lxml import html

def extract_data_from_html(content, xpath_expression):
    tree = html.fromstring(content)
    return tree.xpath(xpath_expression)

def extract_row_value(content, lookup):
    res = extract_data_from_html(
        content,
        f'//table[@class="table"]//tr[td[contains(text(), "{lookup}")]]/td[2]'
    )
    assert len(res) == 1
    return convert_to_int(res[0].text)


def convert_to_int(text):
    cleaned_text = re.sub(r'[^\d]', '', text)
    return int(cleaned_text)

vote_regions = defaultdict(dict)

for file_path in glob.glob('raw/1_*_ik.html'):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    vote_region = int(file_path.split('_')[1])
    vote_region_name = extract_data_from_html(content, '//*[@id="main"]/h3[5]')[0].text
    i1_voters_in_lists_count = extract_row_value(content, "1. Брой на избирателите в избирателните списъци при предаването им на СИК")
    i5_found_bulletins = extract_row_value(content, "5. Брой на намерените в избирателните кутии хартиени бюлетини")
    i6_invalid_bulletins = extract_row_value(content, "6. Брой на намерените в избирателните кутии недействителни гласове (бюлетини)")

    invalid_ratio = i6_invalid_bulletins / i5_found_bulletins
    activity_ratio = i5_found_bulletins / i1_voters_in_lists_count

    vote_regions[vote_region]["vote_region_name"] = vote_region_name
    vote_regions[vote_region]["i1_voters_in_lists_count"] = i1_voters_in_lists_count
    vote_regions[vote_region]["i5_found_bulletins"] = i5_found_bulletins
    vote_regions[vote_region]["i6_invalid_bulletins"] = i6_invalid_bulletins
    vote_regions[vote_region]["invalid_ratio"] = invalid_ratio
    vote_regions[vote_region]["activity_ratio"] = activity_ratio

sorted_regions = sorted(
    vote_regions.values(),
    key=lambda ik: ik["invalid_ratio"]
)
for region in sorted_regions:
    invalid_percentage = round(region["invalid_ratio"] * 100, 2)
    activity_percentage = round(region["activity_ratio"] * 100, 2)
    print(
        "| " +
        region["vote_region_name"].ljust(50) + " | " +
        str(region["i1_voters_in_lists_count"]).ljust(25) + " | " +
        str(region["i6_invalid_bulletins"]).ljust(25) + " | " +
        str(activity_percentage).ljust(25) + " | " +
        str(invalid_percentage).ljust(25) + " | "
    )
