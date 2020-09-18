# PageLayouts

``PageLayouts`` store the information on what a frontend view should look like. This information is served
to the frontend by the [AssetServer] and [AssetTypeServer], who are in turn served by the [PageManager].

> Right now ``PageLayouts`` are the most complex entity of the project.

``PageLayouts`` are used to generate views. For each AssetType, there are two views, the user can configure
however he likes. 

## The Layout

![page_layout][page_layout]

The ``PageLayout`` is implemented as a [dataclass] in the python backend. 

![page_layout_class][page_layout_class]

* ``asset_type_id``: Specifies the asset_type, this layout is meant for.
* ``asset_page_layout``: Specifies, whether this is a detail page or not.
* ``layout``: field to store the layout the user configured for the view.
* ``field_mappings``: Mapping from frontend field values to ``AssetType`` fields.
* ``created``: Time (to the second), when this layout was created.
* ``updated``: Time (to the second), when this layout was last updated.
* ``sources``: Mapping to the sources and actions the view/page uses.
* ``layout_id``: Unique id of the ``PageLayout`` (-> primary_key)

[//]: # (LINKS)
[AssetType]: https://github.com/PDT420/AnyBase/blob/master/doc/components/asset_types.md
[AssetTypeServer]: https://github.com/PDT420/AnyBase/blob/master/doc/servers/asset_type_server.md
[PageManager]: https://github.com/PDT420/AnyBase/blob/master/doc/managers/page_manager.md
[dataclass]: https://docs.python.org/3/library/dataclasses.html

[//]: # (IMAGES)
[page_layout]: graphics/rendered_images/AssetTypeOverviewViewSketch_labeled.png
[page_layout_class]: graphics/rendered_images/page_layout.png