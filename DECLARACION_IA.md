# Declaración de uso de Inteligencia Artificial

**Actividad:**
**Integrantes:**
1. Cruz Escobar Aarón
2. Góngora Barroso Alfonso
3. Quirino Roman Emmanuel
**Fecha:**
14-Octubre-2026

> Esta declaración es obligatoria en toda tarea, práctica y en el proyecto final.
> **No da ni quita puntos**: es un reporte adicional que se revisa aparte y se
> devuelve con comentarios. **No se evalúa cuánta IA usaron**, sino si pueden
> dar cuenta de lo que entregaron.

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [X] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|---|---|
| Gemini | Gemini 3.6 Flash |

> Cuenta también el autocompletado del editor (Copilot y similares). Si sólo
> fue eso, basta con decirlo en un renglón y seguir al punto 4.

---

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
|---|---|
| Revisar que pruebas no hemos considerado | ANALISIS (test no probados) |

> Sean específicos. *"Para la tarea"* no dice nada.
> *"Para generar las pruebas de `minimo_de_llaves`"* sí.

---

## 3. Prompts principales

Textuales, tal como los escribieron. No los limpien ni los reescriban.

```
(prompt 1)
Me podrías decir que casos no hemos considerado?
*"Se adjuntan archivos test y clases principales"*
```

---

## 4. Cómo se incorporó o se descartó lo obtenido

**Éste es el punto que más pesa.**

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|---|---|---|---|
| test caracter invalido posicion | Aceptado | Queremos comprobar que los errores que salten manden a la posición correcta del error | `test_evaluator.py` Agregando pruebas|
| test exsceso de parentesis | Aceptado | Puesto que el programa debe de ignorar los parentesis excendentes | `test_evaluator.py` Añado pruebas |
| test operaciones seguidas | Modificado | Queremos que el programa sea capaz de procesar una cadena de texto más grande que la propuesta | `test_evaluator.py` Añadiendo pruebas |
| test operaciones con negativos | Descartado | El programa no debe de ser capaz de procesar los numeros negativos | | 

> **"Lo descartamos" es una respuesta excelente**, si dicen por qué.
> Una declaración donde todo se aceptó sin cambios es una declaración que
> no muestra criterio.

### 4.1 Si la usaron para el análisis: el contraste

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

| ¿Qué encontró la herramienta que ustedes **no** habían notado? | ¿Qué **no** encontró, que en este curso sí consideramos un problema?  |
|---|---|
| Probar el programa con exceso de parentesis | Test con cadenas vacías |
| Probar el programa con operaciones seguidad | Pruebas con asociatividad |
| Probar el programa con parentesis vacíos | |
| Probar que el programa regresaba el indice correcto donde se ubicaba el error | |

> La segunda es la que más nos interesa. Una herramienta suele no señalar la
> duplicación de código, porque el programa funciona igual. Ustedes ya saben
> por qué eso sí importa.
>
> Si no usaron IA para el análisis, escriban *"no aplica"*.

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

Los test no fueron implementados por la IA, solo dio sugerencias textuales, estos se evaluaron conforme a su validez para los casos a evaluar
y fueron implementados

> Una prueba que escribieron, una ejecución, un contraste contra las notas de
> clase o contra el enunciado. *"Lo revisamos"* no es una verificación.

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

Los test se ven limitados a la imaginación del programador y su conocimiento sobre el lenguaje y el código

> Concreta. No *"a veces se equivoca"*, sino *"propuso pruebas sólo para
> m = 4 y nunca para órdenes impares, porque no conocía la definición del
> laboratorio"*.

### 5.2 ¿Qué harían distinto la próxima vez?

Daríamos junto con el código la sección 7 del README, para que las sugerencias respeten la semántica propuesta y no proponga casos que contradicen o choquen 
con lo que queremos

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|---|---|
| Cruz Escobar Aarón | 323306287 |
| Góngora Barroso Alfonso | 323273888 |
|  Quirino Roman Emmanuel | 323030173 |
