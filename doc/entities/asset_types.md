# Asset Types

## Subtypes & Supertypes

Asset types are _the_ central element of AnyBase. They define the structure of [Asset]s managed by the software. 
To manage the asset types available, there is the asset type manager, which provides the database interface to 
store, edit and get asset types. [Asset]s come with one of two different types: There are __supertype__ and 
__subtype__ asset types. To create a subtype asset type, there must first exist a super type. A supertype asset 
type is basically any asset type, which is not a subtype. Still subtypes can themselves have subtypes. The asset 
type, a subtype asset type is sub to, is called __parent__. Subtypes realize an Extension Type.

>An AssetType is considered a subtype, if its ``super_type`` is less or equal to zero. This is just opportune, 
>since every table, handled by AnyBase's DbConnection, defines a ``pimary_key`` which, for sqlite, starts at one 
>and automatically increases with every row appended. In the future it might be sensable, to add a separate 
>database column containing a true boolean, indicating, wether an AssetType is a subtype or not.


> ### Example
>
>For example: Let's look at some of the AssetTypes the library defines. The _Media Ariticle_ is the most general
>abstraction of an item the library might want to manage. It will serve as the super type for all the asset types
>the library might want to define or manage.
>
>
>![Super Type][super_type]
>
>
> 

## Owner

AssetTypes can be slaves and slave owners. This probably comes as a shock to you, but sadly, it's the truth.
This is indicated by the AssetTypes ``is_slave`` and ``owner_id`` fields. Those fields suggest, that an asset_type
is not independently interesting, but only as a field value for _another_ AssetType. The AssetType, who defines 
the field, the _owned AssetType_ is supposed to fill, is called the _owner_. Just as one might think, the 
``owner_id`` persists the id of the _owner AssetType_. Though highly politically incorrect, the _owned AssetTypes_
are called _slave_ types. They exist to be used by their _owner_.
Since owned AssetTypes are not independently interesting, they are ignored by the AssetTypeManagers ``get_all`` 
functions. Instead, since we only ever want to get the slaves of one AssetType, the AssetTypeManager defines a 
separate method ``get_slaves``. There is an additional configuration for slave types. If the ``is_slave`` is set,
yet the AssetType does not define an ``owner_id``, it is a public slave, to be employed by anyone.

## Bookable AssetTypes

Bookable AssetTypes are basically just normal AssetTypes who have the ``is_bookable`` flag set to true and define
a ``bookable_type_id``. For these AssetTypes, when they are created, the [AssetTypeManager] creates an additional
AssetType the _bookable type_. The _bookable_type_ is intended as a super type for any AssetType who realizes
a booking of an asset of this type.

> ### Example
>
>In the libraries usecase, an obvious bookable would be a Book. When creating the Book, the user would make the 
>Book bookable, by checking the appropriate box in the creation form.
>
>
> ![Bookable Type][bookable_type]
>
>
>The library defines an AssetType _Book_ with ``is_bookable = True``. On creation of _Book_, the [AssetTypeManager] 
>will generate an additional ``AssetType``: _bookable book_. This is the super type for any AssetType who realizes
>a booking of a book (e.g. 😒 when someone borrows a book). The Library defines the AssetType _Borrow_ (😩), who 
>extends the _bookable book_. A _Member_ (someone who is registered with the library) can have a number of such 
>borrows.

## Backend Representation

>TODO: Update

In the backend of the software an asset type is stored in a dataclass called ``AssetType``. All operations performed 
on asset types must use this as their input/output parameter type. An asset type should _never_ be handled in any 
other form in the backend. 

![Asset Type Class][asset_type_class]

Each asset type contains a list of [Column]s. This list defines the columns required from a database table, so 
[Asset]s of this type can be stored in it. It also contains an asset type id, which is filled database primary key.
The column ``primary_key`` is automatically added to each asset type table. When creating a new asset type in the 
backend or using a frontend facility, the asset type does not need to set this field. When storing the asset type 
in the database, the current implementation of the asset type manager checks (and future implementations will and 
should probably do so) if an asset type with that asset name already exists in the database, if not the asset type 
is stored and the primary key is set for the asset type. When loading an asset type from the databse the 


## Database Representation

>TODO: Update

All of these asset types are stored in the database table ``abintern_asset_types``. On creation, for each asset type
an additional table called ``abasset_table_{asset_name}``. The table name is generated from the name of the asset 
type. The manner in which the table names are generated from the name is part of the abstract implementation of the
asset type manager, to guarantee, that future implementations of the asset type manager will still be able to access
these tables. The table name generation is provided by the static method ``generate_asset_table_name``. 

![Asset Type Database Representation][asset_type_db]

The fieldnames suggest the content. The only interesting one being ``asset_columns``. Since the [Column] is also an
item defined by AnyBase, in this field we store a string representation of the columns. This representation must be
the formatted the same way in each future version to guarantee interoperability, which is why the generation of the
representation is part of the abstracth implementation of the asset type manager.

[//]: # (LINKS)
[Column]: ../components/column.md
[Asset]: ../components/assets.md

[//]: # (IMAGES)
[asset_type_class]: graphics/rendered_images/asset_type_class.png "Asset Type Class"
[bookable_type]: graphics/rendered_images/BookableType.png "Bookable Type"
[asset_type_db]: graphics/rendered_images/asset_type_db.png "Asset Type Database Entity"
[super_type]: graphics/rendered_images/SuperType.png "Super Type - Type Extension"