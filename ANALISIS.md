# Análisis — Tarea 1

**Integrantes:**
1. Cruz Escobar Aarón
2. Góngora Barroso Alfonso
3. Quirino Roman Emmanuel

**Fork:**
https://github.com/3mm4nu3lqr-ai/tarea1-mini-interprete
**Rama:**
tarea1-pruebas-refactorizacion

> Contesten en este archivo. Respuestas breves y concretas: se califica que
> hayan entendido, no la extensión.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | Texto (str) | Lista de tokens | Partir el texto en tokens (número, operador, paréntesis), ignorando espacios y guardando la posición de cada uno |
| `parser` | Lista de tokens | AST (árbol de sintaxis abstracta)| Agrupar los tokens según el orden de prioridad de la gramática, construir el árbol y lanzar `ErrorDeSintaxis` si la entrada no es válida |
| `ast` | Nada | Nodos: Numero y OperacionBinaria | Definir los tipos de nodo del árbol (estructuras del árbol) |
| `evaluator` | AST (árbol de sintaxis abstracta) | Un número | Recorrer el árbol, evaluar primero los dos lados de cada operación y aplicar el operador o lanzar `ErrorDeEvaluacion` |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

> Usen `(3 + 4) * 2` como ejemplo y muestren cómo se ve entre etapa y etapa.

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | [PAR_IZQ, NUMERO(3), MAS, NUMERO(4), PAR_DER, POR, NUMERO(2)] |
| AST | (ver dibujo abajo) |
| resultado | 14 |

```
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```

> Para el renglón del AST, dibújenlo **primero ustedes** y después comprueben
> con `python3 interprete.py --arbol "(3 + 4) * 2"`. Si su dibujo y el del
> programa no coinciden, uno de los dos está mal, y averiguar cuál es
> justamente el trabajo.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| `test_suma` | evaluator | Que `3 + 4` dé 7 | 1 | Normal |
| `test_resta` | evaluator | Que `10 - 3` dé 7 | 1 | Normal |
| `test_multiplicacion` | evaluator | Que `6 * 7` dé 42 | 1 | Normal |
| `test_division` | evaluator | Que `10 / 2` dé 5 | 1 | Normal |
| `test_precedencia_sin_parentesis` | evaluator | Que `3 + 4 * 2` dé 11, o sea que la multiplicación se calcule antes que la suma | 2 | Normal |
| `test_precedencia_con_parentesis` | evaluator | Que `(3 + 4) * 2` dé 14, o sea que los paréntesis fuercen a calcular primero la suma | 2 | Normal |
| `test_tokeniza_un_numero_solo` | lexer | Que `42` produzca un único token `NUMERO` con valor 42 en la posición 0 | 0 | Frontera (entrada mínima: un solo número) |
| `test_tokeniza_una_suma` | lexer | Que `3+4` (sin espacios) produzca `NUMERO(3)` en la posición 0, `MAS` con valor `"+"` en la 1 y `NUMERO(4)` en la 2. | 1 | Normal |
| `test_los_espacios_no_producen_tokens` | lexer | Que `"  3   +   4  "` (espacios al inicio, al final y de más en medio) produzca exactamente 3 tokens. | 1 | Frontera (espacios en cantidad y en los extremos) |
| `test_tokeniza_parentesis` | lexer | Que `(3)` produzca los tipos `PAR_IZQ`, `NUMERO`, `PAR_DER`, en ese orden. | 0 | Normal |
| `test_construye_el_arbol_de_una_suma` | parser | Que `3 + 4` produzca `OperacionBinaria('+', Numero(3), Numero(4))` | 1 | Normal |
| `test_la_multiplicacion_se_agrupa_antes_que_la_suma` | parser | Que `3 + 4 * 2` produzca `OperacionBinaria('+', Numero(3), OperacionBinaria('*', Numero(4), Numero(2)))`, es decir `3 + (4 * 2)` | 2 | Normal |
| `test_los_parentesis_cambian_la_agrupacion` | parser | Que `(3 + 4) * 2` produzca `OperacionBinaria('*', OperacionBinaria('+', Numero(3), Numero(4)), Numero(2))`, es decir `(3 + 4) * 2` | 2 | Normal |

