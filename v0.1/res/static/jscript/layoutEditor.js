// Author: PDT
// Since: 2020/09/19

// This is the script used in layout-editor.html

// CREATE ELEMENTS
// ~~~~~~~~~~~~~~~

function createTitleRow(layout_form) {

    let titleRow = document.createElement('div');
    titleRow.setAttribute('class', 'row');

    let titleCol = document.createElement('div');
    titleCol.setAttribute('class', 'col');

    titleCol.style.paddingLeft = '0px';
    titleCol.style.paddingRight = '0px';

    titleRow.appendChild(titleCol);

    let titleSelectLabel = document.createElement('label');
    titleSelectLabel.setAttribute('for', 'detail-view-title')
    titleSelectLabel.textContent = "Page Title:";
    titleCol.appendChild(titleSelectLabel);

    titleCol.appendChild(createColumnSelector(layout_form, 'detail-view', 'title'));

    return titleRow;
}

function createAddRowButton(layout_form) {

    let addRowButtonRow = document.createElement('div');
    addRowButtonRow.setAttribute('class', 'row justify-content-end');
    addRowButtonRow.style.marginBottom = '10px';

    let addRowButtonCol = document.createElement('div');
    addRowButtonCol.setAttribute('class', 'col-2');
    addRowButtonRow.appendChild(addRowButtonCol);

    let addRowButton = document.createElement('button');
    addRowButton.setAttribute('class', 'btn btn-block btn-dark');
    addRowButton.setAttribute('type', 'button');
    addRowButton.textContent = "Add Row";
    addRowButton.onclick = () => {
        layout_form.appendChild(createRow(layout_form));
    };
    addRowButtonCol.appendChild(addRowButton);

    return addRowButtonRow;
}

function createRow(layout_form) {

    let rows = layout_form['rows'];
    let rowNumbers = Array.from(rows.keys());
    let rowNumber = (rowNumbers.length > 0 ? (Math.max(...rowNumbers) + 1) : 0);

    // Create RowInfo object

    rows.set(rowNumber, {
        'column_number': 0,
        'columns': []
    });

    // CREATE VIEW OBJECT
    // ------------------

    // Create a container for the layout row

    let layoutRowEditItemRow = document.createElement('div');
    layoutRowEditItemRow.setAttribute('class', 'row');
    layoutRowEditItemRow.setAttribute('id', 'row-' + rowNumber + '-container-row');

    // Creating a row with id 'row-{rowNumber}'

    let layoutRowEditItem = document.createElement('div');
    layoutRowEditItem.setAttribute('id', 'row-' + rowNumber + '-container-col');
    layoutRowEditItem.setAttribute('class', 'col');

    layoutRowEditItem.style.paddingLeft = 0;
    layoutRowEditItem.style.paddingRight = 0;

    layoutRowEditItemRow.appendChild(layoutRowEditItem);

    let layoutRowEditItemBody = document.createElement('div');
    layoutRowEditItemBody.setAttribute('class', 'container shadow p-3 mb-2 bg-white rounded');
    layoutRowEditItemBody.setAttribute('id', 'row-' + rowNumber + '-container-body');
    layoutRowEditItem.appendChild(layoutRowEditItemBody);

    layoutRowEditItemBody.style.paddingLeft = '10px';
    layoutRowEditItemBody.style.paddingRight = '10px';

    // Creating the Row row (❁´◡`❁)
    let columnRow = document.createElement('div');
    columnRow.setAttribute('id', 'row-' + rowNumber + '-col')
    columnRow.setAttribute('class', 'row flex-nowrap');

    columnRow.style.alignItems = 'stretch';

    // Add items to body
    layoutRowEditItemBody.appendChild(createRowMenu(layout_form, rows, rowNumber));
    layoutRowEditItemBody.appendChild(document.createElement('hr'));
    layoutRowEditItemBody.appendChild(columnRow);

    // Add initial Column
    columnRow.appendChild(createColumn(layout_form, rows, rowNumber, rows.get(rowNumber)['column_number']));

    return layoutRowEditItemRow;
}

