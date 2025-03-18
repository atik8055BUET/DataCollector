from bs4 import BeautifulSoup
from typing import List, Optional
import re
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import csv
import os
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

class ExtractText:
    __bangla_pattern = re.compile(r'[\u0980-\u09FF]')
    
    @staticmethod
    def __contains_bangla(text: str) -> bool:
        return bool(ExtractText.__bangla_pattern.search(text))
    
    @staticmethod
    def __clean_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\r\n\t]', ' ', text)
        return text.strip()
    
    @staticmethod
    def get_tags(soup: BeautifulSoup, tags: List[str], min_length: int = 20, 
                           bangla_only: bool = True) -> List[str]:
        if not soup:
            raise ValueError("No soup object provided")
        
        results = []
        for tag_name in tags:
            elements = soup.find_all(tag_name)
            for element in elements:
                text = ExtractText.__clean_text(element.get_text())
                if len(text) >= min_length and (not bangla_only or ExtractText.__contains_bangla(text)):
                    results.append(text)
        return results
    
    @staticmethod
    def get_selectors(soup: BeautifulSoup, selectors: List[str], min_length: int = 20, 
                                bangla_only: bool = True) -> List[str]:
        if not soup:
            raise ValueError("No soup object provided")
        
        results = []
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = ExtractText.__clean_text(element.get_text())
                if len(text) >= min_length and (not bangla_only or ExtractText.__contains_bangla(text)):
                    results.append(text)
        return results
    
    @staticmethod
    def get_para(soup: BeautifulSoup, container_selector: Optional[str] = None, 
                         min_words: int = 20, bangla_only: bool = True) -> List[str]:
        if not soup:
            raise ValueError("No soup object provided")
        
        container = soup.select_one(container_selector) if container_selector else soup
        
        paragraphs = []
        for p in container.find_all('p'):
            text = ExtractText.__clean_text(p.get_text())
            word_count = len(text.split())
            
            if word_count >= min_words and (not bangla_only or ExtractText.__contains_bangla(text)):
                paragraphs.append(text)
        return paragraphs

class HTMLParser:
    __DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    @staticmethod
    def __get_html_from_url(url: str, headers: Optional[Dict[str, str]] = None, proxies: Optional[Dict[str, str]] = None) -> str:
        if not url:
            raise ValueError("No URL provided")

        request_headers = HTMLParser.__DEFAULT_HEADERS.copy()
        if headers:
            request_headers.update(headers)
            
        try:
            response = requests.get(
                url, 
                headers=request_headers,
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise e
    
    @staticmethod
    def __get_soup_from_html(html_content: str) -> BeautifulSoup:
        if not html_content:
            raise ValueError("No HTML content to parse")
        
        return BeautifulSoup(html_content, 'html.parser')
    
    @staticmethod
    def get_soup(url: str, headers: Optional[Dict[str, str]] = None, proxies: Optional[Dict[str, str]] = None) -> BeautifulSoup:
        html_content = HTMLParser.__get_html_from_url(url, headers, proxies)
        return HTMLParser.__get_soup_from_html(html_content)

class DataSaver:
    @staticmethod
    def __create_directory(filepath: str) -> None:
        """Create directory if it doesn't exist."""
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    @staticmethod
    def save_csv(paragraphs: List[str], filepath: str, source_url: str, append: bool = False) -> str:
        DataSaver.__create_directory(filepath)

        rows = []
        date = datetime.now().date().isoformat()
        
        for paragraph in paragraphs:
            rows.append([paragraph, source_url, date])
        
        mode = 'a' if append and os.path.exists(filepath) else 'w'
        write_headers = not (append and os.path.exists(filepath) and os.path.getsize(filepath) > 0)
        
        with open(filepath, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_headers:
                writer.writerow(["text", "source_url", "date"])
            writer.writerows(rows)
        
        return filepath
    
    @staticmethod
    def save_excel(paragraphs: List[str], filepath: str, 
                source_url: str,
                sheet_name: str = 'Paragraphs',
                append: bool = False) -> str:
        DataSaver.__create_directory(filepath)
        
        data = {
            "text": paragraphs,
            "source_url": [source_url] * len(paragraphs),
            "date": [datetime.now().date().isoformat()] * len(paragraphs)
        }
        
        df_new = pd.DataFrame(data)
        
        if append and os.path.exists(filepath):
            try:
                with pd.ExcelWriter(filepath, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    try:
                        df_existing = pd.read_excel(filepath, sheet_name=sheet_name)
                        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                        df_combined.to_excel(writer, sheet_name=sheet_name, index=False)
                    except:
                        df_new.to_excel(writer, sheet_name=sheet_name, index=False)
            except Exception as e:
                df_new.to_excel(filepath, sheet_name=sheet_name, index=False)
        else:
            df_new.to_excel(filepath, sheet_name=sheet_name, index=False)
        
        return filepath
