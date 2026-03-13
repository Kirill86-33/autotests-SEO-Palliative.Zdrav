import os
import sys
import json
import re

def find_sitemap_url():
    """Ищет URL sitemap в любых файлах текущей папки"""
    
    print("🔍 Ищу URL sitemap во всех файлах...")
    
    # Сначала попробуем найти admin.json
    if os.path.exists('admin.json'):
        try:
            with open('admin.json', 'r') as f:
                data = json.load(f)
                
            # Ищем в стандартных ключах
            for key in ['sitemap_url', 'sitemap', 'url']:
                if key in data:
                    url = data[key]
                    if url.startswith(('http://', 'https://')):
                        print(f"✅ Найден в admin.json по ключу '{key}': {url}")
                        return url
                        
        except json.JSONDecodeError:
            print("❌ admin.json не является валидным JSON")
    
    # Ищем во всех файлах .py
    for file in os.listdir('.'):
        if file.endswith('.py'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Ищем URL в коде Python
                url_patterns = [
                    r'sitemap.*?=.*?[\'"](https?://[^\'"]+)[\'"]',
                    r'url.*?=.*?[\'"](https?://[^\'"]+)[\'"]',
                    r'https?://[^\s\'"]+sitemap[^\s\'"]*\.xml',
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"✅ Найден в {file}: {matches[0]}")
                        return matches[0]
                        
            except Exception as e:
                continue
    
    # Если ничего не нашли
    print("❌ URL sitemap не найден ни в одном файле")
    
    # Спросим у пользователя
    print("\n💡 Введите URL sitemap вручную:")
    print("Примеры:")
    print("  - https://site.com/sitemap.xml")
    print("  - https://site.com/sitemap_index.xml")
    print("  - https://site.com/ru/sitemap.xml")
    
    url = input("\nURL: ").strip()
    
    if url:
        # Сохраним в admin.json для будущего использования
        data = {'sitemap_url': url}
        with open('admin.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ URL сохранен в admin.json")
        return url
    
    return None

def download_sitemap(url):
    """Скачивает sitemap по URL"""
    import requests
    
    print(f"\n⬇️  Скачиваю {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Сохраняем
        filename = 'sitemap.xml'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Файл сохранен как {filename}")
        print(f"📏 Размер: {len(response.content)} байт")
        
        # Быстрая проверка
        if b'<?xml' in response.content[:100]:
            print("✅ Это валидный XML файл")
            
            # Считаем количество URL
            import xml.etree.ElementTree as ET
            try:
                root = ET.fromstring(response.content)
                urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if urls:
                    print(f"📊 Найдено URL в sitemap: {len(urls)}")
            except:
                pass
        else:
            print("⚠️  Внимание: файл может не быть XML")
            
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("SITEMAP DOWNLOADER")
    print("=" * 50)
    
    url = find_sitemap_url()
    
    if url:
        download_sitemap(url)
    
    # Пауза для Windows
    if sys.platform == "win32":
        input("\nНажмите Enter для выхода...")