function createRowMenu(layout_form, rows, rowNumber) {

    let editItemMenuRow = document.createElement('div');
    editItemMenuRow.setAttribute('id', 'row-' + rowNumber + '-menu');
    editItemMenuRow.setAttribute('class', 'row justify-content-end');

    // Add menu item to the layoutRowEditItem

    let addColumnMenuItemHeaderColumn = document.createElement('div');
    addColumnMenuItemHeaderColumn.setAttribute('class', 'col-10');
    editItemMenuRow.appendChild(addColumnMenuItemHeaderColumn);

    let addColumnMenuItemHeader = document.createElement('h5');
    addColumnMenuItemHeader.setAttribute('class', 'header');
    addColumnMenuItemHeader.textContent = 'Row: # ' + rowNumber;
    addColumnMenuItemHeaderColumn.appendChild(addColumnMenuItemHeader);

    let addColumnMenuItemColumn = document.createElement('div');
    addColumnMenuItemColumn.setAttribute('class', 'col-2');
    editItemMenuRow.appendChild(addColumnMenuItemColumn);

    // Specifying a button, that lets a user add
    // a layoutColumn to the row of the layout.

    let addColMenuItemButton = document.createElement('button');
    addColMenuItemButton.setAttribute('class', 'btn btn-block btn-dark');
    addColMenuItemButton.innerText = "Add Column";
    addColMenuItemButton.type = 'button';

    // Adding an onclick to the add column button, that does exactly that.
    addColMenuItemButton.onclick = () => {

        let rows = document.getElementById('layout-form')['rows'];
        let columnRow = document.getElementById('row-' + rowNumber + '-col');

        let newColumn = createColumn(layout_form, rows, rowNumber, rows.get(rowNumber)['column_number']);

        if (newColumn) {
            columnRow.appendChild(newColumn);

            rows.get(rowNumber).columns.forEach((item) => {

                let no_columns = rows.get(rowNumber).columns.length;
                let column_width = 12 / no_columns;
                let max_offset = 12 - 3 * no_columns;
                let max_width = 12 - 3 * (no_columns - 1);

                let widthSelector = document.getElementById(
                    'row-' + rowNumber + '-col-' + item.column_id + '-width')
                let offsetSelector = document.getElementById(
                    'row-' + rowNumber + '-col-' + item.column_id + '-offset')

                item.column_width = String(column_width);
                item.column_offset = String(0)
                item.column_div.setAttribute(
                    'class', 'col-' + column_width + ' offset-0')

                widthSelector.setAttribute('value', column_width);
                widthSelector.setAttribute('max', max_width);
                widthSelector.value = String(column_width);

                offsetSelector.setAttribute('value', 0);
                offsetSelector.setAttribute('max', max_offset);
                offsetSelector.value = String(0);
            })
        }
    }

    addColumnMenuItemColumn.appendChild(addColMenuItemButton);

    return editItemMenuRow;
}

function createPluginRow() {

    let pluginRow = document.createElement('div');
    pluginRow.setAttribute('class', 'row');
    pluginRow.style.paddingBottom = '12px';

    let pluginCol = document.createElement('div');
    pluginCol.setAttribute('class', 'col');
    pluginRow.appendChild(pluginCol);

    return {'row': pluginRow, 'col': pluginCol};
}

