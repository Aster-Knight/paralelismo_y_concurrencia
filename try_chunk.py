from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pika_banner import print_pikachu
from tqdm import tqdm
import requests
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import math

def download_and_process_chunk(id_range, worker_id, base_url, dir_origin, dir_processed):
    """
    Un solo proceso ejecuta esta función.
    Primero descarga todas las imágenes de su rango, y luego las procesa.
    """
    start_id, end_id = id_range
    
    for i in range(start_id, end_id + 1):
        file_name = f'{i:03d}.png'
        url = f'{base_url}/{file_name}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(os.path.join(dir_origin, file_name), 'wb') as f:
                f.write(response.content)
        except requests.exceptions.RequestException:
            pass # Ignoramos errores por simplicidad

    for i in range(start_id, end_id + 1):
        file_name = f'{i:03d}.png'
        path_origin = os.path.join(dir_origin, file_name)
        if not os.path.exists(path_origin):
            continue # Si la descarga falló, saltar
        try:
            img = Image.open(path_origin).convert('RGB')
            # ... (mismas transformaciones)
            img_inv = ImageOps.invert(img)
            saving_path = os.path.join(dir_processed, file_name)
            img_inv.save(saving_path, quality=95)
        except Exception:
            pass
            
    return f'Worker {worker_id} finalizado.'

def run_parallel_pipeline(n=150, max_workers=8):
    """Función principal que divide el trabajo y lo asigna a los procesos."""
    dir_origin = 'pokemon_dataset_chunk'
    dir_processed = 'pokemon_processed_chunk'
    os.makedirs(dir_origin, exist_ok=True)
    os.makedirs(dir_processed, exist_ok=True)
    
    base_url = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ'
    
    print(f'\n[PIPELINE PARALELO] Ejecutando pipeline en {max_workers} cores...\n')
    start_time = time.time()

    chunk_size = math.ceil(n / max_workers)
    tasks = []
    for i in range(max_workers):
        start_id = i * chunk_size + 1
        end_id = min((i + 1) * chunk_size, n)
        if start_id > n: break
        tasks.append(((start_id, end_id), i)) # ((range), worker_id)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_and_process_chunk, r, wid, base_url, dir_origin, dir_processed) for r, wid in tasks]
        
        for future in tqdm(as_completed(futures), total=len(tasks), desc="Chunks completados"):
            result = future.result()

    total_time = time.time() - start_time
    print(f'\nPipeline paralelo por chunks completado en {total_time:.2f} segundos')
    return total_time

if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   PARTE 3: PIPELINE PARALELO POR CHUNKS (I/O + CPU)')
    print('='*60)
    
    total_time = run_parallel_pipeline()
    
    print('='*60)
    print('RESUMEN PARTE 3\n')
    print(f'  Tiempo Total (Pipeline Paralelo): {total_time:.2f} seg')
    print('='*60)