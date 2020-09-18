# AnyBase

This is AnyBase. Think of it as a backoffice version of Wordpress. It is meant to
be used by anyone. Most tasks in the backoffice can be reduced to storing updating 
and overall managing data. Be it records about items in the inventory of a store. 
The documentation files provided in this repository will use the usecase-example
of a library. 

Lets think about the needs of a library. What would the management of a library
require to digitize its backoffice? The documentation will use the concepts and
mechanisms provided by AnyBase to digitize the library. 

## Concept

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


As mentioned earlier, everything in AnyBase concerns either an [Asset] or an [AssetType]. 
This is also true for the frontend. The user must be enabled to adjust the frontend with 
regard to his individual demands. This is why AnyBase provides the means, to define custom
views for [AssetType]s the user created. For each [AssetType] the user will be able to 
define two views. One for the _entity_ [AssetType] and one for a single [Asset] with 
that type. 

To hold the information on what one of this views should look like, there are the
[PageLayout]s. They contain general information and the definition of the _layout_
of the view. The view is made up from a number of rows, that themselves are filled 
with a number of columns represented by [ColumnInfo] objects. Each column can contain
a [Plugin]. A plugin must exist both as a frontend implementation that can be "put 
into the view", as well as a backend entity, that fulfills all the backend needs of 
the plugin.  

The frontend is served by the server layer, which is implemented as a number of
server singletons, which hold static methods serving as route outlets. The routes
are connected to the methods using [Quart]. The Servers use the Managers to do stuff 
in the database. 

[//]: # (LINKS)
[Column]: https://github.com/PDT420/AnyBase/blob/master/doc/components/column.md
[Asset]: https://github.com/PDT420/AnyBase/blob/master/doc/components/assets.md
[AssetType]: https://github.com/PDT420/AnyBase/blob/master/doc/components/asset_types.md
[Quart]: https://github.com/pgjones/quart

[//]: # (IMAGES)
[concept_diagram]: doc/graphics/rendered_images/AnyBase.png