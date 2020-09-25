// Auth: PDT
// Since: 2020/09/24
//
// This script contains the functions used in the 'basic-notes-plugin'.

// CREATE ELEMENTS
// ~~~~~~~~~~~~~~~

function createNotesContainer(column_info) {

    // TODO: Refactor this!
    // CHECKOUT: Move Container Creation to jinja template ?!

    let id = column_info['column_id'];

    let notesContainer = document.createElement('div');
    notesContainer.setAttribute('class', 'container shadow-sm p-3 mb-1 bg-white rounded');
    notesContainer.setAttribute('id', 'plugin-container-' + id);
    notesContainer.style.padding = '0px';

    // Header for the notes plugin view
    // °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    let notesHeaderRow = document.createElement('div');
    notesHeaderRow.setAttribute('class', 'row');
    notesContainer.appendChild(notesHeaderRow);

    let notesHeaderCol = document.createElement('div');
    notesHeaderCol.setAttribute('class', 'col');
    notesHeaderRow.appendChild(notesHeaderCol);

    let notesHeader = document.createElement('h6');
    notesHeader.innerText = "Notes:"
    notesHeader.style.marginBottom = '6px';
    notesHeaderCol.appendChild(notesHeader);

    let assetListRow = document.createElement('div');
    assetListRow.setAttribute('class', 'row');
    assetListRow.setAttribute('id', 'notes-list-row-' + id);
    notesContainer.appendChild(assetListRow)

    let assetListCol = document.createElement('div');
    assetListCol.setAttribute('class', 'col');
    assetListCol.setAttribute('id', 'notes-list-col-' + id);
    assetListRow.appendChild(assetListCol)

    return [notesContainer, assetListRow, assetListCol];
}

function createNoteInput(column_info) {

    let column_id = column_info['column_id'];
    let fieldMappings = column_info['field_mappings'];
    let create_route = column_info['sources']['create-note'];

    let noteInputRow = document.createElement('form');
    noteInputRow.setAttribute('class', 'form-row shadow-sm p-3 mb-1 bg-white rounded');
    noteInputRow.setAttribute('id', 'notes-input-row-column-' + column_id);
    noteInputRow.setAttribute('action', create_route);
    noteInputRow.setAttribute('method', 'POST');

    let noteInputCol = document.createElement('div');
    noteInputCol.setAttribute('class', 'col');
    noteInputCol.setAttribute('id', 'notes-input-col-column-' + column_id);
    noteInputRow.appendChild(noteInputCol)

    // Add header row to input
    // °°°°°°°°°°°°°°°°°°°°°°°
    let noteInputHeaderRow = document.createElement('div');
    noteInputHeaderRow.setAttribute('class', 'form-group row');
    noteInputHeaderRow.style.marginTop = '6px';
    noteInputHeaderRow.style.marginBottom = '6px';
    noteInputCol.appendChild(noteInputHeaderRow);

    let noteInputHeaderCol = document.createElement('div');
    noteInputHeaderCol.setAttribute('class', 'col');
    noteInputHeaderRow.appendChild(noteInputHeaderCol);

    let noteInputHeader = document.createElement('h6');
    noteInputHeader.innerText = 'Post a Note:'
    noteInputHeader.style.marginBottom = '0px';
    noteInputHeaderCol.appendChild(noteInputHeader);

    let divider = document.createElement('hr');
    divider.style.marginTop = '6px';
    divider.style.marginBottom = '6px';
    noteInputCol.appendChild(divider);

    // Add note title input
    // °°°°°°°°°°°°°°°°°°°°
    let noteTitleTextInputRow = document.createElement('div');
    noteTitleTextInputRow.setAttribute('class', 'form-group row');
    noteInputCol.appendChild(noteTitleTextInputRow);

    let noteTitleTextInputCol = document.createElement('div');
    noteTitleTextInputCol.setAttribute('class', 'col');
    noteTitleTextInputRow.appendChild(noteTitleTextInputCol);

    let noteTitleTextLabel = document.createElement('label');
    noteTitleTextLabel.innerText = 'Title:'
    noteTitleTextInputCol.appendChild(noteTitleTextLabel);

    let noteTitleTextInput = document.createElement('input');
    noteTitleTextInput.setAttribute('class', 'form-control form-control-sm');
    noteTitleTextInput.setAttribute('name', fieldMappings['title']);
    noteTitleTextInputCol.appendChild(noteTitleTextInput);

    // Add text input area
    // °°°°°°°°°°°°°°°°°°°
    let noteInputTextAreaRow = document.createElement('div');
    noteInputTextAreaRow.setAttribute('class', 'form-group row');
    noteInputTextAreaRow.style.marginTop = '6px';
    noteInputTextAreaRow.style.marginBottom = '6px';
    noteInputCol.appendChild(noteInputTextAreaRow);

    let noteInputTextAreaCol = document.createElement('div');
    noteInputTextAreaCol.setAttribute('class', 'col');
    noteInputTextAreaCol.setAttribute('for', 'notes-input-title-field-column-' + column_id);
    noteInputTextAreaRow.appendChild(noteInputTextAreaCol);

    let noteTextAreaLabel = document.createElement('label');
    noteTextAreaLabel.innerText = 'Note:'
    noteInputTextAreaCol.appendChild(noteTextAreaLabel);

    let noteInputField = document.createElement('textarea');
    noteInputField.setAttribute('class', 'form-control');
    noteInputField.setAttribute('name', fieldMappings['note']);
    noteInputField.setAttribute('id', 'notes-input-title-field-column-' + column_id);
    noteInputTextAreaCol.appendChild(noteInputField)

    // Add post note button area
    // °°°°°°°°°°°°°°°°°°°°°°°°°

    let noteInputPostButtonRow = document.createElement('div');
    noteInputPostButtonRow.setAttribute('class', 'row');
    noteInputCol.appendChild(noteInputPostButtonRow);

    let noteInputPostButtonCol = document.createElement('div');
    noteInputPostButtonCol.setAttribute('class', 'col d-flex justify-content-end');
    noteInputPostButtonRow.appendChild(noteInputPostButtonCol);

    let noteInputPostButton = document.createElement('button');
    noteInputPostButton.setAttribute('class', 'btn btn-dark btn-sm');
    noteInputPostButton.setAttribute('type', 'submit');
    noteInputPostButton.innerText = 'Post';
    noteInputPostButtonCol.appendChild(noteInputPostButton);

    return noteInputRow;
}

