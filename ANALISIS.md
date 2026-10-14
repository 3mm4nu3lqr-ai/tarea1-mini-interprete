# Análisis — Tarea 1

**Integrantes:**
1. Cruz Escobar Aarón
2. Góngora Barroso Alfonso
3. Quirino Roman Emmanuel

**Fork:**
**Rama:**

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

- No hay pruebas que verifique que las divisiones entre 0 envíe `ErrorDeEvaluación`
- No hay ninguna prueba con `pytest.raises(ErrorDeSintaxis)` como revisar paréntesis sin cerrar o abrir, entradas vacías, menos unario (`-3`)
- Ninguna prueba revisa la asociatividad (los operadores de la misma precedencia se asocian a la izquierda) por ejemplo `10 - 3 + 2`, `8 / 4 / 2 `
- No hay pruebas que verifiquen entradas inválidas y que lancen `ErrorDeSintaxis` por ejemplo con caracteres no reconocidos como `3 $ 4`, `3 & 4`
- Faltan pruebas que revisen que un mensaje de error indique la posición dentro del texto
- Nunca se prueba una resta con resultado negativo, como `3 - 5`
- Ninguna prueba revisa divisiones no exactas como `10 / 4` por ejemplo
- Faltan pruebas que revisen operadores del mismo nivel de prioridad como `1 + 2 + 3`
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
| | | | | |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

> No basta con "daba mal". Digan contra qué lo están comparando: qué regla,
> qué línea de la semántica declarada del README.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| | | | | | |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

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
