// Auth: PDT
// Since: 2020/09/23
//
// This script contains the functions used in the 'asset-details-plugin'.

// CREATE ELEMENTS
// ~~~~~~~~~~~~~~~

function createDetailsContainer(asset, assetType, fieldMappings) {

    let pluginRootContainer = document.createElement('div');
    pluginRootContainer.setAttribute('class', 'container shadow-sm p-3 mb-1 bg-white rounded')
    pluginRootContainer.style.padding = '0px';

    // Adding header row to asset detail plugin view
    // °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    let assetDetailHeaderRow = document.createElement('div');
    assetDetailHeaderRow.setAttribute('class', 'row');
    pluginRootContainer.appendChild(assetDetailHeaderRow);

    let assetDetailHeaderCol = document.createElement('div');
    assetDetailHeaderCol.setAttribute('class', 'col');
    assetDetailHeaderRow.appendChild(assetDetailHeaderCol);

    let assetDetailHeader = document.createElement('h6');
    assetDetailHeader.innerText = 'Asset Details:';
    assetDetailHeader.style.marginBottom = '6px';
    assetDetailHeaderCol.appendChild(assetDetailHeader);

    Object.entries(fieldMappings).forEach(([field, mapping]) => {

        pluginRootContainer.appendChild(createFieldView(asset, assetType, mapping));
    })

    return pluginRootContainer;
}

function createFieldView(asset, assetType, mapping) {

    let value = asset['data'][mapping];
    let column = assetType['columns'].filter(col => col['db_name'] === mapping)[0];
    let columnName = column['name'];
    let columnDataTypeName = column['datatype']['typename'];

    let fieldContainer = document.createElement('div');
    fieldContainer.setAttribute('class', 'row');
    fieldContainer.style.paddingTop = '10px';

    {
        let fieldLabelColumn = document.createElement('div');
        fieldLabelColumn.setAttribute('class', 'col-6');
        fieldContainer.appendChild(fieldLabelColumn);

        let fieldLabelText = document.createElement('span');
        fieldLabelText.textContent = columnName.toString() + ':';
        fieldLabelColumn.appendChild(fieldLabelText);

        let fieldValueColumn = document.createElement('div');
        fieldValueColumn.setAttribute('class', 'col-6');
        fieldContainer.appendChild(fieldValueColumn);

        if (columnDataTypeName === 'ASSET') {

            let fieldValueText = document.createElement('a');
            fieldValueText.setAttribute('href',
                '/asset-type:' + assetType['asset_type_id'] +
                '/asset:' + asset['asset_id']);
            fieldValueText.textContent = value.toString();
            fieldValueColumn.appendChild(fieldValueText);

        } else if (columnDataTypeName === 'ASSETLIST') {

            let fieldValueText = document.createElement('a');
            fieldValueText.setAttribute('href',
                '/asset-type:' + assetType['asset_type_id']);
            fieldValueText.textContent = assetType['asset_name'];
            fieldValueColumn.appendChild(fieldValueText);

        } else {

            let fieldValueText = document.createElement('input');
            fieldValueText.value = value.toString();
            toString();
            fieldValueText.setAttribute('class', 'form-control');
            fieldValueText.disabled = true;
            fieldValueColumn.appendChild(fieldValueText);
        }
    }
    return fieldContainer;
}

// CREATE PLUGIN FUNCTION
// ~~~~~~~~~~~~~~~~~~~~~~

function createPlugin(root_id, column_info) {

    let assetRoot = document.getElementById(root_id);
    let pluginRoot = document.getElementById('column-' + column_info['column_id']);

    let fieldMappings = column_info['field_mappings'];
    let asset = assetRoot['asset'];
    let assetType = assetRoot['assetType'];

    pluginRoot.appendChild(createDetailsContainer(asset, assetType, fieldMappings));
}