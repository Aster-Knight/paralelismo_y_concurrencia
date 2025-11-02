# Proyecto: Paralelismo y Concurrencia

* **Modalidad:** proyecto individual.
* **Fecha de entrega:** domingo 02 de noviembre, a las 11:59pm.

---

**Intrucciones:** 

* En este *gist* encontrará dos archivos iniciales para su proyecto: `pika_banner.py` es una trivialidad, `pokemon.py` es el archivo principal.

* Descargar los archivos y ejecutar `pokemon.py` localmente para ver su funcionamiento. El archivo hace lo siguiente:
  * A través de un [repositorio público](https://github.com/HybridShivam/Pokemon) de imágenes de pokémon, descarga la imagen HD de los primeros 150 pokemones y los almacena en un directorio llamado `/pokemon_dataset`. Las imágenes son descargadas una por una y debe continuarse haciendo de esa forma a lo largo del proyecto. Estas son operaciones *I/O bound*.
  * Una vez descargado el dataset, se procede a *transformar* dichas imágenes con ayuda de la librería PIL. Se aplican transformaciones como filtros de gauss, inversión de color, resizing, entre otros... estas son operaciones *CPU bound*.
  * Las imágenes procesadas se almacenan en un nuevo directorio llamado `/pokemon_processed`.
  * Al finalizar, el script muestra un resumen de tiempos por fase y en total. Tener presente dicha métrica.

* Para correr localmente el script, puede que no tenga inicialmente todas la librerías requeridas instaladas. Troubleshootearlo.

* Trás haber descargado los archivos, instalado librerías, ejecutado localmente, explorado el código y el funcionamiento del script. Podrá iniciar a desarrollar su **solución**.

---

**Solución:**

* El código brindado en este gist será su código *baseline*, o sea, el punto de inicio. Antes de iniciar con su solución, deberá hacer un commit que incluya el código sin ninguna modificación. Agregar un nombre de commit que incluya el keyword "baseline".

* Ahora, podrá iniciar a mejorar el rendimiento del código. Para esto deberá **aplicar paralelismo y concurrencia** según considere correspondiente en las distintas fases del programa. El objetivo es reducir el tiempo de ejecución en la mayor medida posible. 

* *Constraints*:
  * Podrán usar como máximo 8 cores.
  * Las imágenes deben ser descargadas y procesadas de forma individual (que no es lo mismo a *secuencialmente*).
 
---

**Entregable:**

* Deberá trabajar todo en un repositorio personal de github. Los commits deben reflejar trabajo progresivo y ordenado.
* Documentar en el `README.md` las estrategias utilizadas para mejorar el rendimiento y una tabla comparativa con los tiempos del script baseline y los mejores tiempos obtenidos con la solución paralela/concurrente.
* Una vez finalizado su trabajo, deberán hacer público su repositorio.
* Comentar este *gist* desde su cuenta de github, dejando ahí el link a su repositorio, antes del deadline de entrega especificado.