> Llenen la tabla **completa**, con las 13. Es tediosa a propósito: la única
> forma de saber qué no está cubierto es caracterizar sistemáticamente lo que
> sí. Cuando terminen, léanla como columna, no como renglones, y pregúntense
> qué combinación **no aparece nunca**.

### 2.2 ¿Qué comportamientos **no** estaban probados?

- No hay pruebas que verifiquen que las divisiones entre 0 envíe `ErrorDeEvaluacion`
- No hay ninguna prueba con `pytest.raises(ErrorDeSintaxis)` como revisar paréntesis sin cerrar o abrir, entradas vacías, menos unario (`-3`), dos números sin operador (`"3 4"`)
- Ninguna prueba revisa la asociatividad (los operadores de la misma precedencia se asocian a la izquierda) por ejemplo `8 / 4 / 2 `, `10 - 3 - 2`
- No hay pruebas que verifiquen entradas inválidas y que lancen `ErrorDeSintaxis` por ejemplo con caracteres no reconocidos como `3 $ 4`, `3 & 4`
- Faltan pruebas que revisen que un mensaje de error indique la posición dentro del texto
- Nunca se prueba una resta con resultado negativo, como `3 - 5`
- Ninguna prueba revisa divisiones no exactas como `10 / 4` por ejemplo
- No hay pruebas que verifiquen `007` ni `((3))`
- Ninguna prueba verifica el dibujo del árbol, por ejemplo en `formatear_arbol`, que está en `cli.py`, se podría comprobar que `3 + 4 * 2` produzca el dibujo:
```
  +
  |-- 3
  `-- *
      |-- 4
      `-- 2
```

