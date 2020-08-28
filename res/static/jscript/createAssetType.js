// Auth: PDT
// Since: 2020/08/25

// This is the script used in create-asset-type.html

let columnsAdded = new Set();
let columnNumber = 0;

function addColumn() {
    if (columnsAdded.size < 15) {

        while (columnsAdded.has(columnNumber)) {
            columnNumber = (columnNumber + 1) % 15;
        }

        const columnList = document.getElementById('column-list');

        let columnEntry = document.createElement('div');
        columnEntry.setAttribute('id', 'column-entry-' + columnNumber);
        columnEntry.setAttribute('class', 'form-group card');
        columnList.appendChild(columnEntry);

        let cardBody = document.createElement('div');
        cardBody.setAttribute('class', 'card-body');
        columnEntry.appendChild(cardBody);

        let cardBodyRow = document.createElement('div');
        cardBodyRow.setAttribute('class', 'row');
        cardBody.appendChild(cardBodyRow);

        // Adding Remove Column Button

        let removeColumn = document.createElement('div');
        removeColumn.setAttribute('class', 'col-md-1');
        cardBodyRow.appendChild(removeColumn);

        let removeColumnButton = document.createElement('button');
        removeColumnButton.setAttribute('type', 'button');
        removeColumnButton.setAttribute('id', columnNumber);
        removeColumnButton.onclick = function () {
            let column = document.getElementById('column-entry-' + removeColumnButton.id);
            column.parentElement.removeChild(column);
            columnsAdded.delete(parseInt(removeColumnButton.id));
        }
        removeColumnButton.style.border = 'none';
        removeColumnButton.style.backgroundColor = 'Transparent';
        removeColumnButton.style.cursor = 'pointer';
        removeColumnButton.style.outline = 'none';
        removeColumn.appendChild(removeColumnButton);

        let removeColumnButtonIcon = document.createElement('i');
        removeColumnButtonIcon.setAttribute(
            'class', 'far fa-times-circle');
        removeColumnButton.appendChild(removeColumnButtonIcon);

        // Adding Column Name Input

        let columnName = document.createElement('div');
        columnName.setAttribute('class', 'col-md-6');
        cardBodyRow.appendChild(columnName);

        let columnNameInput = document.createElement('input');
        columnNameInput.setAttribute('class', 'form-control');
        columnNameInput.setAttribute('type', 'text');
        columnNameInput.setAttribute('name', 'column-name-' + columnNumber);
        columnName.appendChild(columnNameInput);

        // Adding Data Type Input

        let columnDataType = document.createElement('div');
        columnDataType.setAttribute('class', 'col-md-4');
        cardBodyRow.appendChild(columnDataType);

        let columnDataTypeRow = document.createElement('div');
        columnDataTypeRow.setAttribute('class', 'row');
        columnDataType.appendChild(columnDataTypeRow);

        let columnDataTypeSelectColumn = document.createElement('div');
        columnDataTypeSelectColumn.setAttribute('class', 'col-md-6');
        columnDataTypeRow.appendChild(columnDataTypeSelectColumn);

        let columnDataTypeSelect = document.createElement('select');
        columnDataTypeSelect.setAttribute('class', 'form-control custom-select');
        columnDataTypeSelect.setAttribute('name', 'column-data-type-' + columnNumber);
        columnDataTypeSelect.onchange = function () {
            dataTypeSelection(
                columnDataTypeSelect.name,
                columnDataTypeSelect.value
            );
        };
        columnDataTypeSelectColumn.appendChild(columnDataTypeSelect);

        for (let key in dataTypes) {
            let dataType = dataTypes[key];
            let columnDataTypeSelectOption = document.createElement('option');
            columnDataTypeSelectOption.value = dataType['typename'];
            columnDataTypeSelectOption.text = dataType['fe_name'];
            columnDataTypeSelect.appendChild(columnDataTypeSelectOption);
        }

        // Adding Asset Type Input

        let columnAssetTypeSelectColumn = document.createElement('div');
        columnAssetTypeSelectColumn.setAttribute('class', 'col-md-6');
        columnDataTypeRow.appendChild(columnAssetTypeSelectColumn);

        let columnAssetTypeSelect = document.createElement('select');
        columnAssetTypeSelect.setAttribute('class', 'form-control custom-select');
        columnAssetTypeSelect.setAttribute('id', 'column-asset-type-' + columnNumber);
        columnAssetTypeSelect.setAttribute('name', 'column-asset-type-' + columnNumber);
        columnAssetTypeSelectColumn.appendChild(columnAssetTypeSelect);

        for (let key in assetTypes) {
            let assetType = assetTypes[key];
            let columnAssetTypeSelectOption = document.createElement('option');
            columnAssetTypeSelectOption.setAttribute('value', key);
            columnAssetTypeSelectOption.textContent = assetType['asset_name'];
            columnAssetTypeSelect.appendChild(columnAssetTypeSelectOption);
        }

        // Adding Required Input

        let columnRequired = document.createElement('div');
        columnRequired.setAttribute('class', 'col-md-1');
        cardBodyRow.appendChild(columnRequired);

        let columnRequiredInput = document.createElement('input');
        columnRequiredInput.setAttribute('type', 'checkbox');
        columnRequiredInput.setAttribute('class', 'form check-input');
        columnRequiredInput.setAttribute('name', 'column-required-' + columnNumber);
        columnRequiredInput.setAttribute('value', 'checkboxTrue');
        columnRequiredInput.checked = false;
        columnRequired.appendChild(columnRequiredInput);

        columnsAdded.add(columnNumber);
    } else {
        console.warn("Can't create more than 15 Columns!");
    }
}

function dataTypeSelection(name, value) {

    const entryNumber = name.toString().slice(-1);
    const atSelection = document.getElementById(
        'column-asset-type-' + entryNumber);

    if (['ASSET', 'ASSETLIST'].includes(value)) {
        atSelection.style.visibility = "visible";
    } else {
        atSelection.style.visibility = "hidden";
    }
}

addColumn();

let first_entry = document.getElementById('column-data-type-0');
console.log(first_entry);