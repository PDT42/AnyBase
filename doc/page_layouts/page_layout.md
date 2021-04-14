# PageLayouts

_PageLayouts_ store the information on what a frontend view should look like. This information is served
to the frontend by the [AssetServer] and [AssetTypeServer], who inturn use the [PageManager] to interact
with the underlying database. The _PageLayout_ is the third entity after Asset/Type to get their own manager.

_PageLayouts_ are used to generate views. For each [AssetType], there are two views, the user can configure
however he likes. The _AssetTypeOverView_ (no pun intended🤞) and the _AssetDetailView_. Both of these are
defined on a per [AssetType] base, so don't be confused by the name _AssetDetailView_. Tho it is used to
show views, designed to inspect the ``data`` of a single [Asset], the information on what the view should
look like will still be the same for each [Asset] of the Type.

A _PageLayout_ must contain all the data necessary to generate a view for a specified Asset/Type dataset.

The user configures both the _AssetTypeOverView_ and the _AssetDetailView_ himself. The information he inputs
is processed in the ``APageManager``'s method ``get_page_layout_from_form_data``. The method's name says
it all. It returns a backend ``PageLayout`` type object.

## Backend Representation - The _PageLayout's_ Fields

In the python backend, the _PageLayout_ just as the [AssetType] and [Asset] is implemented as a [dataclass].

![page_layout_class][page_layout_class]

### Field Descriptions:
* ``asset_type_id``: Specifies the asset_type, this layout is meant for.
* ``asset_page_layout``: Specifies, whether this is a  or not.
* ``layout``: field to store the layout the user configured for the view.
* ``field_mappings``: Mapping from frontend field values to ``AssetType`` fields.
* ``created``: Time (to the second), when this layout was created.
* ``updated``: Time (to the second), when this layout was last updated.
* ``sources``: Mapping to the sources and actions the view/page uses.
* ``layout_id``: Unique id of the ``PageLayout`` (-> primary_key)


## The Layout

![page_layout][page_layout]

The ``PageLayout`` is implemented as a [dataclass] in the python backend. 



[//]: # (LINKS)
[AssetType]: ../components/asset_types.md
[AssetTypeServer]: ../servers/asset_type_server.md
[PageManager]: ../managers/page_manager.md
[dataclass]: https://docs.python.org/3/library/dataclasses.html

[//]: # (IMAGES)
[page_layout]: graphics/rendered_images/AssetTypeOverviewViewSketch_labeled.png
[page_layout_class]: graphics/rendered_images/page_layout.png