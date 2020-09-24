# PageManager

The ``PageManager`` does exactly what the name suggests. He manages pages. Pages, or to call the
child by its backend name [PageLayout]s, define what the user gets to see, when he opens the 
overview or detail view of an [AssetType].

The ``PageManager`` is located in the manager layer and serves the [AssetTypeServer], as well as 
the [AssetServer], with the [PageLayout]s they send to the user. Just as all the other managers 
of [AnyBase], it represents the connection between the [DbConnection] and the main application. It can 
be used to store, get, update and overall manager [PageLayout]s in the database.

The information on the [Plugin]s used in the [PageLayout]s ``layout[i][j]`` [ColumnInfo]

[//]: # (LINKS)
[PageLayout]: https://github.com/PDT420/AnyBase/blob/master/doc/components/page_layouts.md
[AssetType]: https://github.com/PDT420/AnyBase/blob/master/doc/components/asset_types.md
[AssetTypeServer]: https://github.com/PDT420/AnyBase/blob/master/doc/servers/asset_type_server.md
[AssetServer]: https://github.com/PDT420/AnyBase/blob/master/doc/servers/asset_server.md
[DbConnection]: https://github.com/PDT420/AnyBase/blob/master/doc/database/db_connection.md
[Column]: https://github.com/PDT420/AnyBase/blob/master/doc/components/column.md

[//]: # (IMAGES)