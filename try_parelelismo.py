from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pika_banner import print_pikachu  
from tqdm import tqdm                  
import requests
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

def download_pokemon(n=150, dir_name='pokemon_dataset'):
    os.makedirs(dir_name, exist_ok=True)
    base_url = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ' 

    print(f'\n[SECUENCIAL] Descargando {n} pokemones...\n')
    start_time = time.time()
    
    for i in tqdm(range(1, n + 1), desc='Descargando', unit='img'):
        file_name = f'{i:03d}.png'
        url = f'{base_url}/{file_name}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(os.path.join(dir_name, file_name), 'wb') as f:
                f.write(response.content)
        except requests.exceptions.RequestException as e:
            tqdm.write(f'  Error descargando {file_name}: {e}')
    
    total_time = time.time() - start_time
    print(f'  Descarga completada en {total_time:.2f} segundos')
    return total_time

def process_one_pokemon(image_path, dir_origin, dir_processed):
    """Función 'worker' que procesa una sola imagen."""
    try:
        path_origin = os.path.join(dir_origin, image_path)
        img = Image.open(path_origin).convert('RGB')
        
        # Transformaciones
        img = img.filter(ImageFilter.GaussianBlur(radius=10))
        img = ImageEnhance.Contrast(img).enhance(1.5)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img_inv = ImageOps.invert(img)
        img_inv = img_inv.filter(ImageFilter.GaussianBlur(radius=5))
        width, height = img_inv.size
        img_inv = img_inv.resize((width * 2, height * 2), Image.LANCZOS)
        img_inv = img_inv.resize((width, height), Image.LANCZOS)
    
        saving_path = os.path.join(dir_processed, image_path)
        img_inv.save(saving_path, quality=95)
        return None
    except Exception as e:
        return f'Error procesando {image_path}: {e}'

def process_pokemon_parallel(dir_origin='pokemon_dataset', dir_processed='pokemon_processed_parallel', max_workers=8):
    os.makedirs(dir_processed, exist_ok=True)
    images = sorted([f for f in os.listdir(dir_origin) if f.endswith('.png')])
    
    print(f'\n[PARALELO] Procesando {len(images)} imágenes con {max_workers} cores...\n')
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_one_pokemon, img, dir_origin, dir_processed) for img in images]
        
        for future in tqdm(as_completed(futures), total=len(images), desc='Procesando', unit='img'):
            error = future.result()
            if error:
                tqdm.write(f'  {error}')
    
    total_time = time.time() - start_time
    print(f'  Procesamiento completado en {total_time:.2f} segundos')
    return total_time

if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   PARTE 1: OPTIMIZANDO SOLO EL PROCESAMIENTO (CPU)')
    print('='*60)
    
    download_time = download_pokemon()
    processing_time = process_pokemon_parallel()
    
    total_time = download_time + processing_time
    print('='*60)
    print('RESUMEN PARTE 1\n')
    print(f'  Descarga (Secuencial):   {download_time:.2f} seg')
    print(f'  Procesamiento (Paralelo): {processing_time:.2f} seg\n')
    print(f'  Total:                   {total_time:.2f} seg')
    print('='*60)