> Ésta es la pregunta importante de toda la tarea. Tómense su tiempo.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| `test_evaluator::test_division_entre_cero` | `5 / 0` | `ErrorDeEvaluacion` | Frontera | El divisor `0` es el valor límite donde la división deja de estar definida |
| `test_evaluator::test_division_se_asocia_a_la_izquierda` | `8 / 4 / 2` | `1` | Normal | Porque es una expresión común, verifica la asociatividad izquierda de la sección 7 |
| `test_evaluator::test_resta_se_asocia_a_la_izquierda` | `10 - 3 - 2` | `5` | Normal | Porque es una expresión válida con dos operadores del mismo nivel |
| `test_evaluator::test_resta_con_resultado_negativo` | `3 - 5` | `-2` | Frontera | La entrada no tiene signo, pero el resultado cruza el límite del cero |
| `test_evaluator::test_division_no_exacta` | `10 / 4` | `2.5` | Normal | Porque es un uso típico de la división declarada en la sección 7 |
| `test_evaluator::test_ceros_a_la_izquierda` | `007` | `7` | Frontera | Forma diferente de escribir un número (con ceros no cambia su valor), declarada en la sección 7 |
| `test_evaluator::test_parentesis_redundantes` | `((3))` | `3` | Frontera | Porque es una doble anidación sin ninguna operación dentro |
| `test_parser::test_resta_se_agrupa_a_la_izquierda` | `10 - 3 - 2` | Árbol `(10 - 3) - 2` | Normal | Porque es una entrada válida, se verifica la forma del árbol, no solo el número |
| `test_cli::test_dibujo_del_arbol` | Árbol de `3 + 4 * 2` | Las 5 líneas del dibujo, con `+` en la raíz | Normal | Entrada común que verifica `formatear_arbol` |
| `test_entradas_invalidas::test_operador_al_final` | `3 +` | `ErrorDeSintaxis` | Inválida | Falta el operando derecho |
| `test_entradas_invalidas::test_parentesis_sin_cerrar` | `(3 + 4` | `ErrorDeSintaxis` | Inválida | Falta el `)` |
| `test_entradas_invalidas::test_parentesis_sin_abrir` | `3 + 4)` | `ErrorDeSintaxis` | Inválida | Sobra un `)` |
| `test_entradas_invalidas::test_operadores_seguidos` | `3 + * 4` | `ErrorDeSintaxis` | Inválida | Dos operadores sin número en medio |
| `test_entradas_invalidas::test_parentesis_vacios` | `()` | `ErrorDeSintaxis` | Inválida | Paréntesis sin expresión dentro |
| `test_entradas_invalidas::test_caracter_no_reconocido` | `3 $ 4` | `ErrorDeSintaxis` | Inválida | El `$` no pertenece al lenguaje |
| `test_entradas_invalidas::test_entrada_vacia_invalida` | `""` | `ErrorDeSintaxis` | Inválida | No hay ninguna expresión que evaluar |
| `test_entradas_invalidas::test_entrada_de_solo_espacios_invalidos` | `"   "` | `ErrorDeSintaxis` | Inválida | Los espacios se ignoran y no queda nada |
| `test_entradas_invalidas::test_dos_numeros_sin_operador_invalido` | `3 4` | `ErrorDeSintaxis` | Inválida | Dos números seguidos sin operador entre ellos |
| `test_entradas_invalidas::test_menos_unario_invalido` | `-3` | `ErrorDeSintaxis` | Inválida | La sección 7 dice que el menos unario no se soporta |
| `test_entradas_invalidas::test_caracter_inesperado_indica_la_posicion` | `3 / - 4` | `ErrorDeSintaxis` con `posicion == 4` | Inválida | Operador donde se esperaba un número, además verifica la posición exigida por la sección 7 |
| `test_entradas_invalidas::test_caracter_no_reconocido_indica_la_posicion` | `3 $ 4` | `ErrorDeSintaxis` con `posicion == 2` | Inválida | Caracter que es ajeno al lenguaje, verifica la posición del error |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?
- El error que reveló fue que la asociatividad de operadores de la misma precedencia se realizaba hacia la derecha, por ejemplo con `"10 - 3 - 2`, donde el programa devolvía `"9"`, cuando debía devolver `"5"`. Y revisando más a detalle las pruebas, se encontró que además se estaban rompiendo otras reglas, como el rechazar caracteres no permitidos o el cómo manejar tokens sobrantes al final de una entrada.
### 4.2 ¿Por qué el comportamiento observado era incorrecto?
- El resultado de la prueba `"10 - 3 - 2"` no puede ser `"9"`, pues rompe con la regla establecida en la sección 7 del `"README.md"` que establece que `"los operadores de la misma precedencia se asocian a la izquierda"`. Lo que se hacía es que la operación se agrupaba a la derecha como `"10 - (3 - 2) = 9"`, cuando cumpliendo con la regla se debía agrupar como `"(10 - 3) - 2 = 5"`. Además las pruebas de entradas inválidas violaban la regla de Entrada inválida que dice `"debe rechazarse con ErrorDeSintaxis, nunca con un error de Python"` y la regla de Mensajes de error que dice `"deben indicar la posición dentro del texto"`.