function createNote(column_info, item) {

    let columnId = column_info['column_id'];
    let fieldMappings = column_info['field_mappings'];
    let noteId = 'column-' + columnId + '-note-' + item['asset_id'];

    let noteContainer = document.createElement('div');
    noteContainer.setAttribute('class', 'container shadow-sm p-3 mb-1 bg-white rounded');
    noteContainer.setAttribute('id', noteId + '-container');

    // Add the header to the note
    // °°°°°°°°°°°°°°°°°°°°°°°°°°

    let noteHeaderRow = document.createElement('div');
    noteHeaderRow.setAttribute('class', 'row');
    noteContainer.appendChild(noteHeaderRow);

    // Add title to note
    let noteTitleCol = document.createElement('div');
    noteTitleCol.setAttribute('class', 'col');
    noteHeaderRow.appendChild(noteTitleCol);

    let noteTitle = document.createElement('h6');
    noteTitle.innerText = item['data'][fieldMappings['title']];
    noteTitle.style.marginBottom = '6px';
    noteTitleCol.appendChild(noteTitle)

    // Add posted by to note
    let notePostedByCol = document.createElement('div');
    notePostedByCol.setAttribute('class', 'col d-flex justify-content-end');
    noteHeaderRow.appendChild(notePostedByCol);

    let notePostedBy = document.createElement('h9');
    notePostedBy.innerText = '#' + item['asset_id'];
    notePostedBy.style.marginBottom = '6px';
    notePostedByCol.appendChild(notePostedBy)

    // Add Body to note
    // °°°°°°°°°°°°°°°°

    let noteBodyRow = document.createElement('div');
    noteBodyRow.setAttribute('class', 'row');
    noteContainer.appendChild(noteBodyRow);

    let noteBodyCol = document.createElement('div');
    noteBodyCol.setAttribute('class', 'col');
    noteBodyRow.appendChild(noteBodyCol);

    let noteBodyTextArea = document.createElement('textarea');
    noteBodyTextArea.setAttribute('class', 'form-control');
    noteBodyTextArea.value = item['data'][fieldMappings['note']];
    noteBodyTextArea.disabled = 'true';
    noteBodyCol.appendChild(noteBodyTextArea);

    // Add Footer to note
    // °°°°°°°°°°°°°°°°°°

    let noteFooterRow = document.createElement('div');
    noteFooterRow.setAttribute('class', 'row');
    noteContainer.appendChild(noteFooterRow);

    let noteFooterCol = document.createElement('div');
    noteFooterCol.setAttribute('class', 'col d-flex justify-content-end');
    noteFooterRow.appendChild(noteFooterCol);

    let noteFooter = document.createElement('span');
    noteFooter.innerText = item[fieldMappings['user']] + ' - ' +
        (new Date(Number(item['created']))).toLocaleString();
    noteFooter.style.color = '#496FA0';
    noteFooter.style.fontSize = '12px';
    noteFooterCol.appendChild(noteFooter);

    return noteContainer;
}

// CREATE PLUGIN FUNCTION
// ~~~~~~~~~~~~~~~~~~~~~~

function createPlugin(root_id, column_info) {

    let root = document.getElementById(root_id);
    let pluginRoot = document.getElementById('column-' + column_info['column_id']);

    let [notesContainer, notesListRow, notesListCol] = createNotesContainer(column_info);

    let divider = document.createElement('hr');
    divider.style.marginBottom = '6px';
    divider.style.marginTop = '6px';
    notesContainer.appendChild(divider);

    notesContainer.append(createNoteInput(column_info));
    pluginRoot.appendChild(notesContainer);

    // Get the channel this plugin should subscribe to.
    // We do this by matching the name pattern of the
    // stream channel. The channel's name must start with
    // 'stream-' followed by the plugin name: 'basic_notes'.

    // °°°°°°°°°°°°°°°°°°°°°°°°°°

    root['stream_data'].forEach((obs_info, channel) => {

        if (channel.startsWith('stream-basic_notes')) {

            // Register this plugins callback in stream data.
            registerStreamDataCallback(root_id, channel, (items) =>
                items.forEach((item) =>
                    notesListCol.appendChild(
                        createNote(column_info, item)
                    )));
        }
    });
}