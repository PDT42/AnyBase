// Author: PDT
// Since: 2020/08/26

// This is the script used in create-asset.html


function createPlugin() {

    let root = document.getElementById('create-asset');

    // TODO: Get AssetType and available plugins another way.

    let form = document.createElement('form');
    form.setAttribute('class', 'col');
    form.setAttribute('action',
        '/asset-type:' + assetType['asset_type_id'] + '/create-asset');
    form.setAttribute('method', 'POST');
    root.appendChild(form);

    assetType['columns'].forEach(function (column) {

        let columnRow = document.createElement('div');
        columnRow.setAttribute('class', 'row');
        columnRow.setAttribute('id', 'row-' + column['db_name']);
        columnRow.style.paddingTop = '10px';
        form.appendChild(columnRow);

        {
            let labelColumn = document.createElement('div');
            labelColumn.setAttribute('class', 'col-4');
            columnRow.appendChild(labelColumn);

            {
                let label = document.createElement('span');
                label.textContent = column['name'];
                labelColumn.appendChild(label);
            }

            let inputColumn = document.createElement('div');
            inputColumn.setAttribute('class', 'col-8');
            columnRow.appendChild(inputColumn);

            if (column.datatype.typename === 'ASSET') {

                let assetInput = document.createElement('select');
                assetInput.setAttribute('class', 'form-control custom-select');
                assetInput.setAttribute('name', column['db_name']);
                inputColumn.appendChild(assetInput);

                assets[column.asset_type_id].forEach(function (asset) {
                    let option = document.createElement('option');
                    option.setAttribute('value', asset['asset_id']);
                    option.text = asset.data.name;
                    assetInput.appendChild(option);
                })
            } else if (column.datatype.typename === 'ASSETLIST') {

                let assetListInput = document.createElement('select');
                assetListInput.setAttribute('class', 'form-control custom-select');
                assetListInput.setAttribute('name', column['db_name']);
                inputColumn.appendChild(assetListInput);

                assets[column.asset_type_id].forEach(function (asset) {
                    let option = document.createElement('option');
                    option.setAttribute('value', asset['asset_id']);
                    option.textContent = asset['name'];
                    assetListInput.appendChild(option);
                })
            }
            else {

                let input = document.createElement('input');
                input.setAttribute('type', column['datatype']['fe_type']);
                input.setAttribute('step', 'any');
                input.setAttribute('class', 'form-control');
                input.setAttribute('name', column['db_name']);
                inputColumn.appendChild(input);
            }
        }
    });

    form.appendChild(document.createElement('hr'))

    let submitButtonRow = document.createElement('div');
    submitButtonRow.setAttribute('class', 'row justify-content-end');
    form.appendChild(submitButtonRow);

    let submitButtonColumn = document.createElement('col-2');
    submitButtonColumn.setAttribute('class', 'col-2');
    submitButtonRow.appendChild(submitButtonColumn);

    let submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.setAttribute('class', 'btn btn-block btn-dark');
    submitButton.textContent = 'Create';
    submitButtonColumn.appendChild(submitButton);
}