> No basta con "daba mal". Digan contra qué lo están comparando: qué regla,
> qué línea de la semántica declarada del README.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| La asociatividad se hacía a la derecha en entradas con operadores de la misma precedencia | `"10 - 3 - 2"` | `"9"` (calculaba `"10 - (3 - 2)"`) | `"5"` (calculando `"(10 - 3) - 2"`) | `"b57db20"` Corrijo 3, 4 y 4.1 de DECLARACION_IA | `"9941fc5"` Corrijo parser.py: ahora agrupa a la izquierda con la función coincidir y evalúa sintaxis incompleta |
| Los caracteres no reconocidos eran ignorados | `"3 $ 4"` | El `"$"` se ignoraba y solo se tokenizaba el `"3"` y `"4"` | Un mensaje `"ErrorDeSintaxis("Caracter no identificado '$'", 2")"` | `"b57db20"` Corrijo 3, 4 y 4.1 de DECLARACION_IA | `"69f5bc3"` Corrijo lexer.py: ahora lanza error al encontrar un caracter no identificado |
| Los valores sobrantes eran ignorados | `"3 4"` | `"3"` (pues solo leía el 3 e ignoraba el resto) | Un mensaje `"ErrorDeSintaxis("Token inesperado '4'", 2")"` | `"b57db20"` Corrijo 3, 4 y 4.1 de DECLARACION_IA | `"9941fc5"` Corrijo parser.py: ahora agrupa a la izquierda con la función coincidir y evalúa sintaxis incompleta |
| Se lanzaban errores nativos de Python en lugar hacían falta tokens | `"(3 + 4"` | Un error nativo de Python | Un mensaje `"ErrorDeSintaxis"` con la posición del error exacto | `"b57db20"` Corrijo 3, 4 y 4.1 de DECLARACION_IA | `"9941fc5"` Corrijo parser.py: ahora agrupa a la izquierda con la función coincidir y evalúa sintaxis incompleta |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?
- Estas correcciones son generales porque para empezar no se pusieron condiciones para casos específicos como poner un if para que cada prueba pudiera pasar, lo que se hizo fue cambiar la lógica de `parser.py` y `lexer.py`.
En `parser.py` se cambió la recursión por un ciclo `while`, esto garantiza que para cualquier entrada con varias operaciones de la misma precedencia encadenadas, la asociatividad se hará de izquierda a derecha. Además se agregaron verificaciones para los casos de entradas en donde haya elementos de más.
En `lexer.py` se cambió el salto que se hacía al encontrar caracteres no permitidos para que ahora se lance un `ErrorDeSintaxis` que marca el caracter y su posición exacta.
Con estos cambios se aseguró que al momento de correr `pytest` todas las pruebas pasaran y garantizando que cualquier prueba futura también lo haga.

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?
Durante la revisión tuvimos las siguientes observaciones:
- Duplicación de código en `parser.py`: pues en las funciones `_expresion()` y `_termino()` se repetía casi el mismo código para verificar si el token actual era válido o no, para después consumirlo (la única diferencia que había era el tipo de operador que evaluaba), lo que hacía que el código fuera repetitivo.
- Juntar responsabilidades en `evaluator.py`: la función evaluar hacia dos cosas a la vez, que era recorrer la estructura del AST y ejecutar las operaciones aritméticas con varios `if` anidados, por lo que no había una separación para estas dos acciones.
- Ocultamiento de errores en `lexer.py`: al verificar si el caracter era válido, y éste no lo era, lo se hacía era simplemente ignorarlo, lo que podría generar conflictos más adelante.

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?
Se realizaron dos refactorizaciones en el código:
- En `parser.py` se extrae la función `_coincidir()`: se encapsuló la comprobación y el avance del token en esa función (evitando así tener que repetir el  mismo código dos veces) y sigue conservando el mismo comportamiento porque se hacen las mismas verificaciones en el mismos orden y se avanza en la posición del texto de igual manera.
- En `parser.py` se factorizó el comportamiento de los métodos termino y expresion
- En `evaluator.py` se extrae la función `_calcular_binaria()`: se movieron las operaciones aritméticas a esa función y conserva el mismo comportamiento porque el árbol se recorre en el mismo orden, los resultados se calculan igual y se lanzan los mismos errores (como cuando se divide entre cero).
 
> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?
Consideramos que ninguno, pues el código no es tan grande y es directo, por lo que usar alguno de estos patrones podría complicar el código sin hacer alguna mejora o resolver un problema real, pero, si se quisiera usar alguno de estos patrones el sistema se necesitaría que el programa permita agregar nuevos tipos de tokens sin tener que modificar el codigo base (esto para Factory Method) o que se conecte a una librería externa que devuelva datos de manera distinta a como lo hace actualmente el programa (esto para Adapter).

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?
Para agregar un operador nuevo se tendrían que modificar 3 archivos:
- `lexer.py` para definir un nuevo tipo de token y para que éste pueda ser reconocido.
- `parser.py` para agregar el nuevo token en el orden de precedencia que le corresponde.
- `evaluator.py` para agregar la operación en la función `_calcular_binaria()` y tener en cuenta sus restricciones.
De estas modificaciones la más difícil de hacer sería la de `parser.py` pues se tiene que poner el nuevo operador en el lugar adecuado dentro del orden de precedencia para evitar que la asociatividad y el orden se vean afectadas y hagan mal los cálculos.

> Por ejemplo `%`. ¿Cuántos archivos hay que tocar? ¿Por qué?

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.
