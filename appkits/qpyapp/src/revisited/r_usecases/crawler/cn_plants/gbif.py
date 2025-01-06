import requests
from typing import Dict, Optional
from urllib.parse import quote


def fetch_gbif_occurrences(species_name: str) -> Dict:
    """
    从GBIF获取物种分布数据

    Parameters:
        species_name: 物种名称
    """
    try:
        # 构建URL
        base_url = 'https://www.gbif.org/api/occurrence/search'

        # 查询参数
        params = {
            'advanced': 'false',
            'country': 'CN',
            'dwca_extension.facetLimit': '1000',
            'facet': [
                'establishment_means',
                'basis_of_record',
                'iucn_red_list_category',
                'month',
                'type_status',
                'issue',
                'dwca_extension',
                'dataset_key',
                'institution_code',
                'country',
                'continent',
                'media_type',
                'license',
                'protocol',
                'lifeStage',
                'establishmentMeans',
                'pathway',
                'degreeOfEstablishment',
                'publishing_org',
                'gbif_region',
                'published_by_gbif_region',
                'sex'
            ],
            'has_coordinate': 'true',
            'has_geospatial_issue': 'false',
            'issue.facetLimit': '1000',
            'locale': 'en',
            'month.facetLimit': '12',
            'occurrence_status': 'present',
            'q': species_name,
            'type_status.facetLimit': '1000'
        }

        # 请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'https://www.gbif.org/occurrence/search?q={quote(species_name)}&country=CN&has_coordinate=true&has_geospatial_issue=false&occurrence_status=present',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }

        # 发送请求
        response = requests.get(
            base_url,
            params=params,
            headers=headers
        )

        # 检查响应状态
        response.raise_for_status()
        one = response.json()['results'][0]
        # 返回JSON数据
        return one["decimalLatitude"], one["decimalLongitude"]

    except Exception as e:
        print(f"解析JSON出错: {e}")
        return 0, 0


# 使用示例
if __name__ == "__main__":
    # 获取物种分布数据
    with open('all_names.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            name = line.replace("\n","").strip()
            la, lo = fetch_gbif_occurrences(line.replace("\n","").strip())
            print(",".join([name, str(la), str(lo)]))
            with open("la_lo.csv", 'a') as f:
                f.write(",".join([name, str(la), str(lo)]) + "\n")