function createColumn(layout_form, rows, rowNumber, columnNumber) {

    if (columnNumber < 3) {

        // Adding the Column column ༼ つ ◕_◕ ༽つ

        let columnId = 'row-' + rowNumber + '-col-' + columnNumber + '-column'

        let columnEditor = document.createElement('div');
        columnEditor.setAttribute('id', columnId);
        columnEditor.setAttribute('class', 'col');

        columnEditor.style.alignItems = 'stretch';

        // This is the editor card for the column/plugin/whatnot
        // Checkout: Namespace is SHIT here (ಥ_ಥ)

        let columnEditorBody = document.createElement('div');
        columnEditorBody.setAttribute('id', columnId + '-body')
        columnEditorBody.setAttribute('class', 'container shadow p-3 mb-2 bg-white rounded');

        columnEditorBody.style.paddingTop = '8px';
        columnEditorBody.style.paddingBottom = '8px';
        columnEditorBody.style.flexGrow = 'True';
        columnEditorBody.style.alignSelf = 'stretch';

        columnEditor.appendChild(columnEditorBody);

        // Adding a heading to each card

        let columnEditorHeaderRow = document.createElement('div');
        columnEditorHeaderRow.setAttribute('class', 'row');
        columnEditorBody.appendChild(columnEditorHeaderRow);

        let columnEditorHeaderCol = document.createElement('div');
        columnEditorHeaderCol.setAttribute('class', 'col');
        columnEditorHeaderRow.appendChild(columnEditorHeaderCol);

        let columnEditorHeader = document.createElement('h6');
        columnEditorHeader.setAttribute('class', 'header');
        columnEditorHeader.textContent = 'Column: # ' + columnNumber;
        columnEditorHeaderCol.appendChild(columnEditorHeader)

        // Adding a divider

        columnEditorBody.appendChild(document.createElement('hr'));

        // Adding inputs for the ColumnInfo data

        columnEditorBody.appendChild(createPluginSelector(layout_form, rowNumber, columnNumber));
        columnEditorBody.appendChild(createWidthSelector(rowNumber, columnNumber));
        columnEditorBody.appendChild(createOffsetSelector(rowNumber, columnNumber));

        let fieldMappingsAnchorId = 'row-' + rowNumber + '-col-' + columnNumber + '-field-mappings';

        let columnEditorFieldMappings = document.createElement('div');
        columnEditorFieldMappings.setAttribute('id', fieldMappingsAnchorId);
        columnEditorBody.appendChild(columnEditorFieldMappings);

        let customMappingsAnchorId = 'row-' + rowNumber + '-col-' + columnNumber + '-custom-mappings';

        let columnEditorCustomMappings = document.createElement('div');
        columnEditorCustomMappings.setAttribute('id', customMappingsAnchorId);
        columnEditorBody.appendChild(columnEditorCustomMappings);

        rows.get(rowNumber)['column_number'] += 1;
        rows.get(rowNumber).columns.push({
            column_id: columnNumber,
            column_plugin: null,
            column_width: null,
            column_offset: 0,
            column_div: columnEditor
        });

        return columnEditor;
    }
    return null;
}

function createPluginSelector(layout_form, rowNumber, columnNumber) {

    let availablePlugins = document.getElementById('layout-form')['available_plugins'];
    let rowId = 'row-' + rowNumber + '-col-' + columnNumber + '-plugin';

    let {row: selectPluginRow, col: selectPluginCol} = createPluginRow();

    let selectPluginLabel = document.createElement('label');
    selectPluginLabel.setAttribute('for', rowId);
    selectPluginLabel.textContent = 'Plugin:';
    selectPluginCol.appendChild(selectPluginLabel);

    let selectPlugin = document.createElement('select');
    selectPlugin.setAttribute('class', 'form-control custom-select');
    selectPlugin.setAttribute('id', rowId);
    selectPlugin.setAttribute('name', rowId);
    // IMPORTANT: This is the plugin changed handler.
    selectPlugin.onchange = (selected) => {

        let fieldMappingsAnchorId = 'row-' + rowNumber + '-col-' + columnNumber + '-custom-mappings';
        let fieldMappingsAnchor = document.getElementById(fieldMappingsAnchorId);

        let selectedPlugin = availablePlugins.filter(plugin => plugin.id === selected.target['value'])[0];

        fieldMappingsAnchor.querySelectorAll('*').forEach(n => n.remove());

        if (selectedPlugin['allow_custom_mappings']) {
            fieldMappingsAnchor.appendChild(
                createFieldMappings(layout_form, rowNumber, columnNumber, rowId, selectedPlugin));
        }

        if (selectedPlugin['allow_custom_fields']) {
            fieldMappingsAnchor.appendChild(
                createCustomMappings(layout_form, rowNumber, columnNumber));
        }
    };
    selectPlugin.oncuechange = selectPlugin.onchange;
    selectPluginCol.appendChild(selectPlugin);

    // Adding options (Plugins) to select

    for (let key in availablePlugins) {

        let plugin = availablePlugins[key];

        let selectPluginOption = document.createElement('option');
        selectPluginOption.value = plugin.id;
        selectPluginOption.text = plugin.name;
        selectPlugin.appendChild(selectPluginOption);
    }

    return selectPluginRow;
}

