import os
import time
import requests
import multiprocessing as mp
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from tqdm import tqdm
from pika_banner import print_pikachu
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

N_POKEMON = 150
MAX_DOWNLOAD_WORKERS = 20 
MAX_PROCESSING_WORKERS = 8

DIR_ORIGIN = 'pokemon_dataset_final'
DIR_PROCESSED = 'pokemon_processed_final'
BASE_URL = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ'

def download_one_pokemon(i):
    """Worker para el ThreadPool: Descarga una sola imagen."""
    file_name = f'{i:03d}.png'
    url = f'{BASE_URL}/{file_name}'
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(os.path.join(DIR_ORIGIN, file_name), 'wb') as f:
            f.write(response.content)
        return None
    except requests.exceptions.RequestException as e:
        return f'Error descargando {file_name}: {e}'

def download_pokemon_concurrently(n, max_workers):
    """Gestiona la descarga concurrente de N imágenes usando un ThreadPool."""
    os.makedirs(DIR_ORIGIN, exist_ok=True)
    print(f'\n[FASE 1 - CONCURRENTE] Descargando {n} pokemones con {max_workers} hilos...\n')
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_one_pokemon, i) for i in range(1, n + 1)]
        
        for future in tqdm(as_completed(futures), total=n, desc='Descargando', unit='img'):
            error = future.result()
            if error:
                tqdm.write(f'  ADVERTENCIA: {error}')

    total_time = time.time() - start_time
    print(f'  Descarga concurrente completada en {total_time:.2f} segundos')
    return total_time

def process_one_pokemon(image_path):
    """Worker para el ProcessPool: Procesa una sola imagen."""
    try:
        path_origin = os.path.join(DIR_ORIGIN, image_path)
        img = Image.open(path_origin).convert('RGB')
        
        img = img.filter(ImageFilter.GaussianBlur(radius=10))
        img = ImageEnhance.Contrast(img).enhance(1.5)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img_inv = ImageOps.invert(img)
        img_inv = img_inv.filter(ImageFilter.GaussianBlur(radius=5))
        width, height = img_inv.size
        img_inv = img_inv.resize((width * 2, height * 2), Image.LANCZOS)
        img_inv = img_inv.resize((width, height), Image.LANCZOS)
    
        saving_path = os.path.join(DIR_PROCESSED, image_path)
        img_inv.save(saving_path, quality=95)
        return None
    except Exception as e:
        return f'Error procesando {image_path}: {e}'

def process_pokemon_in_parallel(max_workers):
    """Gestiona el procesamiento en paralelo de imágenes usando un ProcessPool."""
    os.makedirs(DIR_PROCESSED, exist_ok=True)
    images = sorted([f for f in os.listdir(DIR_ORIGIN) if f.endswith('.png')])
    
    if not images:
        print("\nNo se encontraron imágenes para procesar.")
        return 0

    print(f'\n[FASE 2 - PARALELO] Procesando {len(images)} imágenes con {max_workers} cores...\n')
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_one_pokemon, img) for img in images]
        
        for future in tqdm(as_completed(futures), total=len(images), desc='Procesando', unit='img'):
            error = future.result()
            if error:
                tqdm.write(f'  ADVERTENCIA: {error}')
    
    total_time = time.time() - start_time
    print(f'  Procesamiento en paralelo completado en {total_time:.2f} segundos')
    return total_time

if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   PIPELINE ÓPTIMO: CONCURRENCIA (I/O) + PARALELISMO (CPU)')
    print('='*60)
    
    download_time = download_pokemon_concurrently(
        n=N_POKEMON, 
        max_workers=MAX_DOWNLOAD_WORKERS
    )
    
    processing_time = process_pokemon_in_parallel(
        max_workers=MAX_PROCESSING_WORKERS
    )
    
    total_time = download_time + processing_time

    print('\n' + '='*60)
    print('RESUMEN DE TIEMPOS DEL PIPELINE ÓPTIMO\n')
    print(f'  Descarga Concurrente (I/O):  {download_time:.2f} seg')
    print(f'  Procesamiento Paralelo (CPU): {processing_time:.2f} seg')
    print(f'  Tiempo Total:                  {total_time:.2f} seg')
    print('='*60)