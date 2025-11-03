from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pika_banner import print_pikachu
from tqdm import tqdm
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_one_pokemon(i, base_url, dir_name):
    """Función 'worker' que descarga una sola imagen."""
    file_name = f'{i:03d}.png'
    url = f'{base_url}/{file_name}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(os.path.join(dir_name, file_name), 'wb') as f:
            f.write(response.content)
        return None
    except requests.exceptions.RequestException as e:
        return f'Error descargando {file_name}: {e}'

def download_pokemon_concurrent(n=150, dir_name='pokemon_dataset', max_workers=8):
    os.makedirs(dir_name, exist_ok=True)
    base_url = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ' 

    print(f'\n[CONCURRENTE] Descargando {n} pokemones con {max_workers} hilos...\n')
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_one_pokemon, i, base_url, dir_name) for i in range(1, n + 1)]
        
        for future in tqdm(as_completed(futures), total=n, desc='Descargando', unit='img'):
            error = future.result()
            if error:
                tqdm.write(f'  {error}')

    total_time = time.time() - start_time
    print(f'  Descarga completada en {total_time:.2f} segundos')
    return total_time

def process_pokemon(dir_origin='pokemon_dataset', dir_name='pokemon_processed_sequential'):
    os.makedirs(dir_name, exist_ok=True)
    images = sorted([f for f in os.listdir(dir_origin) if f.endswith('.png')])
    
    print(f'\n[SECUENCIAL] Procesando {len(images)} imágenes...\n')
    start_time = time.time()
    
    for image in tqdm(images, desc='Procesando', unit='img'):
        try:
            path_origin = os.path.join(dir_origin, image)
            img = Image.open(path_origin).convert('RGB')
            img_inv = ImageOps.invert(img)
            saving_path = os.path.join(dir_name, image)
            img_inv.save(saving_path, quality=95)
        except Exception as e:
            tqdm.write(f'  Error procesando {image}: {e}')
    
    total_time = time.time() - start_time
    print(f'  Procesamiento completado en {total_time:.2f} segundos')
    return total_time

if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   PARTE 2: OPTIMIZANDO SOLO LA DESCARGA (I/O)')
    print('='*60)
    
    download_time = download_pokemon_concurrent()
    processing_time = process_pokemon()
    
    total_time = download_time + processing_time
    print('='*60)
    print('RESUMEN PARTE 2\n')
    print(f'  Descarga (Concurrente): {download_time:.2f} seg')
    print(f'  Procesamiento (Secuencial): {processing_time:.2f} seg\n')
    print(f'  Total:                    {total_time:.2f} seg')
    print('='*60)