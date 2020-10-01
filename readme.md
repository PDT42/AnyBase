# AnyBase

This is AnyBase. Think of it as a backoffice version of Wordpress. It is meant to
be used by anyone. Most tasks in the backoffice can be reduced to storing, updating 
and overall managing data. Records about items in a stores inventory must be kept, 
holiday requests noted and the times employees spent working recorded. 

>Lets think about the usecase of a library. What would the management of a library
>require to digitize its backoffice? The documentation will use the concepts and
>mechanisms provided by AnyBase to digitize the library. 

## Concept and (some) Architecture

AnyBase uses the concept of [Asset]s to model any kind of item a user might want
to manage using the software. Since the managed assets will vary, depending on the
individual requirements of the user, he must first be enabled to define the [Asset]
he uses AnyBase to manage. An asset must be able to represent _anything_. AnyBase 
meets this requirement with the concept of [AssetType]s, which can be used to define
the digital model of the managed asset.

>These two are the central Elements of AnyBase. Any interaction the user can have with
the application will concern either an [Asset] or an [AssetType].

Assets and AssetTypes move through all the layers of AnyBase.

![Concept Diagram][concept_diagram]

AnyBase is realized as a webapp using a python backend powered by [Quart]. It is 
divided into several layers. First there obviously is the frontend of the webapp. 
The programmatic concept for the frontend right now is _rough_ at best. I'm not as 
familiar with frontend as I am with backend development #NeedHelpHere. It is certain
however, that the frontend will have to meet certain requirements.

#### AssetTypes & Assets

As mentioned earlier, everything in AnyBase concerns either an [Asset] or an [AssetType]. 
This is also true for the frontend. The user must be enabled to adjust the frontend with 
regard to his individual demands. This is why AnyBase provides the means, to define custom
views for [AssetType]s the user created. For each [AssetType] the user will be able to 
define two views. One for the _entity_ [AssetType] and one for a single [Asset] with 
that type. 

>Let's take a moment and think about the usecase example of the library. What _type_
>of assets would a libary want to define, in order to manage them using an awesome
>AnyBase? Well a library will probably need to manage books and stuff. I'll assume, 
>they'd want to defined some supertype [AssetType], that holds information common to 
>all the items a library might have in their inventory. I will call this type of [Asset]
>a "Media Article". The library will have personal as well as members, who can
>borrow books from the library. Both must be modelled (an [AssetType] must be configured),
>so data about them can be managed using AnyBase. 
>
>So let's define those [AssetType]s. More information about how configuring AssetTypes
>works and what requirements the configuration process entails, you can read [TODO].
>For now let's just assume we created the following AssetType sheme.
>
>
>![Library Types][library_types]

#### PageLayouts & Plugins

To hold the information on what one of this views should look like, there are the
[PageLayout]s. They contain general information and the definition of the _layout_
of the view. The view is made up from a number of rows, that themselves are filled 
with a number of columns represented by [ColumnInfo] objects. Each column can contain
a [Plugin]. A plugin must exist both as a frontend implementation that can be "put 
into the view", as well as a backend entity (PluginServer), that fulfills all the 
backend needs of the plugin.  

The frontend is served by the server layer, which is implemented as a number of
server singletons, which hold static methods serving as route outlets. The routes
are connected to the methods using [Quart]. The Servers use the Managers to do stuff 
in the database. 

## Modules and their functions

>TODO

I will list those from _inside to outside_. I hope this will help to get a grasp of 
_how the building blocks are stacked_.

### DbConnection

The DbConnection layer/abstract class realizes the connection between the manager and
the actual database. Implementations of DbConnections must provide a number of functions,
the managers later use to manipulate the managed data.

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

#### SqliteConnection

The SqliteConnection, as the name suggests, provides the methods necessary to interact with
a sqlite .db file/database. 

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``read``                | ``TestSqliteConnection`` | [DbConnection]    |
| ``read_joined``         | ``TestSqliteConnection`` | [DbConnection]    |
| ``delete``              | ``TestSqliteConnection`` | [DbConnection]    |
| ``write_dict``          | ``TestSqliteConnection`` | [DbConnection]    |
| ``update``              | ``TestSqliteConnection`` | [DbConnection]    |
| ``update_table_name``   | ``TestSqliteConnection`` | [DbConnection]    |
| ``update_columns``      | ``TestSqliteConnection`` | [DbConnection]    |
| ``update_append_column``| ``TestSqliteConnection`` | [DbConnection]    |
| ``update_remove_column``| ``TestSqliteConnection`` | [DbConnection]    |
| ``create_table``        | ``TestSqliteConnection`` | [DbConnection]    |
| ``delete_table``        | ``TestSqliteConnection`` | [DbConnection]    |
| ``get_table_info``      | ``TestSqliteConnection`` | [DbConnection]    |
| ``check_table_exists``  | ``TestSqliteConnection`` | [DbConnection]    |
| ``count``               | ``TestSqliteConnection`` | [DbConnection]    |

### Managers

Managers represent the connection between the server and the database layer.

#### AssetTypeManager

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

#### AssetManager

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

#### PageManager

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``create_page``         | ``TestSqliteConnection`` | [DbConnection]    |

### Servers

#### AssetTypeServer

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

#### AssetServer

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

#### PluginServers

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |

##### NotesPlugin

| __Method Name__         | __Tested by__            | __Documented in__ |
| ----------------------- |:------------------------:|:----------------- |
| ``convert_data_to_row`` | ``TestSqliteConnection`` | [DbConnection]    |


[//]: # (LINKS)
[Column]: entities/column.md
[Asset]: entities/assets.md
[AssetType]: entities/asset_types.md
[Quart]: https://github.com/pgjones/quart
[DbConnection]: database/db_connection.md
[PageLayout]: page_layouts/page_layout.md

[//]: # (IMAGES)
[concept_diagram]: doc/graphics/rendered_images/AnyBase.png
[library_types]: doc/graphics/rendered_images/LibraryTypes.png