function createWidthSelector(rowNumber, columnNumber) {

    let inputId = 'row-' + rowNumber + '-col-' + columnNumber + '-width';

    let {row: selectWidthRow, col: selectWidthCol} = createPluginRow();

    let selectWidthInputLabel = document.createElement('label');
    selectWidthInputLabel.setAttribute('for', inputId);
    selectWidthInputLabel.textContent = 'Width:';
    selectWidthCol.appendChild(selectWidthInputLabel);

    let selectWidthInput = document.createElement('input');
    selectWidthInput.setAttribute('type', 'range');
    selectWidthInput.setAttribute('id', inputId);
    selectWidthInput.setAttribute('name', inputId);
    selectWidthInput.setAttribute('class', 'custom-range');
    selectWidthInput.setAttribute('value', '12');
    selectWidthInput.setAttribute('max', '12');
    selectWidthInput.setAttribute('min', '3');
    selectWidthInput.onchange = () => {
        let rows = document.getElementById('layout-form')['rows'];
        let columns = rows.get(rowNumber).columns;
        let column = columns[columnNumber];
        let columnEditor = column.column_div;

        let widthSum = 0;
        columns.map((col) => {
            widthSum += Number(col.column_width);
        })
        let maxWidth = 12 - (widthSum - Number(column.column_width));

        column.column_width = String(
            selectWidthInput.value > maxWidth ? maxWidth : selectWidthInput.value);
        selectWidthInput.value = column.column_width;

        let editorClass = 'col-' + column.column_width + ' ' + 'offset-' + column.column_offset;
        columnEditor.setAttribute('class', editorClass)
    }
    selectWidthCol.appendChild(selectWidthInput);

    return selectWidthRow;
}

function createOffsetSelector(rowNumber, columnNumber) {

    // TODO: Find a smarter solution for offset

    let inputId = 'row-' + rowNumber + '-col-' + columnNumber + '-offset';

    let {row: selectOffsetRow, col: selectOffsetCol} = createPluginRow();

    let selectOffsetInputLabel = document.createElement('label');
    selectOffsetInputLabel.setAttribute('for', inputId);
    selectOffsetInputLabel.textContent = 'Offset:';
    selectOffsetCol.appendChild(selectOffsetInputLabel);

    let selectOffsetInput = document.createElement('input');
    selectOffsetInput.setAttribute('type', 'range');
    selectOffsetInput.setAttribute('id', inputId);
    selectOffsetInput.setAttribute('name', inputId);
    selectOffsetInput.setAttribute('class', 'custom-range');
    selectOffsetInput.setAttribute('value', '0');
    selectOffsetInput.setAttribute('max', '9');
    selectOffsetInput.setAttribute('min', '0');
    selectOffsetInput.onchange = () => {
        let rows = document.getElementById('layout-form')['rows'];
        let columns = rows.get(rowNumber).columns;
        let column = columns[columnNumber];
        let columnEditor = column.column_div;

        let widthSum = 0;
        columns.map((col) => {
            widthSum += Number(col.column_width);
        })
        let maxOffset = 12 - widthSum;

        column.column_offset = String(
            selectOffsetInput.value > maxOffset ? maxOffset : selectOffsetInput.value);
        selectOffsetInput.value = column.column_offset;

        let editorClass = 'col-' + column.column_width + ' ' + 'offset-' + column.column_offset;
        columnEditor.setAttribute('class', editorClass)
    }
    selectOffsetCol.appendChild(selectOffsetInput);

    return selectOffsetRow;
}

function createFieldMappings(layout_form, rowNumber, columnNumber, pluginRowId, selectedPlugin) {

    let inputId = 'row-' + rowNumber + '-col-' + columnNumber + '-field';

    let fieldMappingsContainer = document.createElement('div');
    fieldMappingsContainer.setAttribute('class', 'container');
    fieldMappingsContainer.setAttribute('id', inputId + '-container');

    fieldMappingsContainer.style.padding = '0px';

    selectedPlugin['fields'].forEach((fieldId) => {
        fieldMappingsContainer.appendChild(createMappingInput(layout_form, inputId, fieldId, pluginRowId))
    });

    return fieldMappingsContainer;
}

