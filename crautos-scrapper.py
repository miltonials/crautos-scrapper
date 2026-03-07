import asyncio
import httpx
import re
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import pandas as pd
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

@dataclass
class Car:
    id: str
    link: str
    name: str
    year: int
    CRC: Optional[float]
    USD: Optional[float]

class CrAutosScraper:
    def __init__(self, max_concurrent_requests: int = 10):
        self.base_url = 'https://crautos.com/autosusados/searchresults.cfm?c=03037'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    @staticmethod
    def _parse_price(content: str) -> dict:
        patron = r'(?:&cent;|\$)\s+([\d,]+)'
        precios = re.findall(patron, content)
        result = {"colones": None, "dolares": None}
        if len(precios) >= 2:
            if float(precios[0].replace(',', '')) < 1000000:
                result["dolares"] = float(precios[0].replace(',', ''))
                result["colones"] = float(precios[1].replace(',', ''))
            else:
                result["colones"] = float(precios[0].replace(',', ''))
                result["dolares"] = float(precios[1].replace(',', ''))
        return result

    @staticmethod
    def _parse_year(content: str) -> int:
        year = re.findall(r'(\d{4})&nbsp;', content)
        return int(year[-1]) if year else 0

    @staticmethod
    def _clean_numeric_value(key: str, value: str) -> tuple:
        if not isinstance(value, str):
            return key, value

        value = value.strip()
        match = re.match(r'^([\d,]+)\s*([a-zA-Z]*)$', value)
        if match:
            num_str = match.group(1).replace(',', '')
            unit = match.group(2).lower()

            try:
                num_val = int(num_str)
            except ValueError:
                return key, value

            if unit:
                return f"{key} ({unit})", num_val
            else:
                return key, num_val

        return key, value

    def _process_results(self, results) -> List[Car]:
        cars = []
        for i in range(3, len(results), 4):
            try:
                car_id = results[i][0]
                name = results[i-1][1].replace('&nbsp;', ' ').strip()
                if any(x in name.lower() for x in ['destacado', 'clasificados']):
                    continue

                price_data = self._parse_price(results[i][1])
                year = self._parse_year(results[i-3][1])

                cars.append(Car(
                    id=car_id,
                    link=f'https://crautos.com/autosusados/cardetail.cfm?c={car_id}',
                    name=name,
                    year=year,
                    CRC=price_data['colones'],
                    USD=price_data['dolares']
                ))
            except (IndexError, ValueError):
                continue
        return cars

    async def fetch_page(self, client: httpx.AsyncClient, page: int) -> List[Car]:
        payload = {
            'brand': '00', 'financed': '00', 'yearfrom': '2010', 'yearto': '2026',
            'pricefrom': '100000', 'priceto': '800000000', 'style': '00',
            'province': '0', 'doors': '0', 'orderby': '0', 'newused': '1',
            'fuel': '0', 'trans': '0', 'recibe': '0', 'modelstr': '',
            'totalads': '0', 'p': str(page)
        }

        async with self.semaphore:
            try:
                response = await client.post(self.base_url, data=payload, timeout=20.0)
                response.raise_for_status()
                html = response.content.decode('utf-8', errors='replace').replace('\n', ' ')
                results = re.findall(r'<a href="cardetail.cfm\?c=(\d+)">(.*?)<\/a>', html)
                if not results:
                    return []
                return self._process_results(results)
            except Exception:
                return []

    async def fetch_car_details(self, client: httpx.AsyncClient, car: Car) -> Dict:
        url = f"https://crautos.com/autosusados/extract.cfm?c={car.id}"
        data = asdict(car)

        async with self.semaphore:
            try:
                response = await client.get(url, timeout=20.0)
                response.raise_for_status()

                html_content = response.content.decode('utf-8', errors='replace')
                soup = BeautifulSoup(html_content, 'html.parser')

                gen_info_tab = soup.find('div', id='tab-1')
                if gen_info_tab:
                    for row in gen_info_tab.find_all('tr'):
                        cols = row.find_all('td')
                        if len(cols) == 2:
                            key = cols[0].get_text(strip=True)
                            val = cols[1].get_text(strip=True).replace('\xa0', ' ')
                            if key != "Información General":
                                clean_key, clean_val = self._clean_numeric_value(key, val)
                                data[clean_key] = clean_val
                        elif len(cols) == 1:
                            text = cols[0].get_text(strip=True)
                            if text and text != "Información General":
                                data['Notas'] = text

                equip_tab = soup.find('div', id='tab-2')
                if equip_tab:
                    equip_text = equip_tab.get_text(separator="|", strip=True)
                    items = [item.strip() for item in equip_text.split('|') if len(item.strip()) > 2 and item != "Equipamiento"]
                    data['Equipamiento'] = ", ".join(items)

            except Exception:
                pass 

        return data

    async def run(self, total_pages: int):
        async with httpx.AsyncClient(headers=self.headers) as client:
            print(f"\n[FASE 1/2] Obteniendo lista base de carros ({total_pages} páginas)...")
            tasks = [self.fetch_page(client, p) for p in range(1, total_pages + 1)]
            
            pages_results = []
            for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Páginas Procesadas"):
                pages_results.append(await f)
                
            all_cars = [car for sublist in pages_results for car in sublist]

            if not all_cars:
                print("No se encontraron carros. Verifica tu conexión o el rango de páginas.")
                return pd.DataFrame()

            print(f"\n[FASE 2/2] Se encontraron {len(all_cars)} carros. Extrayendo especificaciones detalladas...")
            detail_tasks = [self.fetch_car_details(client, car) for car in all_cars]
            
            detailed_cars = []
            for f in tqdm(asyncio.as_completed(detail_tasks), total=len(detail_tasks), desc="Carros Extraídos"):
                detailed_cars.append(await f)

            return pd.DataFrame(detailed_cars)
