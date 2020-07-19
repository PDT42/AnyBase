# Domain Analysis

## Asset
Eine Asset ist **ein** Datensatzelement. Jedes Asset hat einen AssetType.

## AssetManager
Der AssetManager verwaltet die Assets. Er stellt das Interface zwischen der Datenbank und dem Backend dar. Über ihn könnnen Assets abgerufen, erstellt und verwaltet werden. 

## AssetType
Ein AssetType definiert die Felder eines Assets. AssetTypes müssen in einer eigenen Datenbank gehalten werden, die beim StartUp der Software gelesen wird.
Im AssetType wird festgehalten, wie die Tabelle heißt, in die Assets des AssetTypes gespeichert werden. Er verknüpft das Asset mit den zu ihr gehörenden PageLayouts.

## AssetTypeManager
Der AssetTypeManager verwaltet die AssetTypes. Er stellt das Interface zwischen der Datenbank und dem Backend dar. Über ihn können AssetTypes abgerufen, erstellt und verwaltet werden.

## User (?)
Nutzer im System. Nutzer haben einen UserType, mit dem ihr Accesslevel angegeben wird. 

## UserType (?)
Wird an User vergeben. Vom UserType ist das Accesslevel von Nutzern abhängig.

## Plugin
Plugins sind das Herzstück von AnyBase. Plugin ist darum ein Interface, auf Basis dessen alle anderen Plugins funktionieren. Ein Plugin braucht dementsprechend eine Datenbankanbindung, mit Hilfe derer es auf den Datenbestand des Users zugreifen kann. Ein Plugin hat außerdem ein Data Requirement, getypte Pflichtfelder, deren required Types mit den zur Verfügung gestellten verglichen werden können. Für einen solchen Vergleich muss natürlich außerdem der AssetType zur Verfügung stehen, mit dem das Plugin arbeitet. Es könnte notwendig werden, dass Plugins auf mehr als einen AssetType zugreifen müssen.   

## PageLayout
Ein PageLayout ist eine bestimmte Seitenaufteilung, die der Nutzer für eine AssetPage oder eine AssetDetailPage festlegen kann. Jedes PageLayout hat eine Anzahl von Feldern, die mit Inhalten aus Plugins gefüllt werden können. 

## AssetPage
Eine AssetPage ist die Übersichtsseite für einen bestimmten AssetType.

## AssetTypePageManager
Der AssetTypePageManager sorgt dafür, dass im System initialisierte AssetTypes eine Route zur Verfügung gestellt bekommen, auf der etwas zu sehen ist. Er erzeugt aus den in der Datenbank gespeicherten Nutzereinstellungen, in denen ein PageLayout enthalten sein muss, dessen mögliche Felder mit Plugins gefüllt werden, die gespeichert werden müssen, eine Ansicht, die dem User gezeigt wird, wenn er die Route aufruft. Außerdem muss der AssetTypePageManager die Funktionalität der Frontend Einstellbarkeit zur Verfügung stellen. 

## AssetDetailPage
Eine AssetDetailPage ist die Übersichtsseite für eine Asset eines bestimmten AssetTypes.

## AssetDetailPageManager
Der AssetDetailPageManager sorgt dafür, dass im System initialisierte Assets eine 'Route' zur Verfügung gestellt bekommen, auf der etwas zu sehen ist. Er erzeugt aus den in der Datenbank gespeicherten Nutzereinstellungen, in denen ein PageLayout enthalten sein muss, dessen mögliche Felder mit Plugins gefüllt werden, die gespeichert werden müssen, eine Ansicht, die dem User gezeigt wird, wenn er die Route aufruft. Außerdem muss der AssetTypePageManager die Funktionalität der Frontend Einstellbarkeit zur Verfügung stellen. 