function createCustomMappings(layout_form, rowNumber, columnNumber) {

    let inputId = 'row-' + rowNumber + '-col-' + columnNumber + '-custom-mappings';

    let customMappingsContainer = document.createElement('div');
    customMappingsContainer.setAttribute('class', 'container');
    customMappingsContainer.setAttribute('id', inputId + '-container');

    customMappingsContainer.style.padding = '0px';

    // Creating a list to show the added custom mappings in.

    let customMappingsListContainer = document.createElement('div');
    customMappingsListContainer.style.marginTop = '8px';
    customMappingsContainer.appendChild(customMappingsListContainer)

    let customMappingsListLabel = document.createElement('div');
    customMappingsListLabel.setAttribute('for', inputId + 'custom-mappings-list');
    customMappingsListLabel.textContent = "Custom Fields:";
    customMappingsListContainer.appendChild(customMappingsListLabel);

    let customMappingsList = document.createElement('div');
    customMappingsList.setAttribute('id', inputId + 'custom-mappings-list')
    customMappingsListContainer.appendChild(customMappingsList);

    // Creating a row to show the add custom mapping button in.

    let addCustomMappingButtonRow = document.createElement('div');
    addCustomMappingButtonRow.setAttribute('class', 'row');
    addCustomMappingButtonRow.style.marginTop = '6px';
    customMappingsContainer.appendChild(addCustomMappingButtonRow);

    let addCustomMappingButtonCol = document.createElement('div');
    addCustomMappingButtonCol.setAttribute('class', 'col');
    addCustomMappingButtonRow.appendChild(addCustomMappingButtonCol);

    // Initializing a custom mapping counter
    layout_form['custom_mappings_added'] = 0;

    let addCustomMappingButton = document.createElement('div');
    addCustomMappingButton.setAttribute('class', 'form-control btn btn-dark');
    addCustomMappingButton.onclick = () => {

        // Right now we allow a maximum of 10 custom mappings.
        // This is set by a constant in the abstract page manager.
        // TODO: This should be generalized - common config?
        if (layout_form['custom_mappings_added'] < 10) {

            let customMappingRow = document.createElement('div');
            customMappingRow.setAttribute('class', 'row');
            customMappingRow.style.marginTop = '6px';
            customMappingsList.appendChild(customMappingRow);

            let customMappingCol = document.createElement('div');
            customMappingCol.setAttribute('class', 'col');
            customMappingRow.appendChild(customMappingCol);

            let fieldId = 'custom-field-' + layout_form['custom_mappings_added']
            let inputId = 'row-' + rowNumber + '-col-' + columnNumber;

            customMappingCol.appendChild(createColumnSelector(layout_form, inputId, fieldId));

            layout_form['custom_mappings_added'] += 1;
        }
    };
    addCustomMappingButtonCol.appendChild(addCustomMappingButton);

    let addCustomMappingButtonIcon = document.createElement('i');
    addCustomMappingButtonIcon.setAttribute('class', 'fas fa-plus-circle');
    addCustomMappingButton.appendChild(addCustomMappingButtonIcon);

    return customMappingsContainer;
}

function createMappingInput(layout_form, inputId, fieldId) {

    // Creating an input for the required field title TODO: its own function?
    let fieldMappingTitleContainer = document.createElement('div');
    fieldMappingTitleContainer.setAttribute('class', 'container');
    fieldMappingTitleContainer.setAttribute('id', inputId + '-title');

    fieldMappingTitleContainer.style.padding = '0px';

    let fieldMappingLabel = document.createElement('label');
    fieldMappingLabel.setAttribute('for', inputId + '-title-input');
    fieldMappingLabel.setAttribute('id', inputId + '-title-label');
    fieldMappingLabel.innerText = fieldId.toString();
    fieldMappingTitleContainer.appendChild(fieldMappingLabel);

    fieldMappingTitleContainer.appendChild(createColumnSelector(layout_form, inputId, fieldId));

    return fieldMappingTitleContainer;
}

function createColumnSelector(layout_form, inputId, fieldId) {

    let asset_type_columns = layout_form['asset_type']['columns'];

    let fieldMappingSelector = document.createElement('select');
    fieldMappingSelector.setAttribute('class', 'form-control');
    fieldMappingSelector.setAttribute('name', inputId + '-' + fieldId);

    asset_type_columns.forEach((column) => {

        let columnOption = document.createElement('option');
        columnOption.value = column['db_name'];
        columnOption.text = column['name'];
        fieldMappingSelector.appendChild(columnOption);
    });
    return fieldMappingSelector;
}

// CREATE PLUGIN FUNCTION
// ~~~~~~~~~~~~~~~~~~~~~~

function createPlugin() {

    const container = document.getElementById('container');
    const layout_form = document.getElementById('layout-form');

    layout_form['rows'] = new Map();

    if (layout_form['detail_view']) {
        layout_form.appendChild(createTitleRow(layout_form));

        let divider = document.createElement('hr');
        divider.style.marginLeft = '-15px';
        divider.style.marginRight = '-15px';
        layout_form.appendChild(divider);
    }

    layout_form.appendChild(createRow(layout_form));
    container.appendChild(createAddRowButton(layout_form));
}
