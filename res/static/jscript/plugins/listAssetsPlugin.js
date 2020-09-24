// Auth: PDT
// Since: 2020/09/20
//
// This is the script used by the list-assets-plugin.html template.

// CREATE ELEMENTS
// ~~~~~~~~~~~~~~~

function createAssetList(column_info) {

    let id = column_info['column_id'];

    let assetListContainer = document.createElement('div');
    assetListContainer.setAttribute('class', 'container');
    assetListContainer.setAttribute('id', 'plugin-container-' + id);

    let assetListRow = document.createElement('div');
    assetListRow.setAttribute('id', 'asset-list-row-' + id);
    assetListRow.setAttribute('class', 'row');
    assetListContainer.appendChild(assetListRow)

    let assetListCol = document.createElement('div');
    assetListCol.setAttribute('id', 'asset-list-col-' + id);
    assetListCol.setAttribute('class', 'col');
    assetListRow.appendChild(assetListCol)

    assetListCol.style.padding = '0px';

    return [assetListContainer, assetListRow, assetListCol];
}

function createListItem(item, field_mappings, column_id, asset_type) {

    // Create a unique id, for each of the listed items
    let listItemId = 'layout-col-' + column_id + '-list-item-' + item['asset_id'];

    // Create a underlying shadow box
    let listItem = document.createElement('div');
    listItem.setAttribute('id', listItemId);
    listItem.setAttribute('class', 'container shadow-sm p-1 mb-3 bg-white rounded');
    listItem.setAttribute('id', listItemId + '-shadow-box');

    // Create container for the list item
    let listItemHeaderContainer = document.createElement('div');
    listItemHeaderContainer.setAttribute('class', 'container');
    listItemHeaderContainer.setAttribute('id', listItemId + '-header-container');
    listItemHeaderContainer.style.marginTop = '8px';
    listItem.appendChild(listItemHeaderContainer);

    listItemHeaderContainer.appendChild(
        createListItemHeader(item, listItemId, field_mappings['field-title'], asset_type['asset_type_id']))

    let headerDivider = document.createElement('hr');
    headerDivider.style.marginTop = '6px';
    headerDivider.style.marginBottom = '6px';
    listItemHeaderContainer.appendChild(headerDivider);

    return listItem;
}

function createListItemHeader(item, listItemId, fieldMapping, asset_type_id) {

    let listItemHeaderRow = document.createElement('div');
    listItemHeaderRow.setAttribute('class', 'row');
    listItemHeaderRow.setAttribute('id', listItemId + '-header-row');

    let listItemHeaderTitleCol = document.createElement('div');
    listItemHeaderTitleCol.setAttribute('class', 'col');
    listItemHeaderTitleCol.setAttribute('id', listItemId + '-header-column');
    listItemHeaderRow.appendChild(listItemHeaderTitleCol);

    let titleLink = document.createElement('a')
    titleLink.href = '/asset-type:' + asset_type_id + '/asset:' + item['asset_id'];
    listItemHeaderTitleCol.appendChild(titleLink)

    let title = document.createElement('h7');
    title.innerText = item.data[fieldMapping];
    title.style.marginBottom = '4px';
    titleLink.appendChild(title);

    return listItemHeaderRow;
}

// CREATE PLUGIN FUNCTION
// ~~~~~~~~~~~~~~~~~~~~~~

// TODO: Store asset_type in root
function createPlugin(column_info, asset_type) {

    const asset_type_root = document.getElementById('asset-type-root');
    const plugin_root = document.getElementById('column-' + column_info.column_id);

    let field_mappings = column_info['field_mappings'];
    let column_id = column_info['column_id'];

    let [item_list_container, item_list_row, item_list_col] = createAssetList(column_info);
    plugin_root.appendChild(item_list_container);

    // Register this plugins callback in stream data
    asset_type_root['stream_data'].get('stream-assets').subscribers.push((data => {

        data.forEach((item) => {
            item_list_col.appendChild(createListItem(item, field_mappings, column_id, asset_type))
        });
    }))
}