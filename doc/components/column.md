# Column
Columns are entities, that define what the content of an asset should be. The [AssetType] of an [Asset] has a list of columns and by those, defines the expected content of the [Asset]s ``data`` field. 

![Column Class][column_class]

The fields of the Column class are pretty self explanatory. The ``name`` of the Column stores the name the user, who created the [AssetType] this Column belongs to, gave it. The field ``db_name`` is an generic conversion of the ``name`` into a format, which the database will accept as a column name. Right now it is created by: 

```python
column_db_name = column_name.replace(' ', '_').lower()
```

The ``datatype`` field contains the DataType object, that describes the data type of the column. The field ``asset_type`` is set to zero by default and is only required if the ``datatype`` of the column is either ``ASSET`` or ``ASSETLIST``. In those cases it defines the [AssetType] of the [Asset] referenced or, in case of ``ASSETLIST`` the [AssetType] of each of the [Asset]s referenced in the list.

[//]: # (LINKS)
[AssetType]: asset_types.md
[Asset]: asset.md

[//]: # (IMAGES)
[column_class]: graphics/plantuml_rendered/column.png