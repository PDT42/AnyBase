# Asset Types

## Subtypes & Supertypes

AssetTypes are _the_ central element of AnyBase. They define the structure of [Asset]s managed by the software. 
To manage the AssetTypes available, there is the [AssetTypeManager], which provides the database interface to 
store, edit and get asset types. [Asset]s come with one of two AssetTypes: There are __supertype__ and __subtype__
AssetTypes. To create a subtype AssetType, there must first exist a super type. A supertype AssetType is 
basically any AssetType, who is implemented as a ``super_type`` by another AssetType. Still subtypes can 
themselves have subtypes. The AssetType, a subtype AssetType is sub to, is called __parent__. Subtypes realize
an Extension of their supertypes.

An AssetType is considered a subtype, if its ``super_type`` is less or equal to zero. This is just opportune, 
since every table, handled by AnyBase's [DbConnection], defines a ``pimary_key`` which, for sqlite, starts at 
one and automatically increases with every row appended and can thus be used in the ``super_type`` field as a
foreign key. In the future it might be sensable, to add a separate database column containing a true boolean,
indicating, wether an AssetType is a subtype or not.

> ### Example
>
>Let's, for example, take a look at some of the AssetTypes the library defines. The _Media Article_ is the most 
>general abstraction of one of the libraries items. It will serve as the supertype for all the AssetTypes the 
>library might want to define or manage. The _Book_ is one such AssetType. The _Book_ will extend the _Media Article_,
>by setting ``super_type_id = media_article.asset_type_id``. In doing so the _Book_ inherits all the fields of 
>the _Media Article_ and the user must not define them again. 
>
>Additionaly the _Book_ can be used in contexts designed to manage _Media Articles_. Take the case, for example,
>that a _Member_ of the library wants to borrow a _Book_. In this context, it's completely irrelevant whether the
>borrowed _Media Article_ is a _Book_ or a _DVD_. The process of borrowing a book will be the same either way. 
>Since the both _Book_ and _DVD_ implement _Media Article_  as a supertype and thus have all the fields of a
>_Media Article_, the user will be able to use both _Book_ and _DVD_ in workflows he configures for _Media Articles_.
>
>
>![Super Type][super_type]


## Owner

AssetTypes can be slaves and slave owners. This will probably shock you now, but sadly, it's the truth. Whether an 
AssetType is a slave is indicated by the AssetTypes ``is_slave`` and ``owner_id`` fields. AssetTypes who are configured
as _slavetypes_ are not indepentendly interesting, but only as "subsiduaries" for _other_ AssetTypes. The AssetType, 
who defines the field (typed either ASSET or ASSETLIST), the _owned AssetType_ is supposed to fill, is called _the owner_.
Just as one might think, the ``owner_id`` persists the ``asset_type_id`` of the _owner AssetType_. 
_Slavetypes_ exist to be employed at will by their _owner_. Since owned AssetTypes are not independently interesting, 
they are ignored by the [AssetTypeManager]s ``get_all`` functions. Instead, since we only ever want to get the slaves
of one AssetType, the [AssetTypeManager] defines a separate method ``get_slaves``. 

In the first possible ("standard") configuration for _slavetypes_ both, the ``is_slave`` field and the ``owner_id`` 
field, are set. This indicates, that a _slavetype_ will be, exclusively employed by it's _owner_ and discarded at will. 

Secondly there is the "public" configuration for _slavetypes_. If their ``is_slave`` flag is set, yet the AssetType
does not define an ``owner_id``, we call the AssetType a _public slave_, which can be employed by any other AssetType.
The [AssetTypeManager] will include these slaves in every call to ``get_slaves`` if not explicitly told to ignore them.

The last possible configuration for _slavetypes_ is the "private" configuration. This configuration indicates, that the
relationship between the _slave_ and _owner_ is much closer than traditionally allowed for. The _owner_ depends on 
the slave and can't be without it. This is why "private" slavetypes are not accessible to anyone but their _owner_,
who holds the only reference to them (Right now the only example for such a relationship is the _bookable\_type_).
In this configuration, the ``owner_id`` field of the _slavetype_ is set, yet the ``is_slave`` field indicates, that
this is not a slave (THIS IS SPARRRRRRTAAAAAA!!!!11elf1 ㄟ(≧◇≦)ㄏ). Every ``get`` method of the [AssetTypeManager]
will ignore types in this configuration, since these ``get`` methods, if they ignore slaves, will exclude any Type who
defines an ``owner_id`` and should they include slaves, will required the ``is_slave`` flag to be set.


## Bookable AssetTypes

