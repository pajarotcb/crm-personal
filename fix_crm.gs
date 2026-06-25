/**
 * CRM MicroVidas — Script de corrección de fórmulas
 *
 * Qué hace:
 * 1. Inserta columna FECHA ALTA en la tabla CRM principal (entre ID y Responsable)
 * 2. Corrige el VLOOKUP de FECHA ALTA en todas las fichas individuales (índice 3)
 * 3. Corrige el VLOOKUP de RESPONSABLE en las fichas con #REF! (índice 2)
 * 4. Corrige FECHA ACCION para no mostrar 1/0/1900 cuando está vacía
 */
function corregirCRM() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const hojaCRM = ss.getSheetByName('CRM '); // ojo el espacio al final

  if (!hojaCRM) {
    SpreadsheetApp.getUi().alert('No se encontró la hoja "CRM " — verificá el nombre exacto de la pestaña.');
    return;
  }

  // ── PASO 1: Insertar columna FECHA ALTA en la tabla CRM ──────────────────
  // La tabla empieza en fila 7. Columna B es actualmente "Responsable".
  // Insertamos una columna nueva en B para que quede:
  // A=ID, B=FECHA ALTA, C=Responsable, D=Nombre, ...

  hojaCRM.insertColumnBefore(2); // inserta antes de la columna B actual

  // Encabezado
  hojaCRM.getRange('B6').setValue('FECHA ALTA');
  hojaCRM.getRange('B6').setFontWeight('bold');

  // Formato de fecha para la columna B (filas 7 a 41)
  hojaCRM.getRange('B7:B41').setNumberFormat('dd/mm/yyyy');

  Logger.log('✓ Columna FECHA ALTA insertada en columna B del CRM');

  // ── PASO 2: Corregir fichas individuales ─────────────────────────────────
  // Las fichas están en la misma hoja o en hojas separadas — detectamos cuál
  const todasLasHojas = ss.getSheets();
  let fichasCorregidas = 0;

  todasLasHojas.forEach(hoja => {
    const nombre = hoja.getName();

    // Buscar hojas de fichas individuales (tienen "ID-C" en alguna celda o se llaman con el número)
    // Revisamos toda la hoja buscando la celda que dice "ID CLIENTE"
    const datos = hoja.getDataRange().getValues();

    datos.forEach((fila, i) => {
      fila.forEach((celda, j) => {

        // Detectar celda "FECHA ALTA" en la ficha
        if (celda === 'FECHA ALTA') {
          const celdaValor = hoja.getRange(i + 1, j + 2); // celda a la derecha del label
          // Reemplazar con VLOOKUP índice 2 (ahora B = FECHA ALTA)
          celdaValor.setFormula("=IFERROR(VLOOKUP($B$2,'CRM '!$A$7:$O$41,2,FALSE),\"\")");
          celdaValor.setNumberFormat('dd/mm/yyyy');
          fichasCorregidas++;
        }

        // Detectar celda "RESPONSABLE" (label) en la ficha
        if (celda === 'RESPONSABLE') {
          const celdaValor = hoja.getRange(i + 1, j + 2);
          const valorActual = celdaValor.getFormula();
          // Solo corregir si tiene #REF! o está vacía
          if (valorActual.includes('REF') || valorActual === '') {
            celdaValor.setFormula("=IFERROR(VLOOKUP($B$2,'CRM '!$A$7:$O$41,3,FALSE),\"\")");
            fichasCorregidas++;
          }
        }

        // Detectar celda "FECHA ACCION" (label) en la ficha
        if (celda === 'FECHA ACCION') {
          const celdaValor = hoja.getRange(i + 1, j + 2);
          const formulaActual = celdaValor.getFormula();
          // Si tiene una referencia directa tipo =+D52 o =+D38, envolvemos en IFERROR+SI
          if (formulaActual.startsWith('=+D') || formulaActual.startsWith('=D')) {
            const ref = formulaActual.replace('=+', '=').replace('=', '');
            celdaValor.setFormula(`=IFERROR(SI(${ref}="","",${ref}),"")`);
            celdaValor.setNumberFormat('dd/mm/yyyy');
            fichasCorregidas++;
          }
        }

      });
    });
  });

  Logger.log(`✓ Fichas corregidas: ${fichasCorregidas} campos actualizados`);

  SpreadsheetApp.getUi().alert(
    `✅ Corrección completada\n\n` +
    `• Columna FECHA ALTA insertada en el CRM\n` +
    `• ${fichasCorregidas} campos corregidos en fichas individuales\n\n` +
    `Ahora podés cargar las fechas de alta en la columna B del CRM (filas 7 a 37).`
  );
}
