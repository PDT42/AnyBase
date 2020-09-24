// Auth: PDT
// Since: 2020/09/23
//
// This script contains the functions used in the 'asset-details-plugin'.

// CREATE ELEMENTS
// ~~~~~~~~~~~~~~~

function createDetailsContainer(asset, assetType, fieldMappings) {

    let pluginRootContainer = document.createElement('div');

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

function createPlugin(columnId) {

    let assetRoot = document.getElementById('asset-root');
    let pluginRoot = document.getElementById('column-' + columnId);

    let fieldMappings = pluginRoot['fieldMappings'];
    let asset = assetRoot['asset'];
    let assetType = assetRoot['assetType'];

    pluginRoot.appendChild(createDetailsContainer(asset, assetType, fieldMappings));
}