Bookable AssetTypes are basically just normal AssetTypes who have the ``is_bookable`` flag set to true and define
a ``bookable_type_id``. This indicates that they can become subject of a _booking_. For these AssetTypes, when they
are created, the [AssetTypeManager] creates an additional AssetType: The _bookable\_type_. 

The _bookable\_type_ is intended as a super type for any AssetType who realizes a _booking_ of an Asset of this Type. 
A _booking_, in this context, meaning a temporary connection. A record in a list of records, that define both a start 
and an end. Events, that "concern" something (in this case an Asset of a certain AssetType). Appointments, temporal
assignments of resources, reservations, meetings. All these would be modelled as AssetTypes in AnyBase. All of those 
would implement some _bookable\_type_ as their _supertype_, since the Assets of these Types will all temporarily occupy
their _subject_. The Assets of these Types (Appointments and what not 🥱) can then be held in another Assets fields
and will usually be _slavetypes_.

> ### Example
>
>In the libraries usecase, an obvious bookable would be a Book. When creating the _Book_, the librarien would make the 
>it's Type bookable, by checking the appropriate box in the creation form.
>The AssetType _Book_ will have ``is_bookable = True`` set. On creation of _Book_, the [AssetTypeManager] 
>will generate an additional ``AssetType``: _bookable book_. This is the super type for any AssetType who realizes
>a booking of a book (e.g. 😒 when someone borrows a book). The Library defines the AssetType _Borrow_ (😩), which
>extends the _bookable book_. A _Member_ (someone who is registered with the library) can reference a number of such 
>_Borrows_ in one of it's fields (e.g. ``member.bookings: ASSETLIST``) and have the _Borrow_ as one of it's slaves.
>
>
> ![Bookable Type][bookable_type]


## Backend Representation


In the backend of the software an asset type is stored in a dataclass called ``AssetType``. All operations performed 
on asset types must use this as their input/output parameter type. An asset type should _never_ be handled in any 
other form in the backend. 

![Asset Type Class][asset_type_class]

Each asset type contains a list of [Column]s. This list defines the [Column]s required from a database table, so 
[Asset]s of this type can be stored in it. It also contains an ``asset_type_id``, which is filled by database's 
``primary_key``. The column ``primary_key`` is automatically added to each asset type table. When creating a new
asset type in the backend or using a frontend facility, the asset type does not need to set this field. When storing
the asset type in the database, the current implementation of the [AssetTypeManager] checks (and future implementations
will and should probably do so) if an asset type with that asset name already exists in the database, if not the 
AssetType is stored and the primary key is set by the database. When loading an asset AssetType from the database the 
``asset_type_id`` will be filled with the database row's ``primary_key``.


## Database Representation

All of these asset types are stored in the database table ``abintern_asset_types``. On creation, for each AssetType
an additional table called ``abasset_table_{asset_name}`` is created. The table name is generated from the name of the 
AssetType. The manner in which the table names are generated from the name is part of the abstract implementation of the
[AssetTypeManager], to guarantee, that future implementations of the [AssetTypeManager] will still be able to interact 
with the tables. The table name generation is provided in the static method ``generate_asset_table_name``. 

![Asset Type Database Representation][asset_type_db]

The fieldnames suggest the content. The only interesting one being ``asset_columns``. Since the [Column] is also an
item defined by AnyBase, in this field we store a string representation of the columns. This representation must be
the formatted the same way in each future version to guarantee interoperability, which is why the generation of the
representation is part of the abstract implementation of the [AssetTypeManager]. Right now we simply use 
``json.dumps(...)``, but I think it might be worth considering if implementing a less dataintensive enconding would
be worth the trouble. 

Also notable is, that the database representation of the AssetType is missing a column designed to store ``bookable``.
This is because there is no sceanario, in which an AssetType is bookable, but does not define a _bookable\_type_. 
Thus we can imply, whether an AssetType is bookable or not, from the fact, that it either does, or does not define
a _bookable\_type_.

[//]: # (LINKS)
[Column]: ../components/column.md
[Asset]: ../components/assets.md
[AssetTypeManager]: ../managers/asset_type_manager.md
[DbConnection]: ../database/db_connection.md

[//]: # (IMAGES)
[asset_type_class]: graphics/rendered_images/asset_type_class.png "Asset Type Class"
[bookable_type]: graphics/rendered_images/BookableType.png "Bookable Type"
[asset_type_db]: graphics/rendered_images/asset_type_db.png "Asset Type Database Entity"
[super_type]: graphics/rendered_images/SuperType.png "Super Type - Type Extension"