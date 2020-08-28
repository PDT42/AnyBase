# Asset Types

## Subtypes & Supertypes
Asset types are _the_ central element of AnyBase. They define the structure of [Asset]s managed by the software. To manage the asset types available, there is the asset type manager, which provides the database interface to store, edit and get asset types. [Asset]s come with one of two different types: There are __supertype__ and __subtype__ asset types. To create a subtype asset type, there must first exist a super type. A supertype asset type is basically any asset type, which is not a subtype. Still subtypes can themselves have subtypes. The asset type, a subtype asset type is sub to, is called __parent__. Subtypes realize an Extension Type.

>An AssetType is considered a subtype, if its ``super_type`` is less or equal to zero. This is just opportune, since every table, handled by AnyBase's DbConnection, defines a ``pimary_key`` which, for sqlite, starts at one and automatically increases with every row appended. In the future it might be sensable, to add a separate database column containing a true boolean, indicating, wether an AssetType is a subtype or not.

### Example: Subtypes & Supertypes
Consider the usecase of a library. They basically store (abstracted) only one AssetType - a "MediaArticle". Each such, has a "name", an "ISBN", a "purchase_date" etc. field. A Subtype now could be the AssetType "Book". A "Book" has all the fields of a "MediaArticle", but requires some additional ones as well. You should by now, see where this is going. The Subtype ("Book") _extends_ the Supertype ("MediaArticle"). This way the library has one central register ("abintern_asset_table_mediaarticle") containing all the "MediaArticles" they manage, but will be able to load the "Books" seperately. This will ease the type creation in the frontend, since the user will be able to just choose a supertype, and chain supertype hierarchies however he likes. He could for example create a type hierarchie like: "NonFiction" extends "Book" extends "MediaArticle". This way he does not have to create the same 15 fields over and over again. Another positive effect might be, that the user has an easy time keeping entities concise and layering them in tight definitions, which could have a positive effect on the loading time, when retrieving the items. 

// TODO: Insert Image for clarification

## Owner
An AssetType can define an ``owner_id``. Such an id suggests, that an asset_type is not independently interesting, but only as a field value for _another_ AssetType. The AssetType, who defines the field, the _owned AssetType_ is supposed to fill, is called the _owner_. Just as one might think, the ``owner_id`` persists the id of the _owner AssetType_. Though highly politically incorrect, the _owned AssetTypes_ are called _slave_ types. They exist to be used by their _owner_.
Since owned AssetTypes are not independently interesting, they are ignored by the AssetTypeManagers ``get_all`` functions. Instead, since we only ever want to get the slaves of one AssetType, the AssetTypeManager defines a separate method ``get_slaves``.

## Backend Representation

In the backend of the software an asset type is stored in a dataclass called ``AssetType``. All operations performed on asset types must use this as their input/output parameter type. An asset type should _never_ be handled in any other form in the backend. 

![Asset Type Class][asset_type_class]

Each asset type contains a list of [Column]s. This list defines the columns required from a database table, so [Asset]s of this type can be stored in it. It also contains an asset type id, which is filled database primary key. The column ``primary_key`` is automatically added to each asset type table. When creating a new asset type in the backend or using a frontend facility, the asset type does not need to set this field. When storing the asset type in the database, the current implementation of the asset type manager checks (and future implementations will and should probably do so) if an asset type with that asset name already exists in the database, if not the asset type is stored and the primary key is set for the asset type. When loading an asset type from the databse the 

## Database Representation

All of these asset types are stored in the database table ``abintern_asset_types``. On creation, for each asset type an additional table called ``abasset_table_{asset_name}``. The table name is generated from the name of the asset type. The manner in which the table names are generated from the name is part of the abstract implementation of the asset type manager, to guarantee, that future implementations of the asset type manager will still be able to access these tables. The table name generation is provided by the static method ``generate_asset_table_name``. 

![Asset Type Database Representation][asset_type_db]

The fieldnames suggest the content. The only interesting one being ``asset_columns``. Since the [Column] is also an item defined by AnyBase, in this field we store a string representation of the columns. This representation must be the formatted the same way in each future version to guarantee interoperability, which is why the generation of the representation is part of the abstracth implementation of the asset type manager.

[//]: # (LINKS)
[Column]: https://github.com/PDT420/AnyBase/blob/master/doc/components/column.md
[Asset]: https://github.com/PDT420/AnyBase/blob/master/doc/components/assets.md

[//]: # (IMAGES)
[asset_type_class]: graphics/plantuml_rendered/asset_type_class.png "Asset Type Class"
[asset_type_db]: graphics/plantuml_rendered/asset_type_db.png "Asset Type Database Entity"